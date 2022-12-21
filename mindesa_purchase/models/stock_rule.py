from collections import defaultdict
from dateutil.relativedelta import relativedelta
from itertools import groupby

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _merge_purchase_lines(self, lines):
        groups = {}
        to_unlink = self.env['purchase.order.line'].sudo()
        for line in lines:
            key = (line.product_id, line.product_uom)
            if key not in groups:
                groups[key] = line
            else:
                groups[key].write({'product_qty': groups.get(key).product_qty + line.product_qty})
                to_unlink |= line
        to_unlink.unlink()
        return True
    
    def _run_buy(self, procurements):

        procurements_by_po_domain = defaultdict(list)
        for procurement, rule in procurements:

            # Get the schedule date in order to find a valid seller
            procurement_date_planned = fields.Datetime.from_string(procurement.values['date_planned'])
            schedule_date = (procurement_date_planned - relativedelta(days=procurement.company_id.po_lead))

            supplier = procurement.product_id.with_context(force_company=procurement.company_id.id)._select_seller(
                partner_id=procurement.values.get("supplier_id"),
                quantity=procurement.product_qty,
                date=schedule_date.date(),
                uom_id=procurement.product_uom)

            if not supplier:
                msg = _('There is no matching vendor price to generate the purchase order for product %s (no vendor defined, minimum quantity not reached, dates not valid, ...). Go on the product form and complete the list of vendors.') % (procurement.product_id.display_name)
                raise UserError(msg)

            partner = supplier.name
            # we put `supplier_info` in values for extensibility purposes
            procurement.values['supplier'] = supplier
            procurement.values['propagate_date'] = rule.propagate_date
            procurement.values['propagate_date_minimum_delta'] = rule.propagate_date_minimum_delta
            procurement.values['propagate_cancel'] = rule.propagate_cancel

            domain = rule._make_po_get_domain(procurement.company_id, procurement.values, partner)
            procurements_by_po_domain[domain].append((procurement, rule))

        res = super(StockRule, self)._run_buy(procurements)

        for domain, procurements_rules in procurements_by_po_domain.items():
            # Get the procurements for the current domain.
            # Get the rules for the current domain. Their only use is to create
            # the PO if it does not exist.
            # procurements, rules = zip(*procurements_rules)

            # Get the set of procurement origin for the current domain.
            # origins = set([p.origin for p in procurements])
            # Check if a PO exists for the current domain.
            po = self.env['purchase.order'].sudo().search([dom for dom in domain], limit=1)

            # have to add this extra step since changing the POL uom will fail to let the line merge in existing line
            # and I really don't want to overload a major function like run_buy
            # so here we just check again is some lines can be merged, if so, merge them here
            if po:
                to_be_merged = self.env['purchase.order.line'].sudo()
                for line in po.order_line:
                    if not line.display_type:
                        to_be_merged |= line      
                self._merge_purchase_lines(to_be_merged)

    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, values, po):
        partner = values['supplier'].name
        procurement_uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        seller = product_id.with_context(force_company=company_id.id)._select_seller(
            partner_id=partner,
            quantity=procurement_uom_po_qty,
            date=po.date_order and po.date_order.date(),
            uom_id=product_id.uom_po_id)
        res = super(StockRule, self)._prepare_purchase_order_line(product_id, product_qty, product_uom, company_id, values, po)
        seller_product_uom = seller.product_uom
        seller_product_qty = product_uom._compute_quantity(product_qty, seller_product_uom)
        res.update({
            'product_uom': seller_product_uom.id,
            'product_qty': seller_product_qty
        })
        return res

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
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
    
    @api.multi
    def _run_buy(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        cache = {}
        suppliers = product_id.seller_ids.filtered(lambda r: (not r.company_id or r.company_id == values['company_id']) and (not r.product_id or r.product_id == product_id) and r.name.active)
        if not suppliers:
            msg = _('There is no vendor associated to the product %s. Please define a vendor for this product.') % (product_id.display_name,)
            raise UserError(msg)
        supplier = self._make_po_select_supplier(values, suppliers)
        partner = supplier.name
        # we put `supplier_info` in values for extensibility purposes
        values['supplier'] = supplier
    
        domain = self._make_po_get_domain(values, partner)
        po = False
        if domain in cache:
            po = cache[domain]
        else:
            po = self.env['purchase.order'].sudo().search([dom for dom in domain])
            po = po[0] if po else False
            cache[domain] = po
            
        res = super(StockRule, self)._run_buy(product_id, product_qty, product_uom, location_id, name, origin, values)

        # have to add this extra step since changing the POL uom will fail to let the line merge in existing line
        # and I really don't want to overload a major function like run_buy
        # so here we just check again is some lines can be merged, if so, merge them here
        if po:
            to_be_merged = self.env['purchase.order.line'].sudo()
            for line in po.order_line:
                if line._merge_in_existing_line(product_id, product_qty, product_uom, location_id, name, origin, values):
                    to_be_merged |= line      
            self._merge_purchase_lines(to_be_merged)

        return res

    @api.multi
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, values, po, partner):
        procurement_uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        seller = product_id.with_context(force_company=values['company_id'].id)._select_seller(
            partner_id=partner,
            quantity=procurement_uom_po_qty,
            date=po.date_order and po.date_order.date(),
            uom_id=product_id.uom_po_id)
        res = super(StockRule, self)._prepare_purchase_order_line(product_id, product_qty, product_uom, values, po, partner)
        product_uom = seller.product_uom
        product_qty = product_id.uom_po_id._compute_quantity(procurement_uom_po_qty, product_uom)
        res.update({
            'product_uom': product_uom.id,
            'product_qty': product_qty
        })
        return res
                
                
    
    


    

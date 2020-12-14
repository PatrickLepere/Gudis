# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, registry, _, SUPERUSER_ID
from odoo.exceptions import AccessError


_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def confirm_rfq_action(self, automatic=True):
        # Rescue mechanism to commit the changes on each iteration.
        if automatic:
            cr = registry(self._cr.dbname).cursor()
            self = self.with_env(self.env(cr=cr))
        for purchase in self:
            if purchase.state in ['draft','sent'] and purchase.partner_id.is_rfq_confirm and purchase.user_id.is_rfq_confirm:
                try:
                    purchase.button_confirm()
                except Exception:
                    if automatic:
                        cr.rollback()
                    _logger.info("Could not confirm [%s] using scheduled cron to confirm RFQ(S)." % (purchase.name))
            if automatic:
                cr.commit()
        if automatic:
            cr.commit()
            cr.close()

    def _add_supplier_to_product(self):
        # Add the partner in the supplier list of the product if the supplier is not registered for
        # this product. We limit to 10 the number of suppliers for a product to avoid the mess that
        # could be caused for some generic products ("Miscellaneous").
        for line in self.order_line:
            # Do not add a contact as a supplier
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            if line.product_id and partner not in line.product_id.seller_ids.mapped('name') and len(line.product_id.seller_ids) <= 10:
                # Convert the price in the right currency.
                currency = partner.property_purchase_currency_id or self.env.company.currency_id
                price = self.currency_id._convert(line.price_unit, currency, line.company_id, line.date_order or fields.Date.today(), round=False)
                # Compute the price for the template's UoM, because the supplier's UoM is related to that UoM.
                if line.product_id.product_tmpl_id.uom_po_id != line.product_uom:
                    default_uom = line.product_id.product_tmpl_id.uom_po_id
                    price = line.product_uom._compute_price(price, default_uom)

                supplierinfo = {
                    'name': partner.id,
                    'sequence': max(line.product_id.seller_ids.mapped('sequence')) + 1 if line.product_id.seller_ids else 1,
                    'min_qty': 0.0,
                    'price': price,
                    'currency_id': currency.id,
                    'delay': 0,
                    ############# custom code start ###############
                    'product_uom': line.product_uom.id,
                    ############# custom code end ################

                }
                # In case the order partner is a contact address, a new supplierinfo is created on
                # the parent company. In this case, we keep the product name and code.
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.order_id.date_order and line.order_id.date_order.date(),
                    uom_id=line.product_uom)
                if seller:
                    supplierinfo['product_name'] = seller.product_name
                    supplierinfo['product_code'] = seller.product_code
                vals = {
                    'seller_ids': [(0, 0, supplierinfo)],
                }
                try:
                    line.product_id.write(vals)
                except AccessError:  # no write access rights -> just ignore
                    break

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        if self.partner_id.is_rfq_confirm and self.company_id.partner_id.property_stock_customer and \
            self.partner_id != self.company_id.partner_id and \
            ((self.env.uid == SUPERUSER_ID) or (self.env.user.company_id.partner_id == self.partner_id)):
            res['location_id'] = self.company_id.partner_id.property_stock_customer.id
        return res

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        if self.order_id.partner_id.is_rfq_confirm and self.company_id.partner_id.property_stock_customer and \
            self.order_id.partner_id != self.company_id.partner_id and \
            ((self.env.uid == SUPERUSER_ID) or (self.env.user.company_id.partner_id == self.order_id.partner_id)):
            for line_vals in res:
                line_vals['location_id'] = self.company_id.partner_id.property_stock_customer.id
        return res

from odoo import api, fields, models, _
from odoo import SUPERUSER_ID


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

from odoo import api, fields, models, _


class AccountInvoice(models.TransientModel):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        if self._context.get("create_bill") and self.user_has_groups(
            "purchase.group_purchase_user,!purchase.group_purchase_manager"
        ):
            self = self.sudo()
        return super(AccountInvoice, self).create(vals)

    def action_invoice_open(self):
        if self.user_has_groups(
            "purchase.group_purchase_user,!purchase.group_purchase_manager"
        ):
            self = self.sudo()
        return super(AccountInvoice, self).action_invoice_open()

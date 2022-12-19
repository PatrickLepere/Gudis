from odoo import api, fields, models, _


class account_payment(models.Model):
    _inherit = "account.payment"

    def action_validate_invoice_payment(self):
        if self.user_has_groups(
            "purchase.group_purchase_user,!purchase.group_purchase_manager"
        ):
            self = self.sudo()
        return super(account_payment, self).action_validate_invoice_payment()

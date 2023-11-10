from odoo import api, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        if self.env.context.get("create_bill") and self.user_has_groups(
            "purchase.group_purchase_user,!purchase.group_purchase_manager"
        ):
            self = self.sudo()
        return super().create(vals)

    def _post(self, soft=True):
        if self.user_has_groups(
            "purchase.group_purchase_user,!purchase.group_purchase_manager"
        ):
            self = self.sudo()
        return super()._post(soft)

from odoo import fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"

    is_rfq_confirm = fields.Boolean(string="Is RFQ confirm")

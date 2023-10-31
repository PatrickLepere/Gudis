from odoo import api, fields, models, _


class Users(models.Model):
    _inherit="res.users"

    is_rfq_confirm = fields.Boolean(string="Is RFQ confirm")

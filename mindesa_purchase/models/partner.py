# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = "res.partner"

    is_rfq_confirm = fields.Boolean(string="Is RFQ confirm")

class Users(models.Model):
    _inherit="res.users"

    is_rfq_confirm = fields.Boolean(string="Is RFQ confirm")


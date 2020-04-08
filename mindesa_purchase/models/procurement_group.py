# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def run_scheduler(self, use_new_cursor=False, company_id=False):
        res = super(ProcurementGroup,self).run_scheduler(use_new_cursor, company_id)
        purchases = self.env['purchase.order'].search([])
        purchases.confirm_rfq_action()  
        return res

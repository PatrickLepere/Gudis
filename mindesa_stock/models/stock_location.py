# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


# class StockLocation(models.Model):
#     _inherit = "stock.location"

#     def _should_be_valued(self):
#         """ This method returns a boolean reflecting whether the products stored in `self` should
#         be considered when valuating the stock of a company.
#         """
#         self.ensure_one()
#         res = super(StockLocation, self)._should_be_valued()
#         if self.usage == 'transit':
#             return False
#         return res
    

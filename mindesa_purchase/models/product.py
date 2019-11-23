# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    # this is the original product_uom, keep it here in order to not confuse people in the future
    product_uom_default = fields.Many2one('uom.uom', ondelete="set null", related='product_tmpl_id.uom_po_id', string="Unit of Measure (Default)", help="This comes from the product form.")
    # this is necessary to add a domain to the new product_uom from form view
    product_uom_category_id = fields.Many2one('uom.category', related='product_tmpl_id.uom_po_id.category_id')
    # this is the new editable product uom
    product_uom = fields.Many2one('uom.uom', ondelete='set null', string='Unit of Measure (Vendor)', store=True, readonly=False, related=False, required=True)

    
    


    

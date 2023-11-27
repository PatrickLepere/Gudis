from odoo import fields, models, _


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    # this is the original product_uom, keep it here in order to not confuse people in the future
    product_uom_default = fields.Many2one('uom.uom', ondelete="set null", related='product_tmpl_id.uom_po_id', string="Unit of Measure (Default)", help="This comes from the product form.")
    # this is necessary to add a domain to the new product_uom from form view
    product_uom_category_id = fields.Many2one('uom.category', related='product_tmpl_id.uom_po_id.category_id')
    # this is the new editable product uom
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure (Vendor)', store=True, readonly=False, related=False, required=False)


class ProductProduct(models.Model):
    _inherit = 'product.product'


    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False):
        sellers = self._get_filtered_sellers(partner_id=partner_id, quantity=quantity, date=date, uom_id=uom_id, params=params)
        res = self.env['product.supplierinfo']
        for seller in sellers:
            if not res or res.name == seller.name:
                res |= seller
        # Start Patch
        res = sellers.filtered(lambda s: s.name == res.company_id.partner_id) if res.company_id else res
        # End Patch
        return res and res.sorted('price')[:1]

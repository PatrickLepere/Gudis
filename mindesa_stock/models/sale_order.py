from odoo import api, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('move_ids.state', 'move_ids.scrapped', 'move_ids.product_uom_qty', 'move_ids.product_uom')
    def _compute_qty_delivered(self):
        super()._compute_qty_delivered()

        for line in self:
            if line.qty_delivered_method == 'stock_move':
                qty = 0.0
                for move in line.move_ids.filtered(lambda r: r.state == 'done' and not r.scrapped and line.product_id == r.product_id):
                    if move.location_dest_id.usage in ("customer", "transit"):
                        if not move.origin_returned_move_id or (move.origin_returned_move_id and move.to_refund):
                            qty += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                    elif move.location_dest_id.usage not in ("customer", "transit") and move.to_refund:
                        # [EHE] this might cause issue in the future,  what if dest is transit (i.e., return to a transit location)?
                        qty -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                line.qty_delivered = qty

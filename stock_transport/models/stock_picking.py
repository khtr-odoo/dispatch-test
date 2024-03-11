from odoo import api,models,fields

class StockPickingType(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(string="Volume", compute="_compute_volume")
    weight = fields.Float(string="Weight", compute="_compute_weight")
    
    
    @api.depends("move_ids")
    def _compute_volume(self):
        v = 0
        for record in self:
            v = 0
            temp = record.move_ids
            for product in temp:
                v = v + product.product_id.volume * product.product_uom_qty
            record.volume = v 

    @api.depends("move_ids")
    def _compute_weight(self):
        w = 0
        for record in self:
            w = 0
            temp = record.move_ids
            for product in temp:
                w = w + product.product_id.weight * product.product_uom_qty
            record.weight = w 
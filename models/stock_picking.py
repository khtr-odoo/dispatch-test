from odoo import api,models,fields

class StockPickingType(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(string="Volume", compute="compute_volume")
    
    @api.depends("move_line_ids")
    def compute_volume(self):

        v = 0
        for record in self:
            temp = record.move_line_ids
            for product in temp:
                v = v + product.product_id.volume * product.quantity
                self.volume = v 
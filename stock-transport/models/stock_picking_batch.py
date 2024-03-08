from odoo import api,fields,models

class StockPickingBatch(models.Model):
    _inherit = ['stock.picking.batch']

    dock_id = fields.Many2one('stock.transport.dock', string="Dock")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', string="Vehicle Category")
    volume = fields.Float(string="Volume", compute="_compute_weight_volume", store=True)
    weight = fields.Float(string="Weight(kg)", compute="_compute_weight_volume", store=True)
    moves_number = fields.Float(string="Move Lines", compute="_compute_moves_number", store=True)
    transfers_number  = fields.Float(string="Transfer Lines", compute="_compute_moves_number", store=True)
    total_weight = fields.Float(string="Weight", compute="_compute_weight_volume", store=True)
    total_volume = fields.Float(string="Volume", compute="_compute_weight_volume", store=True)

    @api.depends('picking_ids','vehicle_category_id')
    def _compute_weight_volume(self):
        for record in self:
            for move_line in record.picking_ids:
                weight = 0
                volume = 0

                weight = weight + move_line.weight
                volume = volume + move_line.volume

                record.total_weight = weight
                record.total_volume = volume
                record.weight = (weight / record.vehicle_category_id.max_weight) * 100 if record.vehicle_category_id.max_weight != 0 else 0
                record.volume = (volume / record.vehicle_category_id.max_volume) * 100 if record.vehicle_category_id.max_volume != 0 else 0

    @api.depends("move_line_ids", "picking_ids")
    def _compute_moves_number(self):
        for record in self:
            record.moves_number = len(record.move_line_ids)
            record.transfers_number = len(record.picking_ids)

    @api.depends("name", "weight", "volume")
    def _compute_display_name(self):
        for record in self:
            record.display_name = "{} ({:.2f}kg, {:.2f}m\u00b3)".format(record.name,record.weight, record.volume)
             
            
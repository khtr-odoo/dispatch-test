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
    # start_date = fields.Date(string="Start Date", default=fields.Date.today, store=True)
    # end_date = fields.Date(string="End Date", store=True)

    @api.depends("vehicle_category_id")
    def _compute_weight_volume(self):
        for record in self:
            move_line_ids = []

            weight = 0
            volume = 0

        for move_line_id in record.move_line_ids:
            move_line_ids.append(move_line_id.id)

        move_lines = self.env["stock.move.line"].browse(move_line_ids)

        for move_line in move_lines:
            weight += move_line.product_id.weight * move_line.quantity
            volume += move_line.product_id.volume * move_line.quantity

            record.weight = weight / record.vehicle_category_id.max_weight if record.vehicle_category_id.max_weight != 0 else 0
            record.volume = volume / record.vehicle_category_id.max_volume if record.vehicle_category_id.max_volume != 0 else 0

    @api.depends("move_line_ids", "picking_ids")
    def _compute_moves_number(self):
        for record in self:
            record.moves_number = len(record.move_line_ids)
            record.transfers_number = len(record.picking_ids)
            
    
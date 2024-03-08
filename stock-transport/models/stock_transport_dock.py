from odoo import api,fields, models

class StockTransportDock(models.Model):
    _name = "stock.transport.dock"
    _description = "Stock Transport Dock Model"

    name = fields.Char("Dock name")

   
{
    'name' : 'Stock Transport',
    'version' : '17.0.1.0.0',
    'description' : """ Stock Transport developed by khtr """,
    'depends': ['fleet', 'stock_picking_batch'],
    'data' : [
        'security/ir.model.access.csv',
        'views/fleet_vehicle_model_category_views.xml',
        'views/stock_picking_batch_views.xml',
        'views/stock_picking_views.xml'
        ]
}
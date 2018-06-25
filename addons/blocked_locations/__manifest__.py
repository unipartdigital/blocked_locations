# -*- coding: utf-8 -*-
{
    'name': "blocked_locations",
    'summary': 'Handling of blocked locations.',
    'description': """
Handling of blocked locations.

- Stock.quants cannot be reserved at blocked locations
- Location_id and/or location_dest_id for stock.picking, stock.move,
  stock.move.line, stock.inventory and stock.iventory.line cannot
  be a blocked location.
    """,
    'author': 'Unipart Digital',
    'category': 'Warehouse Management',
    'version': '0.1',
    #'license': 'LGPL-3',
    'depends': ['base', 'stock'],
    'data': [
        'views/stock_location.xml',
    ],
}

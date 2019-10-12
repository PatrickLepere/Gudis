# -*- coding: utf-8 -*-
{
    'name': "POS NETWORK PRINTER",
    'summary': """
        Print from Point of sale to ESC/POS Network Printer without POS Box. The module is used for POS Retail
        """,
    'description': """
        Print from Point of sale to ESC/POS Network Printer without POS Box. The module is used for POS Retail
    """,
    'author': "Aimé Jules Andrinirina",
    'website': 'https://www.aimejules.com',
    'license': 'OPL-1',
    'category': 'Point Of Sale',
    'version': '12.0.1.1',
    'images': ['static/description/banner.jpg'],
    'depends': ['base', 'point_of_sale'],
    'qweb': ['static/src/xml/pos.xml'],
    'data': [
        # security
        'security/ir.model.access.csv',
        # views
        'views/assets.xml',
        'views/pos_config_view.xml',
        'views/network_printer_view.xml',
    ],
    'price': '300',
    'currency': 'EUR',
    'live_test_url': 'https://demo.aimejules.com',

}

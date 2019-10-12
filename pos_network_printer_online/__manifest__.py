# -*- coding: utf-8 -*-
{
    'name': "POS NETWORK PRINTER ONLINE",
    'summary': """
        Connect local printer to Pos retail for online server using Odoo Printer Connector
    """,
    'description': """
        Connect local printer to Pos retail for online server using Odoo Printer Connector
    """,
    'author': "Aimé Jules Andrinirina",
    'website': 'https://www.aimejules.com',
    'license': 'OPL-1',
    'category': 'Point Of Sale',
    'version': '0.1',
    'images': ['static/description/banner.jpg'],
    'depends': [
        'base',
        'pos_network_printer',
    ],
    'data': [
        # security
        'security/security.xml',
        'security/ir.model.access.csv',
        # views
        'views/printer_connector_view.xml',
        'views/network_printer_view.xml',
        'views/queue_print_view.xml',
        'views/assets.xml',
    ],
    'price': '20',
    'currency': 'EUR',
    'live_test_url': 'https://demo.aimejules.com',
}

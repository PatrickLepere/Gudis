# -*- coding: utf-8 -*-

from odoo import models, fields, api

class NetworkPrinter(models.Model):
    _inherit = 'network.printer'

    connector_id = fields.Many2one('printer.connector', string='Connector', required=True)
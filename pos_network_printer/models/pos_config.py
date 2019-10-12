# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    ticket_print_mode = fields.Selection([('web', 'Web'), ('network', 'Network')], string='Ticket print mode', default='web', required=True)
    network_printer_ids = fields.Many2many('network.printer', string='Network printers')

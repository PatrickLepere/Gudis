odoo.define('pos_network_printer_online.Models', function (require) {
    'use strict';
    var models = require('point_of_sale.models');
    models.load_fields('network.printer','connector_id');
    models.load_models({
        model: 'printer.connector',
        fields: ['id', 'token'],
        domain: null,
        loaded: function (self, connector) {
            var printer_connectors = []
            for (var i = 0; i < connector.length; i++) {
                printer_connectors.push(connector[i]);
            }
            self.printer_connectors = printer_connectors;
        },
    });
});
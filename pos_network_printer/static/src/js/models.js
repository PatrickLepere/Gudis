odoo.define('pos_network_printer.Models', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    models.load_models({
        model: 'network.printer',
        fields: ['printer_name', 'printer_ip', 'printer_port'],
        domain: null,
        loaded: function (self, printers) {
            var network_printers_config = {};
            var network_printers_active = [];
            for (var i = 0; i < self.config.network_printer_ids.length; i++) {
                network_printers_config[self.config.network_printer_ids[i]] = true;
            }
            for (var i = 0; i < printers.length; i++) {
                if (network_printers_config[printers[i].id]) {
                    network_printers_active.push(printers[i]);
                }
            }
            self.network_printers = network_printers_active;
        },
    });
});
odoo.define('pos_network_printer_online.NetworkDevices', function (require) {
    "use strict";
    var NetworkDevices = require('pos_network_printer.NetworkDevices');
    var rpc = require('web.rpc');

    NetworkDevices.include({
        print_network_xmlreceipt: function (widget, receipt, printer) {
            var self = this;
            var order = widget.pos.get_order();
            var queue_print_data = {
                // "uid": order.uid,
                "printer_name": printer.printer_name,
                "printer_ip": printer.printer_ip,
                "printer_port": printer.printer_port,
                "connector_id": printer.connector_id[0],
                "receipt": receipt,
                "token": self.get_connector_token(widget, printer),
            }
            rpc.query({
                model: 'queue.print',
                method: 'create',
                args: [queue_print_data]
            }).then(function (result) {
                console.log('new queue created ' + 1);
            });

        },
        get_connector_token: function (widget, printer) {
            var connector = _.filter(widget.pos.printer_connectors, function (line) {
                return line.id == printer.connector_id[0]
            });
            return connector[0].token;
        }
    });
});
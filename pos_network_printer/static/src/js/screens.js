odoo.define('pos_network_printer.ReceiptScreenWidget', function (require) {
    'use strict';
    var screens = require('point_of_sale.screens');
    var ReceiptScreenWidget = screens.ReceiptScreenWidget;
    var core = require('web.core');
    var QWeb = core.qweb;
    var NetworkDevices = require('pos_network_printer.NetworkDevices');

    ReceiptScreenWidget.include({
        print_web: function () {
            var self = this;
            if (self.pos.config.ticket_print_mode == 'web') {
                window.print();
            }
            if (self.pos.config.ticket_print_mode == 'network') {
                self.print_network();
            }
            this.pos.get_order()._printed = true;
        },
        print_network: function () {
            var self = this;
            var printers = this.pos.network_printers;
            var receipt_data = this.pos.get_order().export_for_printing();
            _.each(receipt_data.orderlines, function (line) {
                // quantity
                var nb = String(line.quantity);
                if (nb.length == 1) {
                    line.quantity_nb = '<pre>  ' + line.quantity + '</pre>';
                }
                else if (nb.length == 2) {
                    line.quantity_nb = '<pre> ' + line.quantity + '</pre>';
                }
                else if (nb.length == 3) {
                    line.quantity_nb = line.quantity;
                }

                //product_name
                var product_nb = line.product_name_wrapped[0].length;
                var max_nb = 20;
                var final_product = "";
                if (product_nb >= max_nb) {
                    for (var i = 0; i < max_nb; i++) {
                        final_product = final_product + line.product_name_wrapped[0][i];
                    }
                } else {
                    var diff_nb = max_nb - product_nb;
                    final_product = '<pre>' + line.product_name_wrapped[0];
                    for (var i = 0; i < diff_nb; i++) {
                        final_product = final_product + ' ';
                    }
                    final_product = final_product + '</pre>';
                }
                line.final_product = final_product;

                //price unit
                var max_pu_nb = 7;
                var pu_nb = String(line.price).length;
                var diff_pu_nb = max_pu_nb - pu_nb;
                var final_pu = "<pre>";
                for (var i = 0; i < diff_pu_nb; i++) {
                    final_pu = final_pu + ' ';
                }
                final_pu = final_pu + line.price + '</pre>';
                line.final_pu = final_pu;

                //price display
                var max_pd_nb = 10;
                var pd_nb = String(line.price_display).length;
                var diff_pd_nb = max_pd_nb - pd_nb;
                var final_pd = "<pre>";
                for (var i = 0; i < diff_pd_nb; i++) {
                    final_pd = final_pd + ' ';
                }
                final_pd = final_pd + line.price_display + '</pre>';
                line.final_pd = final_pd;
            });
            var env = {
                widget: this,
                pos: this.pos,
                order: this.pos.get_order(),
                receipt: receipt_data,
                paymentlines: this.pos.get_order().get_paymentlines()
            };
            var receipt = QWeb.render('XmlReceipt', env);
            var Printer = new NetworkDevices();
            for (var i = 0; i < printers.length; i++) {
                Printer.print_network_xmlreceipt(this, receipt, printers[i]);
            }
        }
    });
});
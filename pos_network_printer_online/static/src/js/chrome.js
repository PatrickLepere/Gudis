odoo.define('pos_network_printer_online.RemoveStatusWidget', function (require) {
    'use strict';

    var pos_chrome = require('point_of_sale.chrome');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    var _lt = core._lt;
    var utils = require('web.utils');
    var Mutex = utils.Mutex;
    var Backbone = window.Backbone;

    pos_chrome.Chrome.include({
        build_widgets: function () {
            this._super();
            var old_widgets = this.widgets;
            var new_widget = {}
            _.each(old_widgets, function(line){
                if(line.name != 'printer_status'){
                    new_widget[line.name] = old_widgets[line.name];
                    console.log(line.name)
                }
            });
            this.widgets = new_widget;
        },
    });
});

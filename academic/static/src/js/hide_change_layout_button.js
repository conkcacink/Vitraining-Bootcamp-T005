odoo.define('academic.hide_change_layout_button', function (require) {
    "use strict";

    var view_registry = require('web.view_registry');
    var ListView = require('web.ListView');

    // Override ListView to hide the Change Layout button
    ListView.include({
        start: function () {
            this._super.apply(this, arguments);
            var toolbar = this.$el.find('.o_cp_switch');
            if (toolbar.length) {
                toolbar.hide();  // Hide the "Change Layout" button
            }
        },
    });
});

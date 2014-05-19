;

var Syops = function () {
    'use strict';

    var self = this,
        methods = {},
        listeners = {};

    /**
     * Constructor
     */
    methods.init = function () {
        $.ajaxSetup({
            cache: false,
            dataType: 'json'
        })
    };

    /**
     * Confirm dialog
     */
    this.confirm = function (settings) {
        var options = {
            title: 'Are you sure?',
            body: '',
            primary_label: 'Save',
            primary_callback: function () {},
            secondary_label: 'Cancel',
            secondary_callback: function () {},
        };
        options = $.extend({}, options, settings);
        $('#confirm-modal')
            .find('.modal-title')
                .text(options.title).end()
            .find('.modal-body')
                .text(options.body).end()
            .find('.modal-footer .btn-default')
                .text(options.secondary_label)
                .off('click')
                .on('click', options.secondary_callback).end()
            .find('.modal-footer .btn-primary')
                .text(options.primary_label)
                .off('click')
                .on('click', options.primary_callback).end()
            .modal();
    }

    /**
     * Catastrophic alerts
     */
    this.alert = function (message, style) {
        $('#alert').removeClass(function (index, css) {
            return (css.match(/\bbg-\S+/g) || []).join(' ');
        }).addClass('bg-' + style).text(message).fadeIn();
    };

    /**
     * App entry
     */
    this.dispatch = function () {
        methods.init()

        // Add basic listeners
        $.each(listeners, function (index, func) {
            func();
        });

        // Dispatch each module
        $.each (self.modules, function (index, Module) {
            self.modules[index] = new Module(self);
            self.modules[index].dispatch();
        });
    };
};
Syops.prototype.modules = {};

$(document).ready(function () {
    var app = new Syops();
    app.dispatch();
});

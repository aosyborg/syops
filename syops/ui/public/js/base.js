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
        // Add user popover
        $('#sidebar-user img, #sidebar-user .name').popover({
            placement: 'bottom',
            html: true,
            content: $('#sidebar-user .popover-content').html()
        });
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
        var close = '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>';
        $('#alert').attr('class', 'bg-' + style).html(message + close).fadeIn();
    };

    /**
     * Shows the modal to add an organization
     */
    methods.show_add_org_modal = function (event) {
        var modal = $('#add-organization');
        $.ajax({
            url: '/v1/team/list_orgs',
            beforeSend: function () {
                modal.modal('show');
            },
            success: function (orgs) {
                console.log(orgs);
            }
        });
    };

    /**
     * Listeners: Add organization
     */
    listeners.add_organization = function () {
        $('#sidebar-user').on('click', '#add-org', methods.show_add_org_modal);
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

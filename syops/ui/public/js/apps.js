;

Syops = Syops || {};
Syops.prototype.modules.apps = function (base) {
    'use strict';

    var self = this,
        constants = {},
        methods = {},
        listeners = {};

    /**
     * Constructor
     */
    methods.init = function () {
        constants.GITHUB_API = 'https://api.github.com';
        // Open menu
        $('#sidebar a.active').closest('div').find('ul:first').addClass('in');
    };

    /**
     * Populates branch select
     */
    methods.populate_branches = function () {
        var app_id = $('.content-wrapper').data('app-id');
        $.ajax({
            url: '/v1/app/list_branches',
            type: 'get',
            data: {app_id: app_id},
            success: function (branches) {
                var html = '';
                $.each(branches, function (index, branch) {
                    html += '<option name="'+branch.name+'">'+branch.name+'</option>';
                });
                $('#release-branch').html(html);
            }
        });
    }

    /**
     * Creates a new release
     */
    methods.create_release = function (form) {
        $.ajax({
            url: '/v1/app/new_release',
            type: 'post',
            data: form.serialize(),
            success: function (response) {
                console.log(response)
            },
            error: function () {
                base.alert('Error creating release.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Saves app edits
     */
    methods.save_edit = function (form) {
        $.ajax({
            url: '/v1/app/edit',
            type: 'post',
            data: form.serialize(),
            beforeSave: function () {
                $('#save-edit-btn').before('<img src="/public/img/ajax-loader.gif" />');
            },
            success: function (response) {
                var app_id = form.find('input[name="id"]').val();
                window.location = "/apps?id=" + app_id;
            },
            error: function () {
                base.alert('Error saving edit.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Listeners
     */
    listeners.releases = function () {
        // New release modal
        $('#new-release-btn').on('click', function (event) {
            methods.populate_branches();
            $('#edit-release')
                .find('.modal-title').text('New Release').end()
                .modal();
        });
        // Create a release
        $('#edit-release-save').on('click', function(event) {
            methods.create_release($(this).closest('.modal-content').find('form'));
        });
    };
    listeners.edit = function () {
        // Save edits
        $('#save-edit-btn').on('click', function (event) {
            methods.save_edit($('.content-wrapper form'));
        });
    };

    /**
     * Entry point
     */
    this.dispatch = function () {
        methods.init();

        // Add basic listeners
        $.each(listeners, function (index, func) {
            func();
        });
    };
};

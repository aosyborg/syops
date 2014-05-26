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
                $('#tagged-branch').html(html);
            }
        });
    }

    /**
     * Creates a new release
     */
    methods.create_release = function (form) {
        var app_id = $('.content-wrapper').data('app-id');
        $.ajax({
            url: '/v1/app/new_release',
            type: 'post',
            data: form.serialize(),
            success: function (response) {
                window.location = "/apps?id=" + app_id;
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
     * Releases an application to production
     */
    methods.release_app = function (release_id) {
        $.ajax({
            url: '/v1/app/release',
            type: 'post',
            data: {release_id: release_id},
            success: function (response) {
                location.reload();
            },
            error: function () {
                base.alert('Error releasing application.', 'danger');
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
        // Release to prod
        $('.release-to-prod').on('click', function (event) {
            var row = $(this).closest('tr'),
                id = row.find('.release-id').text(),
                version = row.find('.release-version').text();
            base.confirm({
                title: 'Release to production',
                body: 'Are you sure you want to release '+
                      '<strong>v' + version + '</strong> to production?',
                primary_label: 'Release',
                primary_callback: $.proxy(methods.release_app, self, id)
            });
        });
    };
    listeners.edit = function () {
        // Build instructions popover
        $('i.octicon-question').popover({
            html: true,
            content: function () {
                var html = $(this).siblings('.popover').html();
                return html;
            }
        });
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

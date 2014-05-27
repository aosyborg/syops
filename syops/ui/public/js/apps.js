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

        // Ensure version is of correct format
        if (!/^\d+\.\d+\-\d+$/.test(form.find('#release-version').val())) {
            form.find('#release-version').closest('.form-group').addClass('has-error');
            return;
        }

        $.ajax({
            url: '/v1/app/new_release',
            type: 'post',
            data: form.serialize(),
            beforeSend: function () {
                form.find('.form-group').removeClass('has-error');
                $('#edit-release').modal('hide');
            },
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
            beforeSend: function () {
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
     * Loads build output (console) modal
     */
    methods.show_console = function (event) {
        var modal = $('#build-output'),
            release_id = $(this).data('release-id');
        console.log(this, release_id);
        $.ajax({
            url: '/v1/app/console',
            type: 'get',
            dataType: 'text',
            data: {release_id: release_id},
            beforeSend: function () {
                modal.modal('show');
            },
            success: function (response) {
                console.log('got here!');
                modal.find('pre').html(response);
            },
            complete: function () {
                console.log('in complete!');
            }
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
            var last_release_row = $('.content-wrapper table tr:nth-child(2)'),
                last_release_in_prod = /prod/i.test(last_release_row.find('.release-status').text()),
                last_release_version = last_release_row.find('.release-version').text(),
                next_version = last_release_version;
            methods.populate_branches();

            // Figure out next version
            if (last_release_in_prod) {
                next_version = last_release_version.replace(/(\d+)\.(\d+)\-\d+/,
                    function (fullMatch, major, minor) {
                        return major + '.' + (+minor + 1) + '-0';
                    }
                );
            } else {
                next_version = last_release_version.replace(/(\d+)\.(\d+)\-(\d+)/,
                    function (fullMatch, major, minor, revision) {
                        return major + '.' + minor + '-' + (+revision + 1);
                    }
                );
            }

            // Update modal
            $('#edit-release')
                .find('.modal-title').text('New Release').end()
                .find('#release-version').val(next_version).end()
                .modal();
        });
        // Create a release
        $('#edit-release-save').on('click', function(event) {
            methods.create_release($(this).closest('.modal-content').find('form'));
        });
        // Console
        $('.release-console i').on('click', methods.show_console);
        // Release to prod
        $('.release-to-prod').on('click', function (event) {
            var row = $(this).closest('tr'),
                id = row.attr('id').replace(/[^\d]/g, ''),
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

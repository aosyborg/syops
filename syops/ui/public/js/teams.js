;

Syops = Syops || {};
Syops.prototype.modules.teams = function (base) {
    'use strict';

    var self = this,
        methods = {},
        listeners = {};

    /**
     * Constructor
     */
    methods.init = function () {
        // Open menu
        $('#sidebar a.active').closest('div').find('ul:first').addClass('in');
    };

    /**
     * Saves an app edit (new or modification)
     */
    methods.save_app_form = function (form) {
        var repo = form.find('#repo-list option:selected');
        $.ajax({
            url: '/v1/app/edit',
            type: 'post',
            dataType: 'json',
            data: {
                team_id: form.find('input[name="team_id"]').val(),
                name: repo.data('name'),
                clone_url: repo.data('clone_url'),
                github_owner: repo.data('owner'),
                github_repo: repo.data('name'),
            },
            success: function (response) {
                var html = '<tr id="app-'+response.id+'">' +
                    '<td class="app-id">'+response.id+'</td>' +
                    '<td class="app-name">'+response.name+'</td>' +
                    '<td class="app-clone-url">'+response.clone_url+'</td>' +
                    '<td class="app-created">'+response.insert_ts+'</td>' +
                    '<td><a href="#" class="app-delete">X</a></td>' +
                '</tr>';
                $('#content table').append(html);
            },
            error: function () {
                base.alert('Error saving applicaiton.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Deletes an app
     */
    methods.delete_app = function (app_id) {
        $.ajax({
            url: '/v1/app/delete',
            type: 'post',
            data: {app_id: app_id},
            success: function (response) {
                if (response !== true) {
                    base.alert('Error deleting application.', 'danger');
                    return;
                }
                $('#app-' + app_id).fadeOut('fast', function () {
                    $(this).remove();
                });
            },
            error: function () {
                base.alert('Error deleting application.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Queries for list of repos and displays them in modal
     */
    methods.open_new_app_modal = function (event) {
        var modal = $('#edit-app');
        $.ajax({
            url: '/v1/team/list_repos',
            beforeSend: function () {
                modal.modal();
            },
            success: function (repos) {
                var html = '';
                $.each(repos, function (index, repo) {
                    html += '' +
                        '<option data-name="'+repo.name+'" '+
                                'data-owner="'+repo.owner.login+'" '+
                                'data-clone_url="'+repo.ssh_url+'"> '+
                                repo.name
                        '</option>';
                });
                $('#repo-list').html(html);
            }
        });
    };

    /**
     * Listeners
     */
    listeners.manage_apps = function () {
        // New App
        $('#new-app-btn').on('click', methods.open_new_app_modal);
        // Save team edits
        $('#edit-app-save').on('click', function(event) {
            methods.save_app_form($(this).closest('.modal-content').find('form'));
        });
        // Delete app
        $('.content-wrapper table').on('click', '.app-delete', function (event) {
            event.preventDefault();
            var row = $(this).closest('tr'),
                app_id = row.find('.app-id').text(),
                app_name = row.find('.app-name').text();
            base.confirm({
                body: 'Are you sure you want to delete "' + app_name + '"? ' +
                      'This action cannot be undone!',
                primary_label: 'Delete',
                primary_callback: $.proxy(methods.delete_app, self, app_id)
            });
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

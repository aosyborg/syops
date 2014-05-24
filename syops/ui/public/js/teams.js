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
    methods.save_app_form = function (event) {
        event.preventDefault();
        var repo = $(this);
        $.ajax({
            url: '/v1/app/edit',
            type: 'post',
            dataType: 'json',
            data: {
                team_id: repo.closest('form').find('[name="team_id"]').val(),
                name: repo.data('name'),
                clone_url: repo.data('clone_url'),
                github_owner: repo.data('owner'),
                github_repo: repo.data('name'),
            },
            success: function (app) {
                window.location.href='/app/edit?id='+app.id
            },
            error: function () {
                base.alert('Error saving applicaiton.', 'danger');
            },
            complete: function () {
                repo.closest('.modal').modal('hide');
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
                location.reload();
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
        var modal = $('#edit-app').modal();
        $.ajax({
            url: '/v1/team/list_repos',
            data: {team_id:modal.find('[name="team_id"]').val()},
            success: function (repos) {
                var html = '';
                $.each(repos, function (index, repo) {
                    html += '' +
                        '<div class="list-group">'+
                            '<a href="#" class="list-group-item"' +
                                'data-name="'+repo.name+'" '+
                                'data-owner="'+repo.owner.login+'" '+
                                /**
                                 *
                                 */
                                'data-clone_url="'+repo.clone_url+'"> '+
                                '<div class="row">'+
                                    '<div class="col-md-1">'+
                                        '<i class="mega-octicon octicon-repo"></i>'+
                                    '</div>'+
                                    '<div class="col-md-11">'+
                                        '<strong>'+repo.name+'</strong>'+
                                        '<p class="list-group-item-text">'+repo.description+'</p>'+
                                        '<div class="text-muted">Last updated '+repo.updated_at+'</div>'+
                                    '</div>'+
                                '</div>'+
                            '</a>'+
                        '</div>';
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
        $('#edit-app .list-group').on('click', '.list-group-item', methods.save_app_form);
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

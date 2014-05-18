;

Syops = Syops || {};
Syops.prototype.modules.admin = function (base) {
    'use strict';

    var self = this,
        methods = {},
        listeners = {};

    /**
     * Constructor
     */
    methods.init = function () {
    };

    /**
     * Saves a team edit (new or modification)
     */
    methods.save_team_form = function (form) {
        $.ajax({
            url: '/v1/admin/team/edit',
            type: 'post',
            dataType: 'json',
            data: form.serialize(),
            success: function (response) {
                var html = '<tr id="team-'+response.id+'">' +
                    '<td class="team-id">'+response.id+'</td>' +
                    '<td class="team-name">'+response.name+'</td>' +
                    '<td class="team-owner"></td>' +
                    '<td class="team-member-count"></td>' +
                    '<td class="team-created">'+response.insert_ts+'</td>' +
                    '<td><a href="#" class="team-delete">X</a></td>' +
                '</tr>';
                $('#content table').append(html);
            },
            error: function () {
                base.alert('Error saving team.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Deletes a team
     */
    methods.delete_team = function (team_id) {
        $.ajax({
            url: '/v1/admin/team/delete',
            type: 'post',
            dataType: 'json',
            data: {team_id: team_id},
            success: function (response) {
                if (response !== true) {
                    base.alert('Error deleting team.', 'danger');
                    return;
                }
                $('#team-' + team_id).fadeOut('fast', function () {
                    $(this).remove();
                });
            },
            error: function () {
                base.alert('Error deleting team.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Saves a user edit (new or modification)
     */
    methods.save_user_form = function (form) {
        $.ajax({
            url: '/v1/admin/user/edit',
            type: 'post',
            dataType: 'json',
            data: form.serialize(),
            success: function (response) {
                var html = '<tr id="user-'+response.id+'">' +
                    '<td class="user-id">'+response.id+'</td>' +
                    '<td class="user-name">'+response.name+'</td>' +
                    '<td class="user-email">'+response.email+'</td>' +
                    '<td class="user-is-admin">'+response.is_admin+'</td>' +
                    '<td class="user-created">'+response.insert_ts+'</td>' +
                '</tr>';
                $('#content table').append(html);
            },
            error: function () {
                base.alert('Error saving user.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Deletes a user
     */
    methods.delete_user = function (user_id) {
        $.ajax({
            url: '/v1/admin/user/delete',
            type: 'post',
            dataType: 'json',
            data: {user_id: user_id},
            success: function (response) {
                if (response !== true) {
                    base.alert('Error deleting user.', 'danger');
                    return;
                }
                $('#user-' + user_id).fadeOut('fast', function () {
                    $(this).remove();
                });
            },
            error: function () {
                base.alert('Error deleting user.', 'danger');
            },
            complete: function () {
            },
        });
    };

    /**
     * Listeners
     */
    listeners.manage_teams = function () {
        // New Team
        $('#new-team-btn').on('click', function (event) {
            $('#edit-team')
                .find('.modal-title').text('New Team').end()
                .find('input').val('').end()
                .modal();
        });
        // Save team edits
        $('#edit-team-save').on('click', function(event) {
            methods.save_team_form($(this).closest('.modal-content').find('form'));
        });
        // Delete team
        $('.team-delete').on('click', function (event) {
            event.preventDefault();
            var row = $(this).closest('tr'),
                team_id = row.find('.team-id').text(),
                team_name = row.find('.team-name').text();
            base.confirm({
                body: 'Are you sure you want to delete "' + team_name + '"? ' +
                      'This action cannot be undone!',
                primary_label: 'Delete',
                primary_callback: $.proxy(methods.delete_team, self, team_id)
            });
        });
    };
    listeners.manage_users = function () {
        // New user
        $('#new-user-btn').on('click', function (event) {
            $('#edit-user')
                .find('.modal-title').text('New User').end()
                .find('input').val('').end()
                .modal();
        });
        // Save user edits
        $('#edit-user-save').on('click', function(event) {
            methods.save_user_form($(this).closest('.modal-content').find('form'));
        });
        // Delete user
        $('.user-delete').on('click', function (event) {
            event.preventDefault();
            var row = $(this).closest('tr'),
                user_id = row.find('.user-id').text(),
                user_name = row.find('.user-name').text();
            base.confirm({
                body: 'Are you sure you want to delete "' + user_name + '"? ' +
                      'This action cannot be undone!',
                primary_label: 'Delete',
                primary_callback: $.proxy(methods.delete_user, self, user_id)
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

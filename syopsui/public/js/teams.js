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
        console.log('got here');
    };

    /**
     * Saves an app edit (new or modification)
     */
    methods.save_app_form = function (form) {
        $.ajax({
            url: '/v1/app/edit',
            type: 'post',
            dataType: 'json',
            data: form.serialize(),
            success: function (response) {
                var html = '<tr id="app-'+response.id+'">' +
                    '<td class="app-id">'+response.id+'</td>' +
                    '<td class="app-name">'+response.name+'</td>' +
                    '<td class="app-clone-url">'+response.clone_url+'</td>' +
                    '<td class="app-github-owner">'+response.github_owner+'</td>' +
                    '<td class="app-github-repo">'+response.github_repo+'</td>' +
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
            dataType: 'json',
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
     * Listeners
     */
    listeners.manage_apps = function () {
        // New App
        $('#new-app-btn').on('click', function (event) {
            $('#edit-app')
                .find('.modal-title').text('New Application').end()
                .find('input[type!="hidden"]').end()
                .modal();
        });
        // Populate owner and repo fields from repo url
        $('#app-clone-url').on('blur', function (event) {
            var url = $(this).val(),
                owner = $('#app-owner'),
                repo = $('#app-repo'),
                inferred_owner = url.replace(/.*:([a-z]+).*/i, '$1'),
                inferred_repo = url.replace(/.*\/([a-z]+).git.*/i, '$1');

            if (owner.val() === '' && repo.val() === '' && inferred_owner !== '' && inferred_repo !== '') {
                owner.val(inferred_owner);
                repo.val(inferred_repo);
            }
        });
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

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
        var wrapper = $('.content-wrapper'),
            owner = wrapper.data('github-owner'),
            repo = wrapper.data('github-repo');
        $.ajax({
            url: constants.GITHUB_API + '/repos/'+owner+'/'+repo+'/branches',
            type: 'get',
            dataType: 'json',
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
            dataType: 'json',
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

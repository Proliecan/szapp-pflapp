/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        create: function (name) {
            let ajax_options = {
                type: 'POST',
                url: 'api/plants',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'name': name
                })
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_create_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                })
        },
    };
}());

// Create the view instance
ns.view = (function () {
    'use strict';

    // let $name = $('#name');

    // return the API
    return {
        reset: function () {
            // $lname.val('');
            // $fname.val('').focus();
        },
        update_editor: function (fname, lname) {
            // $lname.val(lname);
            // $fname.val(fname).focus();
        },
        error: function (error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function () {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body');

    // Get the data from the model after the controller is done initializing

    // Validate input
    function validate(fname, lname) {
        return fname !== "" && lname !== "";
    }

    // Create our event handlers
    $('#create').click(function (e) {
        let fname = $fname.val(),
            lname = $lname.val();

        e.preventDefault();

        if (validate(fname, lname)) {
            model.create(fname, lname)
        } else {
            alert('Problem with first or last name input');
        }
    });

    // Handle the model events
    $event_pump.on('model_create_success', function (e, data) {
        model.read();
    });

    $event_pump.on('model_error', function (e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
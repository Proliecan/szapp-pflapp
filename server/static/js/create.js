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
        create: function (name, min_fill_value, max_fill_value, img_file) {
            let ajax_options = {
                type: 'POST',
                url: 'api/plants',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'name': name,
                    'image_file': img_file, 
                    'min_fill_value': min_fill_value, 
                    'max_fill_value': max_fill_value
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

// Create the controller
ns.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $p_name = $('#p_name'),
        $p_max_fill_value = $('#p_max_fill_value'),
        $p_min_fill_value = $('#p_min_fill_value'),
        $p_img_file = $('#p_img_file');

    // Validate input
    function validate(name) {
        return name !== "";
    }

    // Create our event handlers
    $('#create').click(function (e) {
        let name = $p_name.val(),
            max_fill_value = parseInt($p_max_fill_value.val()),
            min_fill_value = parseInt($p_min_fill_value.val()),
            img_file = $p_img_file.val();
        e.preventDefault();

        if (validate(name)) {
            model.create(name, min_fill_value, max_fill_value, img_file);
        } else {
            alert('No Name was given.');
        }
    });

    // Handle the model events
    $event_pump.on('model_create_success', function (e, data) {
        window.location = "/main_page";
    });

    $event_pump.on('model_error', function (e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
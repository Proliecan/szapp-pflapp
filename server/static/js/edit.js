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
        'read_one': function (plant_id) {
            let ajax_options = {
                type: 'GET',
                url: '../../api/plant/' + plant_id,
                accept: 'application/json',
                contentType: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_read_one_success', data);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                })
        },
        update: function (plant_id, name, min_fill_value, max_fill_value, img_file) {
            let ajax_options = {
                type: 'PUT',
                url: '../../api/plant/' + plant_id,
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
                    $event_pump.trigger('model_update_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                })
        }
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

        },
        build_one_div: function (plant) {
            if (plant) {
                console.log(plant);
                let date = new Date(plant.creation_date);
                let div =
                `<div>
                    <div>
                        <h2>${plant.name}</h2>
                        <img src="../../${plant.image_file}" alt="Image" loading="lazy" style="height: 50vh;">
                        <div id="creation">You kept ${plant.name} alive since ${date.toLocaleDateString()}!</div>       </div>
                </div>`;
                $('#tg-0pky').append(div);
            }
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
        $event_pump = $('body'),
        plant_id = document.getElementById('plant_id_field'),
        $p_name = $('#p_name'),
        $p_max_fill_value = $('#p_max_fill_value'),
        $p_min_fill_value = $('#p_min_fill_value'),
        $p_img_file = $('#p_img_file');;

    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        model.read_one(parseInt(plant_id.textContent));
    }, 100)

    // Validate input
    function validate(name) {
        return name !== "";
    }

    $('#update').click(function (e) {
        let name = $p_name.val(),
            max_fill_value = parseInt($p_max_fill_value.val()),
            min_fill_value = parseInt($p_min_fill_value.val()),
            img_file = $p_img_file.val();

        e.preventDefault();

        if (validate(name)) {
            model.update(parseInt(plant_id.textContent), name, min_fill_value, max_fill_value, img_file);
        } else {
            alert('No Name was given.');
        }
    });

    $('#reset').click(function () {
        view.reset();
    })

    // Handle the model events
    $event_pump.on('model_read_one_success', function (e, data) {
        view.build_one_div(data);
        view.reset();
    });

    $event_pump.on('model_update_success', function (e, data) {
        window.location = "/plant/" + parseInt(plant_id.textContent);
    });

    $event_pump.on('model_error', function (e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
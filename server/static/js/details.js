/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns_ = {};

// Create the model instance
ns_.model = (function () {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read_one': function (plant_id) {
            console.log(plant_id);
            let ajax_options = {
                type: 'GET',
                url: '../api/plant/' + plant_id,
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
        'delete': function (plant_id) {
            let ajax_options = {
                type: 'DELETE',
                url: '../api/plant/' + plant_id,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_delete_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                })
        }
    };
}());

// Create the view instance
ns_.view = (function () {
    'use strict';

    // return the API
    return {
        build_one_div: function (plant) {
            if (plant) {
                let date = new Date(plant.creation_date);
                let div =
                    `<div class="details">
                    <div>
                        <h2>${plant.name}</h2>
                        <img src="../${plant.image_file}" alt="Image" loading="lazy">
                        <div id="creation">You kept ${plant.name} alive since ${date.toLocaleDateString()}!</div>`
                div +=
                    `       </div>
                </div>`;
                $('#p_container').append(div);

                // prepare data for graph
                const dateformat_options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'};

                let water_values = plant.values;
                let labels_ = [];
                let data_values = [];
                for (let i = 0; i < water_values.length; i++) {
                    let date = new Date(water_values[i].report_time);

                    labels_.push(date.toLocaleDateString("de-DE", dateformat_options));

                    data_values.push(water_values[i].value);
                }
                console.log(labels_.length, data_values);

                // build graph

                const data = {
                    labels: labels_,
                    datasets: [{
                        label: 'Water level',
                        backgroundColor: 'rgb(169, 186, 90)',
                        borderColor: 'rgb(32, 69, 144)',
                        color: '#000',
                        data: data_values,
                        fill: false,
                        tension: 0.3,
                    }]
                };
                const config = {
                    type: 'line',
                    data: data,
                    options: {
                        layout: {
                            padding: 20
                        }
                    }
                };

                const water_level_graph = new Chart(
                    document.getElementById('water_level_graph'),
                    config
                );
            }
            return false;
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
ns_.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        plant_id = document.getElementById('plant_id_field');

    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        model.read_one(parseInt(plant_id.textContent));
    }, 10);

    // Validate input
    function validate(name) {
        return name !== "";
    }

    $('#update').click(function (e) {
        e.preventDefault();

        window.location = "/plant/" + parseInt(plant_id.textContent) + "/edit_plant";
    });

    $('#delete').click(function (e) {
        e.preventDefault();
        model.delete(parseInt(plant_id.textContent));
        e.preventDefault();
    });

    // Handle the model events
    $event_pump.on('model_read_one_success', function (e, data) {
        view.build_one_div(data);
        // view.reset();
        e.preventDefault();
    });

    $event_pump.on('model_delete_success', function (e, data) {
        window.location = "/main_page";
    });

    $event_pump.on('model_error', function (e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns_.model, ns_.view));
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
        'read': function () {
            let ajax_options = {
                type: 'GET',
                url: 'api/plants',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_read_success', [data]);
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
        build_divs: function (plants) {
            let divs = ''
            if (plants) {
                for (let i = 0, l = plants.length; i < l; i++) {
                    let date = new Date(plants[i].creation_date);
                    let water_value;
                    let dryWaterLevel = (plants[i].max_fill_value - plants[i].min_fill_value) * 0.3;
                    let additionalClass = '';
                    if (typeof plants[i].values[0] !== 'undefined') {
                        water_value = plants[i].values[0].value;
                        if (water_value <= dryWaterLevel) {
                            additionalClass = ' dry'
                        }
                    } else {
                        water_value = '';
                    }
                    divs += `
                        <a href="/plant/${plants[i].id}" class="plant${additionalClass} wave">
                            <ol>
                                <li>${plants[i].name}</li>
                                <li><img src="../${plants[i].image_file}" alt="Image" loading="lazy"></li>
                                <li>Creation Date: ${date.toLocaleDateString()}</li>
                                <li>${water_value}</li>
                            </ol>
                        </a>`;
                }
                $('#plants_container').prepend(divs);
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
        $event_pump = $('body');

    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        model.read();
    }, 10)

    // Handle the model events
    $event_pump.on('model_read_success', function (e, data) {
        view.build_divs(data);
        view.reset();
    });

    $event_pump.on('model_error', function (e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
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
                .fail(function (xhr, textStatus, errorThrown){
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                })
        },
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
        update: function (fname, lname) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/people/' + lname,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'fname': fname,
                    'lname': lname
                })
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_update_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                })
        },
        'delete': function (lname) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/people/' + lname,
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
        build_one_div: function (plant) {
            if (plant) {
                console.log(plant);
                let date = new Date(plant.creation_date);
                let table = `<table><tr><th>Report Time</th><th>Value</th></tr>`;
                for (let i = 0, l = plant.values.length; i < l; i ++) {
                    let date = new Date(plant.values[i].report_time);
                    table += `<tr><td>${date.toLocaleDateString()}</td><td>${plant.values[i].value}</td>`
                }
                table += `</tr></table>`;
                let div = 
                `<div class="plant">
                    <ol>
                        <li>Name: ${plant.name}</li>
                        <li><img src="../${plant.image_file}" alt="Image" loading="lazy"></li>
                        <li>Creation Date: ${date.toLocaleDateString()}</li>
                        <li id="table">${table}</li>
                    </ol>
                </div>`;
                $('body').append(div);
            }
        },
        build_divs: function (plants) { 
            let divs = ''

            // did we get a plants array?
            if (plants) {
                for (let i = 0, l = plants.length; i < l; i++) {
                    let date = new Date(plants[i].creation_date);
                    divs += `
                        <div class="plant">
                            <ol>
                                <li>Name: ${plants[i].name}</li>
                                <li><img src="../${plants[i].image_file}" alt="Image" loading="lazy"></li>
                                <li>Creation Date: ${date.toLocaleDateString()}</li>
                                <li>${plants[i].values[0].value}</li>
                                <li><a href="/plant/${plants[i].id}">DETAILS</a></li>
                            </ol>
                        </div>`;
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
        $event_pump = $('body'),
        plant_id = document.getElementById('plant_id_field');

    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        model.read_one(parseInt(plant_id.textContent));
    }, 100)

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

    $('#update').click(function (e) {
        let fname = $fname.val(),
            lname = $lname.val();

        e.preventDefault();

        if (validate(fname, lname)) {
            model.update(fname, lname)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function (e) {
        let lname = $lname.val();

        e.preventDefault();

        if (validate('placeholder', lname)) {
            model.delete(lname)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function () {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function (e) {
        let $target = $(e.target),
            fname,
            lname;

        fname = $target
            .parent()
            .find('td.fname')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        view.update_editor(fname, lname);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function (e, data) {
        view.build_divs(data);
        view.reset();
    });

    $event_pump.on('model_read_one_success', function (e, data) {
        view.build_one_div(data);
        view.reset();
    });


    $event_pump.on('model_create_success', function (e, data) {
        model.read_one();
    });

    $event_pump.on('model_update_success', function (e, data) {
        model.read_one();
    });

    $event_pump.on('model_delete_success', function (e, data) {
        model.read_one();
    });

    $event_pump.on('model_error', function (e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
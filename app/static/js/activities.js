var calendar;

function addEvent(id) {
    fetch(url_for_get_events, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            Nome: document.getElementById(id+'Nome').value,
            Descrizione: document.getElementById(id+'Descrizione').value,
            Posti: document.getElementById(id+'Posti').value
        })
    })
    .then(response => statusResponse(response));
}

function createOptionEvent() {
    let empty_row = document.querySelector('#table-body_events .empty_row');
    let id = 'new-event_';
    empty_row.innerHTML = '';
    empty_row.className = '';

    cell = empty_row.insertCell();
    cell.innerHTML = 'nuovo evento';
    cell = empty_row.insertCell();
    let input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Nome';
    input.maxLength = 50;
    input.id = id+'Nome';
    cell.appendChild(input);
    cell = empty_row.insertCell();
    input = document.createElement('input');
    input.type = 'textarea';
    input.placeholder = 'Descrizione';
    input.maxLength = 200;
    input.id = id+'Descrizione';
    cell.appendChild(input);
    cell = empty_row.insertCell();
    input = document.createElement('input');
    input.type = 'number';
    input.placeholder = 'Posti Massimi';
    input.oninput = function() { acceptInteger(this) };
    input.id = id+'Posti';
    cell.appendChild(input);
    cell = empty_row.insertCell();
    cell.innerHTML = '<button class="save" onclick="addEvent(\''+id+'\')">s</button>';
}

function deleteEvent(id) {
    fetch(url_for_get_events + '?IdAttivita=' + id, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}

function addSchedule(id, nome, datePart) {
    let dict_schedule = {
        IdAttivita: id,
        Data: datePart,
        Inizio: document.getElementById('modal_event-start').value,
        Fine: document.getElementById('modal_event-end').value
    }

    console.log(dict_schedule);

    fetch(url_for_get_schedules, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dict_schedule)
    })
    .then(response => calendarProgrammazioni(id, nome));
}

function calendarProgrammazioni(id, nome) {
    document.querySelector('.modal#modal_event').style.display = 'block';
    
    
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'prev next',
        center: 'title',
        right: 'selectedEvent'
        },
        customButtons: {
            selectedEvent: {
                text: nome,
                click: function() {
                    let form = document.createElement('div');
                    form.id = 'modal_event-form';
                    form.className = 'custom-form';
                    form.innerHTML = 'inserisci gli orari e seleziona un giorno!'
                    let div = document.createElement('div');
                    let label = document.createElement('label');
                    label.innerHTML = 'Inizio';
                    let input = document.createElement('input');
                    input.type = 'time';
                    input.id = 'modal_event-start';
                    label.appendChild(input);
                    div.appendChild(label);
                    form.appendChild(div);

                    label = document.createElement('label');
                    label.innerHTML = 'Fine';
                    input = document.createElement('input');
                    input.type = 'time';
                    input.id = 'modal_event-end';
                    label.appendChild(input);
                    div.appendChild(label);
                    form.appendChild(div);

                    if(!document.querySelector('#modal_event-form') ) {
                        var toolbarCenter = document.querySelector('.fc-header-toolbar.fc-toolbar.fc-toolbar-ltr');
                        toolbarCenter.parentElement.insertBefore(form, toolbarCenter.parentElement.childNodes[1]);
                    } else {
                        document.querySelector('#modal_event-form').remove();
                    }
                }
            }
        },
    });
    calendar.render();

    calendar.on('dateClick', function(info) {
        addSchedule(id, nome, info.dateStr.split('T')[0]);
    });

    addEventsToCalendar(id);

    function addEventsToCalendar(id) {
        fetch(url_for_get_schedules + '?IdAttivita=' + id)
        .then(response => response.json())
        .then(data => {
            data.forEach(schedule => {
                const datePart = new Date(schedule.Data).toISOString().split('T')[0];
                calendar.addEvent({
                    start: new Date(`${datePart}T${schedule.Inizio}Z`),
                    end: new Date(`${datePart}T${schedule.Fine}Z`)
                });
            });
        });
    }  
}

function getEvents() {
    document.getElementById('table-body_events').innerHTML = '';

    emptyRow(document.getElementById('table-body_events'), 5, function() {createOptionEvent()});

    fetch(url_for_get_events)
    .then(response => response.json())
    .then(data => {
        data.forEach(event => {
            let row = document.createElement('tr');
            cell = document.createElement('td');
            cell.innerHTML = '<button class="delete" onclick="deleteEvent('+event.IdAttivita+')">x</button>';
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = event.Nome;
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = event.Descrizione;
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = event.Posti;
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = '<button onclick="calendarProgrammazioni(\''+event.IdAttivita+'\', \''+event.Nome+'\')">calendario</button>'
            row.appendChild(cell);
            document.getElementById('table-body_events').appendChild(row);
        });
    });
}

function modalRide() {
    document.querySelector('.modal#modal_ride').style.display = 'block';

    document.querySelector('#modal_ride-datalist_category').innerHTML = '';
    fetch(url_for_get_categories)
    .then(response => response.json())
    .then(data => { 
        data.forEach(category => {
            let option = document.createElement('option');
            option.setAttribute('value', category.Nome);
            option.setAttribute('IdCategoria', category.IdCategoria);
            document.querySelector('#modal_ride-datalist_category').appendChild(option);
        });
    });

    // function newOption() {
    //     let input = document.createElement('input');
    //     input.id = 'modal_ride-new_limit';
    //     input.type = 'text';
    //     input.placeholder = 'Nuovo Limite';
    //     /*
    //     devi farci stare:
    //      - Attributo: reflection(?)
    //      - Condizione
    //      - Descrizione
    //      - Valore str 
    //     */
        
    //     document.querySelector('#modal_ride-constraint_limits').appendChild(option);
    // }

    document.querySelector('#modal_ride-constraint_limits').innerHTML = '';
    // newOption();
    fetch(url_for_get_limits)
    .then(response => response.json())
    .then(data => {
        data.forEach(limit => {
            let limit_id = 'modal_ride-limit_'+limit.IdLimite;
            
            let li = document.createElement('li');
            let checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = limit_id;

            let label = document.createElement('label');
            label.htmlFor = limit_id;
            label.innerHTML = limit.Descrizione;
            
            li.appendChild(checkbox);
            li.appendChild(label);
            document.querySelector('#modal_ride-constraint_limits').appendChild(li);
        });
    });
}

function addRide() {    
    posti = document.querySelector('#modal_ride-total_seats').value;
    posti = !isNaN(posti) && posti<1 ? 1 : posti;

    let dict_limits = [];
    document.querySelectorAll('#modal_ride-constraint_limits input').forEach((checkbox) => {
        if (checkbox.checked) {
            dict_limits.push(checkbox.id.split('_')[2]);
        }
    });

    let dict_ride = {
        Nome: document.getElementById('modal_ride-name').value,
        Descrizione: document.getElementById('modal_ride-description').value,
        Posti: posti,
        Categoria: document.getElementById('modal_ride-category').value, 
        Limiti: dict_limits
    }
    
    console.log(dict_ride);
    fetch(url_for_get_rides, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dict_ride)
    })
    .then(response => statusResponse(response));
}

function deleteRide(id) {
    fetch(url_for_get_rides + '?IdAttivita=' + id, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}

function getRides() {
    let limit_id = document.getElementById('filter_limiti').value.split('_')[1] === undefined ? '' : document.getElementById('filter_limiti').value.split('_')[1];
    let url = url_for_get_rides + '?';
    url += 'category=' + encodeURIComponent(document.getElementById('filter_categorie').value) + '&';
    url += 'limit=' + limit_id + '&';
    url += 'tariff=' + encodeURIComponent(document.getElementById('filter_tariffe').value);
    
    document.querySelector('#table-body_rides').innerHTML = '';

    emptyRow(document.getElementById('table-body_rides'), 6, function() {modalRide()});

    fetch(url)
    .then(response => response.json())
    .then(data => {
        data.forEach(ride => {
            let row = document.createElement('tr');
            cell = document.createElement('td');
            cell.innerHTML = '<button class="delete" onclick="deleteRide('+ride.IdAttivita+')">x</button>';
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = ride.Nome;
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = ride.Descrizione;
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = ride.Posti;
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.innerHTML = ride.NomeCategoria;
            row.appendChild(cell);
            cell = document.createElement('td');
            let ul = document.createElement('ul');
            ride.Limiti.forEach(limit => {
                let li = document.createElement('li');
                li.innerHTML = limit.Descrizione;
                ul.appendChild(li);
            });
            cell.appendChild(ul);
            row.appendChild(cell);
            document.getElementById('table-body_rides').appendChild(row);
        });
    });
}

function filterRides() {
    // FILTERS
    
    // CATEGORIES
    document.getElementById('filter_categorie').innerHTML = '<option value="" selected>Tutte</option>';
    fetch(url_for_get_categories)
    .then(response => response.json())
    .then(data => {
        data.forEach(category => {
            document.getElementById('filter_categorie').innerHTML += '<option value="' + category.Nome + '">' + category.Nome + '</option>';
        });
    });

    // LIMITS
    document.getElementById('filter_limiti').innerHTML = '<option value="" selected>Qualsiasi</option><option value="limit_0">Nessuno</option>';
    fetch(url_for_get_limits)
    .then(response => response.json())
    .then(data => {
        data.forEach(limit => {
            document.getElementById('filter_limiti').innerHTML += '<option value="limit_'+limit.IdLimite+'">' + limit.Descrizione + '</option>';
        });
    });

    // TARIFFS
    document.getElementById('filter_tariffe').innerHTML = '<option value="" selected>Qualsiasi</option>';
    fetch(url_for_get_tariffs)
    .then(response => response.json())
    .then(data => {
        data.forEach(tariff => {
            document.getElementById('filter_tariffe').innerHTML += '<option value="' + tariff.NomeTariffa + '">' + tariff.NomeTariffa + '</option>';
        });
    });

    // AJAX
    document.querySelectorAll('#filter_menu select').forEach((select) => {
        select.addEventListener('change', function() {
            getRides();
        });
    });
}


function Ajax() {
    // change tables
    document.querySelectorAll('.choices .options [name="activity"]').forEach((radio) => {
        radio.addEventListener('click', function () {
            document.querySelectorAll('.choices .options [name="activity"]').forEach((radio) => {
                document.querySelector('#table_'+radio.id.split('_')[1]).parentElement.style.display = 'none';
            });
            document.querySelector('#table_'+radio.id.split('_')[1]).parentElement.style.display = '';
        });
    });

    getEvents();

    filterRides();
    getRides();
}

Ajax();


// add tables empty row QoL


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

function createOptionEvent(empty_row) {
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
    fetch(url_for_get_events + '?IdEvento=' + id, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}

function getEvents() {
    document.getElementById('table-body_events').innerHTML = '';
    // addEmptyRow('#table-body_events', addEvent, 'event');
    let empty_row = document.createElement('tr');
    empty_row.className = 'empty_row';
    let cell = document.createElement('td');
    cell.colSpan = 5;
    let button = document.createElement('button');
    button.classList.add('add');
    button.onclick = function() {createOptionEvent(empty_row)};
    button.innerHTML = '+';
    cell.appendChild(button);
    empty_row.appendChild(cell);
    document.getElementById('table-body_events').appendChild(empty_row);

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
            row.appendChild(cell);
            document.getElementById('table-body_events').appendChild(row);
        });
    });
}

function getRides() {
    let limit_id = document.getElementById('filter_limiti').value.split('_')[1] === undefined ? '' : document.getElementById('filter_limiti').value.split('_')[1];
    let url = url_for_get_rides + '?';
    url += 'category=' + document.getElementById('filter_categorie').value + '&';
    url += 'limit=' + limit_id + '&';
    url += 'tariff=' + document.getElementById('filter_tariffe').value;
    
    console.log(url);
    
    document.getElementById('table-body_rides').innerHTML = '';
    let empty_row = document.createElement('tr');
    empty_row.className = 'empty_row';
    let cell = document.createElement('td');
    cell.colSpan = 6;
    let button = document.createElement('button');
    button.classList.add('add');
    // button.onclick = function() {modalRide()};
    button.innerHTML = '+';
    cell.appendChild(button);
    empty_row.appendChild(cell);
    document.getElementById('table-body_rides').appendChild(empty_row);

    fetch(url)
    .then(response => response.json())
    .then(data => {
        data.forEach(ride => {
            let row = document.createElement('tr');
            cell = document.createElement('td');
            cell.innerHTML = '<button class="delete" onclick="deleteEvent('+ride.IdAttivita+')">x</button>';
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

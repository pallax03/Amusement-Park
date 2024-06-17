const giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica'];

function getTypes() {
    const select = document.getElementById('types');
    select.innerHTML = '';
    fetch(url_for_get_services_types)
    .then(response => response.json())
    .then(data => {
        let option = document.createElement('option');
        option.value = 'all';
        option.innerHTML = 'all';
        select.add(option);
        
        data.forEach(type => {
            let option = document.createElement('option');
            option.value = type;
            option.innerHTML = type;
            select.add(option);
        });
    });
}

function serviceCard(Service = {Nome: '', Tipo: '', Orario: {Lunedi: '', Martedi: '', Mercoledi: '', Giovedi: '', Venerdi: '', Sabato: '', Domenica: ''}}) {
    let card = document.createElement('div');
    card.classList.add('card');

    let header = document.createElement('div');
    header.classList.add('card-header');
    let nome = document.createElement('h4')
    nome.innerHTML = Service.Nome; 
    header.appendChild(nome);

    let body = document.createElement('div');
    body.classList.add('card-body');
    let tipo = document.createElement('p');
    tipo.innerHTML = Service.Tipo; 
    body.appendChild(tipo);
    
    let timetable = document.createElement('div');
    timetable.classList.add('card-footer');
    let orario = document.createElement('ul');
    let giorni = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica'];
    giorni.forEach(giorno => {
        let li = document.createElement('li');
        li.innerHTML = giorno + ': ' + Service.Orario[giorno];
        orario.appendChild(li);
    });
    
    timetable.appendChild(orario);
    
    card.appendChild(header);
    card.appendChild(body);
    card.appendChild(timetable);
    
    let button = document.createElement('button');
    button.classList.add('delete');
    button.onclick = function() {deleteService(Service.Nome)};
    button.innerHTML = 'x';
    card.appendChild(button);

    return card;
}

function getTimetables(select, orario) {
    fetch(url_for_get_timetables)
    .then(response => response.json())
    .then(data => {
        data.forEach(timetable => {
            // modificare attributi con i giorni della settimana
            // spostare viriabile days in globale e ciclare
            let option = document.createElement('option');
            for (let giorno of giorni) {
                option.setAttribute(giorno, timetable[giorno]);
            }
            option.value = timetable.IdOrario;
            option.innerHTML = timetable.IdOrario;
            select.add(option);
        });
        checkTimetable(select, orario);
    });
}

function checkTimetable(select, orario) {

    function changeOrario(select, orario) {
        selectedTimetable = null; 
        select.childNodes.forEach( option => {   
            if(selectedTimetable == null) {
                if (option.value == select.value) selectedTimetable = option;
            }
        });
        giorni.forEach(giorno => {
            let parse_time = selectedTimetable.getAttribute(giorno).split('-');
            let query = orario.querySelectorAll('#'+giorno+' + label input[type=time]');
            let input_inizio = query[0];
            input_inizio.value = parse_time[0];

            let input_fine = query[1];
            input_fine.value = parse_time[1];
        });
    }

    changeOrario(select, orario);

    select.onchange = function() {changeOrario(select, orario)}
}

function disableDay(giorno) {

    giorno.querySelectorAll('label input[type=time]').forEach(input => input.disabled = !input.disabled);
}

function createService() {
    let card = document.createElement('div');
    card.classList.add('card');

    let header = document.createElement('div');
    header.classList.add('card-header');
    let nome = document.createElement('input');
    nome.placeholder = 'Nome';
    header.appendChild(nome);

    let body = document.createElement('div');
    body.classList.add('card-body');
    let tipo = document.createElement('input');
    tipo.placeholder = 'Tipo';
    body.appendChild(tipo);
    
    let timetable = document.createElement('div');
    timetable.classList.add('card-footer');
    
    let select_timetable = document.createElement('select');
    timetable.appendChild(select_timetable);

    let orario = document.createElement('ul');
    giorni.forEach(giorno => {
        let li = document.createElement('li');

        let checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = true;
        checkbox.id = giorno;
        
        let label = document.createElement('label');
        label.innerHTML = giorno+': ';
        label.setAttribute('for', giorno);

        let input_inizio = document.createElement('input');
        input_inizio.className = 'inizio';
        input_inizio.type = 'time';

        let input_fine = document.createElement('input');
        input_fine.className = 'fine';
        input_fine.type = 'time';

        checkbox.onclick = function() {disableDay(li)};

        label.appendChild(input_inizio);
        label.innerHTML += ' - ';
        label.appendChild(input_fine);

        li.appendChild(checkbox);
        li.appendChild(label);
        orario.appendChild(li);
    });
    
    timetable.appendChild(orario);
    
    getTimetables(select_timetable, orario);

    card.appendChild(header);
    card.appendChild(body);
    card.appendChild(timetable);

    let services = document.getElementById('services');
    services.insertBefore(card, services.lastChild);

    

    changeAPIButton('#add_service', addService, '', 'save');
}

function getServices(type) {
    type = type === 'all' ? '' : '?Tipo='+type;

    const services = document.getElementById('services');
    services.innerHTML = '';
    fetch(url_for_get_services + type) 
    .then(response => response.json())
    .then(data => {
        data.forEach(service => {
            services.appendChild(serviceCard(service));
        });
        button = document.createElement('button');
        button.classList.add('add');
        button.id = 'add_service';
        button.onclick = function() {createService()};
        button.innerHTML = '+';
        services.appendChild(button);
        // dynamicEvents();
    });
}

function changeAPIButton(query, func, args, text) {
    document.querySelector(query).innerHTML = { 'add': '+', 'delete': 'x', 'save': 's' }[text];
    document.querySelector(query).className = text;
    document.querySelector(query).onclick = function() {func(args)};
}

function deleteService(nomeservizio) {
    fetch(url_for_add_service + "?Nome="+encodeURIComponent(nomeservizio), {
        method: 'DELETE'
    })
    .then(response => statusResponse(response))
    .then(data => getServices(document.getElementById('types').value));
}

function addService(args) {

    dict_orario = {};

    giorni.forEach(giorno => {
        if(document.getElementById(giorno).checked === false) {
            dict_orario[giorno] = ''; 
        } else {
            time = document.querySelectorAll('#'+giorno+' + label input[type=time]')
            dict_orario[giorno] = time[0].value+'-'+time[1].value;
        }
    });

    service = {
        Nome: document.querySelector('.card-header input').value,
        Tipo: document.querySelector('.card-body input').value,
        Orario: dict_orario
    };  

    fetch(url_for_add_service, {
        method: 'POST',
        body: JSON.stringify(service),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => statusResponse(response))
    .then(data => getServices(document.getElementById('types').value));
}

// //dynamicEvents
// function dynamicEvents() {
//     document.querySelectorAll('.card').forEach(card => card.addEventListener('click', function() {
//         document.querySelectorAll('.card').forEach(card => card.classList.remove('selected'));
//         card.classList.add('selected');
//         changeAPIButton('.cards button', deleteService, card.querySelector('.card-header h4').innerHTML, 'delete');
//         })
//     );
// }

getTypes();
getServices('all');
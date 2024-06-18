function getEntries(codicefiscale, dataingresso) {
    document.querySelector('#entries-data').innerHTML = '';
    fetch( url_for_get_entries + '?CodiceFiscale=' + codicefiscale)
    .then(response => response.json())
    .then(data => {
        data.forEach(function(entry) {
            let date = new Date(entry.Data).toLocaleDateString('en-CA') 
            let option = document.createElement('option');
            option.value = date;
            option.innerHTML = date;
            document.querySelector('#entries-data').appendChild(option);
        });
        if (dataingresso) {
            document.querySelector('#entries-data').value = new Date(dataingresso).toLocaleDateString('en-CA');
        }
        getPartecipates(document.querySelector('#entries-codicefiscale').value, document.querySelector('#entries-data').value);
    })
}

function addPartecipate(codicefiscale, dataingresso, ora, attivita) {
    fetch(url_for_add_partecipate, {
        method: 'POST',
        body: JSON.stringify({
            CodiceFiscale: codicefiscale.value,
            DataIngresso: dataingresso.value,
            Ora: ora.value,
            IdAttivita: attivita.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => statusResponse(response))
}

function createOptionPartecipate() {
    let empty_row = document.querySelector('#table_body-partecipates .empty_row');
    empty_row.innerHTML = '';
    empty_row.insertCell();
    
    let cell = empty_row.insertCell();   
    let ora = document.createElement('input');
    ora.type = 'time';
    ora.id = 'new-partecipate_ora';
    cell.appendChild(ora);

    cell = empty_row.insertCell();
    cell.colSpan = 2;
    let attivita = document.createElement('select');
    attivita.id = 'new-partecipate_attivita';
    cell.appendChild(attivita);

    fetch(url_for_get_activities)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.forEach(function(activity) {
            let option = document.createElement('option');
            option.value = activity.IdAttivita;
            option.setAttribute('posti', activity.Posti);
            option.setAttribute('IsEvent', activity.IsEvent);
            option.innerHTML = activity.IsEvent ? 'E' : 'A';
            option.innerHTML += ' | ' + activity.Nome;
            // if (activity.IsEvent) {
                   
            // }
            attivita.appendChild(option);
        });
    });
    
    cell = empty_row.insertCell();
    let save = document.createElement('button');
    save.classList.add('save');
    save.onclick = function() {addPartecipate(document.querySelector('#entries-codicefiscale'), document.querySelector('#entries-data'), document.querySelector('#new-partecipate_ora'), document.querySelector('#new-partecipate_attivita'))};
    save.innerHTML = 's';
    cell.appendChild(save);
}

function deletePartecipate(idingresso, ora) {
    fetch(url_for_add_partecipate + '?IdIngresso='+idingresso+'&Ora='+ora, {
        method: 'DELETE',
    })
    .then(response => statusResponse(response))
}

function getPartecipates(codicefiscale, dataingresso) {
    document.querySelector('#table-partecipates').style.display = '';
    document.querySelector('#table_body-partecipates').innerHTML = '';

    emptyRow(document.querySelector('#table_body-partecipates'), 5, function() {createOptionPartecipate()});

    fetch(url_for_get_partecipates + '?CodiceFiscale=' + codicefiscale + '&DataIngresso=' + dataingresso)
    .then(response => response.json())
    .then(data => {
        data.forEach(function(partecipate) {
            let row = document.querySelector('#table_body-partecipates').insertRow();
            
            let cell = row.insertCell();
            cell.innerHTML = '<button class="delete" onclick="deletePartecipate(\''+partecipate.IdIngresso+'\', \''+partecipate.Ora+'\')" >x</button>'; //button delete

            cell = row.insertCell();
            cell.innerHTML = partecipate.Ora;

            cell = row.insertCell();
            cell.innerHTML = partecipate.Attivita.Nome;

            cell = row.insertCell();
            cell.innerHTML = partecipate.PostiOccupati + ' / ' + partecipate.Attivita.Posti;

            cell = row.insertCell();
            cell.innerHTML = ''; // padding
        });
    });
}

function Ajax() {
    let codicefiscale = new URL(window.location.href).searchParams.get('CodiceFiscale');
    let dataingresso = new URL(window.location.href).searchParams.get('DataIngresso');
   
    if(codicefiscale) {
        document.querySelector('#entries-codicefiscale').value = codicefiscale;
        getEntries(codicefiscale, dataingresso);
    }
    document.querySelector('#entries-codicefiscale').addEventListener('change', function() {
        getEntries(this.value);
    }); 

    document.querySelector('#entries-data').addEventListener('change', function() {
        getPartecipates(document.querySelector('#entries-codicefiscale').value, document.querySelector('#entries-data').value);
    });
}

Ajax();
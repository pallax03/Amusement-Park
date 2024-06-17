function getEntries(codicefiscale) {
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
        getPartecipates(codicefiscale, document.querySelector('#entries-data').value);
    })
}

function createOptionPartecipate(empty_row) {
    empty_row.innerHTML = '';
    // let cell = empty_row.insertCell();
    // cell.colSpan = 2;
    // let select = document.createElement('select');
    // select.id = 'select-attivita';
    // cell.appendChild(select);
    // fetch(url_for_get_activities)
    // .then(response => response.json())
    // .then(data => {
    //     data.forEach(function(activity) {
    //         let option = document.createElement('option');
    //         option.value = activity.Id;
    //         option.innerHTML = activity.Nome;
    //         select.appendChild(option);
    //     });
    // });

    // cell = empty_row.insertCell();
    // cell.colSpan = 2;
    // let input = document.createElement('input');
    // input.type = 'number';
    // input.min = 1;
    // input.max = 10;
    // input.id = 'input-posti';
    // cell.appendChild(input);

    // cell = empty_row.insertCell();
    // cell.colSpan = 2;
    // let button = document.createElement('button');
    // button.classList.add('save');
    // button.onclick = function() {addPartecipate(document.querySelector('#entries-codicefiscale').value, document.querySelector('#entries-data').value, select, input)};
    // button.innerHTML = 's';
    // cell.appendChild(button);

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
            cell.innerHTML = '<button class="delete" onclick="deletePartecipate('+partecipate.IdIngresso+', '+partecipate.Ora+')" >x</button>'; //button delete

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
    if(codicefiscale) {
        document.querySelector('#entries-codicefiscale').value = codicefiscale;
        getEntries(codicefiscale);
    }
    document.querySelector('#entries-codicefiscale').addEventListener('change', function() {
        getEntries(this.value);
    }); 

    document.querySelector('#entries-data').addEventListener('change', function() {
        getPartecipates(document.querySelector('#entries-codicefiscale').value, document.querySelector('#entries-data').value);
    });
}

Ajax();
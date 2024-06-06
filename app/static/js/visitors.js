var method = 'POST';

// api to get all the tariffs
async function getTariffs(url) {
    document.getElementById('tariffa').innerHTML = '';
    return fetch(url)
    .then(response => response.json())
    .then(data => {
        data.forEach(function(tariff) { 
            var option = document.createElement('option');
            option.value = tariff.NomeTariffa;
            option.text = tariff.NomeTariffa;
            document.getElementById('tariffa').appendChild(option);
        });
    });
}

// api to get all the durations
async function getDurations(url) {
    document.getElementById('durata').innerHTML = '';
    return fetch(url)
    .then(response => response.json())
    .then(data => {
        data.forEach(function(duration) { 
            var option = document.createElement('option');
            option.value = duration.Giorni;
            option.text = duration.Giorni;
            document.getElementById('durata').appendChild(option);
        });
    });
}

async function getCost(url) {
    fetch(url + '?NomeTariffa=' + document.getElementById('tariffa').value + '&Giorni=' + document.getElementById('durata').value)
    .then(response => response.json())
    .then(data => {
        document.getElementById('cost').value = data.Costo;
    });
}

async function modalSubscription( subscription = {CodiceFiscale: '', DataInizio: '', Costo: '', NomeTariffa: '', Costo: ''} , method='POST', url_tariffs, url_durations, url_cost) {
    document.getElementById('tariffa').innerHTML = '';
    document.getElementById('durata').innerHTML = ''; 
    if (typeof subscription === 'string') { // if the subscription is a string, it means that we are adding a new subscription
        method = 'POST';
        document.getElementById('subscription_codicefiscale').value = subscription;

        document.getElementById('datainizio').disabled = false;
        document.getElementById('tariffa').disabled = false;
        document.getElementById('durata').disabled = false;

        await getTariffs(url_tariffs);
        await getDurations(url_durations);
        await getCost(url_cost);

        document.getElementById('tariffa').addEventListener('change', function() {
            getCost(url_cost);
        });
        
        document.getElementById('durata').addEventListener('change', function() {
            getCost(url_cost);
        });
        document.querySelector('#subscription form input[type="button"]').onclick = function() {addSubscription(subscription)};
        document.querySelector('#subscription form input[type="button"]').value = "Add";
    } else {
        method = 'DELETE';
        document.getElementById('subscription_codicefiscale').value = subscription.CodiceFiscale;
        document.getElementById('datainizio').value = subscription.DataInizio== '' ? '' : new Date(subscription.DataInizio).toLocaleDateString('en-CA'); 
        document.getElementById('cost').value = subscription.Costo;
        
        var option = document.createElement('option');
        option.value = subscription.NomeTariffa;
        option.text = subscription.NomeTariffa;
        document.getElementById('tariffa').appendChild(option);

        option = document.createElement('option');
        option.value = subscription.Giorni;
        option.text = subscription.Giorni;
        document.getElementById('durata').appendChild(option);

        document.getElementById('datainizio').disabled = true;
        document.getElementById('tariffa').disabled = true;
        document.getElementById('durata').disabled = true;

        document.querySelector('#subscription form input[type="button"]').onclick = function() {deleteSubscription(subscription)};
        document.querySelector('#subscription form input[type="button"]').value = "Delete";
    }

    document.querySelector('#subscription').style.display = 'block';
}

function modalVisitor(visitor = {CodiceFiscale: '', Nome: '', Cognome: '', DataDiNascita: '', Altezza: '', Peso: ''}) {
    method = 'POST';
    document.querySelector('#visitor form input[type="button"]').value = "Add";
    document.getElementById('visitor_codicefiscale').value = visitor.CodiceFiscale;
    document.getElementById('nome').value = visitor.Nome;
    document.getElementById('cognome').value = visitor.Cognome;
    document.getElementById('birthday').value = visitor.DataDiNascita== '' ? '' : new Date(visitor.DataDiNascita).toLocaleDateString('en-CA'); 
    document.getElementById('altezza').value = visitor.Altezza;
    document.getElementById('peso').value = visitor.Peso; 
    document.querySelector('#visitor').style.display = 'block';
}


function addVisitor() {
    json = {
        CodiceFiscale: document.getElementById('visitor_codicefiscale').value,
        Nome: document.getElementById('nome').value,
        Cognome: document.getElementById('cognome').value,
        DataDiNascita: document.getElementById('birthday').value,
        Altezza: document.getElementById('altezza').value,
        Peso: document.getElementById('peso').value
    };
    form = document.querySelector('#visitor form');

    fetch(form.action, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
    })
    .then(response => statusResponse(response));
}

function deleteVisitor(visitor = {CodiceFiscale: '', Nome: '', Cognome: '', DataDiNascita: '', Altezza: '', Peso: ''}) {
    fetch(document.querySelector('#visitor form').action + '?CodiceFiscale=' + visitor.CodiceFiscale, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}


function deleteSubscription(subscription = {CodiceFiscale: '', DataInizio: '', Costo: '', NomeTariffa: '', Costo: ''}) {
    fetch(document.querySelector('#subscription form').action + '?CodiceFiscale=' + subscription.CodiceFiscale + '&DataInizio=' + new Date(subscription.DataInizio).toLocaleDateString('en-CA'), {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}

function addSubscription() {
    json = {
        CodiceFiscale: document.getElementById('subscription_codicefiscale').value,
        DataInizio: document.getElementById('datainizio').value,
        Costo: document.getElementById('cost').value,
        NomeTariffa: document.getElementById('tariffa').value,
        Giorni: document.getElementById('durata').value
    };
    form = document.querySelector('#subscription form');

    fetch(form.action, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
    })
    .then(response => statusResponse(response));
}
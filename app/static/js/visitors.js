var method = 'POST';

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

function getCost(url) {
    fetch(url + '?NomeTariffa=' + document.getElementById('tariffa').value + '&Giorni=' + document.getElementById('durata').value)
    .then(response => response.json())
    .then(data => {
        document.getElementById('cost').value = data.Costo;
    });
}


async function modalSubscription( subscription = {CodiceFiscale: '', DataInizio: '', Costo: '', NomeTariffa: '', Costo: ''} , method='POST', url_tariffs, url_durations, url_cost) {
    if (typeof subscription === 'string') {
        document.getElementById('subscription_codicefiscale').value = subscription;



        document.getElementById('datainizio').disabled = false;
        document.getElementById('tariffa').disabled = false;
        document.getElementById('durata').disabled = false;
        document.querySelector('#submit').value = "Add";
        
        await getTariffs(url_tariffs);
        await getDurations(url_durations);
        await getCost(url_cost);

        document.getElementById('tariffa').addEventListener('change', function() {
            getCost(url_cost);
        });
        
        document.getElementById('durata').addEventListener('change', function() {
            getCost(url_cost);
        });
    } else {
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

        document.querySelector('#submit').value = "Delete";
    }

    
    
    document.querySelector('form').method = method;
    document.querySelector('#subscription').style.display = 'block';
}

function deleteVisitor(visitor = {CodiceFiscale: '', Nome: '', Cognome: '', DataDiNascita: '', Altezza: '', Peso: ''}) {
    fetch(document.querySelector('#visitor form').action + '?CodiceFiscale=' + visitor.CodiceFiscale, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.status == 200) {
            statusResponse("200", 'Visitor deleted successfully');
        } else {
            statusResponse("400", 'Visitor not deleted');
        }
    });
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

document.querySelectorAll('.close').forEach(function(element) {
    element.addEventListener('click', function() {
        document.querySelector('.modal').style.display = 'none';
    }); 
});

window.onclick = function(event) {
    document.querySelectorAll('.modal').forEach(function(element) {
        if (event.target == element) {
            element.style.display = "none";
        }
    });
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
    .then(response => {
        if (response.status == 200) {
            statusResponse("200", 'Visitor added successfully');
        } else {
            statusResponse("400", 'Visitor not added');
        }
    });
}

function statusResponse(code, message) {
    img = 'img/status/' + code + '.jpg';
    document.querySelector('#content').innerHTML = "<img class='status' src="+img+"><p>"+message+"</p>";

    setTimeout(function() {
        location.reload();
    }, 5000);
}

// document.querySelector('#visitor form').addEventListener('onsubmit', function(event) {
//     event.preventDefault();
//     alert(event.target.action);
//     // var data = new FormData(event.target);
//     // console.log(data);
//     return ;
//     fetch(event.target.action, {
//         method: event.target.method,
//         body: data
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.querySelector('.modal').style.display = 'none';
//         location.reload();
//     });
// });

// document.getElementById('subscription').addEventListener('submit', function(event) {
//     event.preventDefault();
//     var data = new FormData(event.target);
//     fetch(event.target.action, {
//         method: event.target.method,
//         body: data
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.querySelector('.modal').style.display = 'none';
//         location.reload();
//     });
// });
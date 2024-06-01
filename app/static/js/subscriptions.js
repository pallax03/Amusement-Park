
function getTariffs() {
    fetch(url_for_get_tariffs)
    .then(response => response.json())
    .then(data => {
        document.getElementById('options_tariff').innerHTML = '';
        data.forEach(tariff => {
            document.getElementById('options_tariff').innerHTML += '<input type="radio" name="tariff" id="'+tariff.NomeTariffa+'"><label for="'+tariff.NomeTariffa+'"><p>'+tariff.NomeTariffa+'</p><label for="costogiornaliero"><input type="text" class="costogiornaliero" name="costogiornaliero" value="'+tariff.CostoGiornaliero+'" disabled>€ / Giorno</label></label>';
        });
    });
}

function getDurations() {
    fetch(url_for_get_durations)
    .then(response => response.json())
    .then(data => {
        document.getElementById('options_duration').innerHTML = '';
        data.forEach(duration => {
            document.getElementById('options_duration').innerHTML  += '<input type="radio" name="duration" id="'+duration.Giorni+'"><label for="'+duration.Giorni+'"><p>'+duration.Descrizione+': '+duration.Giorni+'</p><label for="discount">Sconto: <input type="text" name="discount" value="'+duration.Sconto+'" disabled></label></label>';
        });
    });
}


async function createOptionTariff() {
    radioClone = document.querySelector('[name="tariff"]').cloneNode(true);
    labelClone = document.querySelector('[for="'+radioClone.id+'"]').cloneNode(true);
    // Generare un nuovo ID unico
    const newId = 'Tariff' + Date.now();
    radioClone.id = newId;
    labelClone.setAttribute('for', newId);

    // Aggiungere l'evento per richiedere il nome della tariffa
    const pClone = labelClone.querySelector('p');
    const costInputClone = labelClone.querySelector('.costogiornaliero');

    pClone.textContent = 'Inserisci nome tariffa';
    pClone.setAttribute('contenteditable', 'true');
    costInputClone.disabled = false;
    costInputClone.value = '';

    // Aggiungere l'evento per impostare il focus e disabilitare gli input
    pClone.addEventListener('blur', function () {
        costInputClone.focus();
    });

    costInputClone.addEventListener('blur', async function () {
        pClone.removeAttribute('contenteditable');
        costInputClone.disabled = true;
        await addTariff( Tariff = {NomeTariffa: pClone.textContent, CostoGiornaliero: costInputClone.value});
        getTariffs();
    });
    
    document.getElementById('options_tariff').appendChild(radioClone);
    document.getElementById('options_tariff').appendChild(labelClone);
}

async function addTariff( Tariff = {NomeTariffa: '', CostoGiornaliero: ''} ) {
    fetch(url_for_add_tariff, {
        method: 'POST',
        body: JSON.stringify(Tariff),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        getTariffs();
    });
}

function getCost() {
    fetch(url_for_cost + '?NomeTariffa=' + document.querySelector('[name="tariff"]:checked').id + '&Giorni=' + document.querySelector('[name="duration"]:checked').id)
    .then(response => response.json())
    .then(data => {
        document.getElementById('costototale').value = data.Costo + '€';
    });
}

document.querySelectorAll('[name="tariff"]').forEach(radio => {
    radio.addEventListener('change', function() {
        getCost();
    });
})


document.querySelectorAll('[name="duration"]').forEach(radio => {
    radio.addEventListener('click', function() {
        getCost();
    });
});
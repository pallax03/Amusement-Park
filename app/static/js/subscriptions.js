function getTariffs() {
    fetch(url_for_get_tariffs)
    .then(response => response.json())
    .then(data => {
        document.getElementById('options_tariff').innerHTML = '';
        data.forEach(tariff => {
            html_tariff = '<input type="radio" name="tariff" id="'+tariff.NomeTariffa+'"><label for="'+tariff.NomeTariffa+'"><p>'+tariff.NomeTariffa+'</p><label for="costogiornaliero"><input type="text" class="costogiornaliero" name="costogiornaliero" value="'+tariff.CostoGiornaliero+'" disabled>€ / Giorno</label><ul class="categories">'
            tariff.Categories.forEach(category => {
                html_tariff += '<li>'+category.Nome+'</li>';
            });
            document.getElementById('options_tariff').innerHTML += html_tariff+'</ul></label>';
        });
    });
}

// TODO: Implementare la funzione per creare una pseudo nuova tariffa
// async function createOptionTariff() {
//     radioClone = document.querySelector('[name="tariff"]').cloneNode(true);
//     labelClone = document.querySelector('[for="'+radioClone.id+'"]').cloneNode(true);
//     // Generare un nuovo ID unico
//     const newId = 'Tariff' + Date.now();
//     radioClone.id = newId;
//     labelClone.setAttribute('for', newId);

//     // Aggiungere l'evento per richiedere il nome della tariffa
//     const pClone = labelClone.querySelector('p');
//     const costInputClone = labelClone.querySelector('.costogiornaliero');

//     pClone.textContent = 'Inserisci nome tariffa';
//     pClone.setAttribute('contenteditable', 'true');
//     costInputClone.disabled = false;
//     costInputClone.value = '';

//     // Aggiungere l'evento per impostare il focus e disabilitare gli input
//     pClone.addEventListener('blur', function () {
//         costInputClone.focus();
//     });

//     costInputClone.addEventListener('blur', async function () {
//         pClone.removeAttribute('contenteditable');
//         costInputClone.disabled = true;
//         await addTariff( Tariff = {NomeTariffa: pClone.textContent, CostoGiornaliero: costInputClone.value});
//         getTariffs();
//     });
    
//     document.getElementById('options_tariff').appendChild(radioClone);
//     document.getElementById('options_tariff').appendChild(labelClone);
// }

// TODO Implementare la funzione per aggiungere una tariffa, also in backend
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
        document.getElementById('box_costototale').style.display = '';
    });
}

document.querySelectorAll('[name="tariff"]').forEach(radio => {
    radio.addEventListener('change', async function() {
        document.getElementById('options_duration').parentElement.style.display = '';
        getCost();
    });
})

async function createOptionDuration() {
    radioClone = document.querySelector('[name="duration"]').cloneNode(true);
    labelClone = document.querySelector('[for="'+radioClone.id+'"]').cloneNode(true);

    function changeid(id) {
        radioClone.id = id;
        labelClone.setAttribute('for', id);
    }
    tmp_id = 'Duration'+Date.now();
    changeid(tmp_id); //tmp id
    //qui
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
    
    document.getElementById('options_duration').appendChild(radioClone);
    document.getElementById('options_duration').appendChild(labelClone);
}



document.querySelectorAll('[name="duration"]').forEach(radio => {
    radio.addEventListener('click', function() {
        getCost();
    });
});


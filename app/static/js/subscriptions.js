function acceptInteger(input) {
    input.value = input.value.replace(/[^0-9]/g, '');
}

function acceptFloat(input) {
    input.value = input.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1').replace(/^0[^.]/, '0');
}

function getCategories() {
    options = '';
    fetch(url_for_get_categories)
    .then(response => response.json())
    .then(data => {
        data.forEach(category => {
            options += '<input type="checkbox" name="category" id="'+category.Nome+'"><label for="'+category.Nome+'">'+category.Nome+'</label>';
        });
    });
    return options;
}

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
async function createOptionTariff() {
    const tariffId = 'Tariff' + Date.now();
    const categoriesHtml = await getCategories();
    const formHtml = `
        <input type="radio" name="tariff" id="${tariffId}">
        <label for="${tariffId}">
            <input type="text" name="${tariffId}" placeholder="Nome Tariffa" value="" onblur="enableDailyCostInput(this)">
            <label for="costogiornaliero">
                <input type="text" class="costogiornaliero" oninput="acceptFloat(this)" name="costogiornaliero" value="15" disabled onblur="createTariffObject(this)">€ / Giorno
            </label>
            <div id="options_category">${categoriesHtml}</div>
        </label>
    `;

    document.getElementById('options_tariff').insertAdjacentHTML('beforeend', formHtml);

    const tariffLabel = input.closest('label');
    const tariffName = tariffLabel.querySelector('input[type="text"][name^="Tariff"]').value;
    const dailyCost = input.value;
    const selectedCategories = Array.from(tariffLabel.querySelectorAll('input[name="category"]:checked'))
                                    .map(categoryInput => ({
                                        IdCategoria: parseInt(categoryInput.id), // Assuming category ID is embedded in the ID
                                        Nome: categoryInput.id
                                    }));

    const Tariff = {
        NomeTariffa: tariffName,
        CostoGiornaliero: dailyCost,
        Categories: selectedCategories
    };
}

// TODO Implementare la funzione per aggiungere una tariffa, also in backend
async function addTariff( Tariff = {NomeTariffa: '', CostoGiornaliero: '', Categories: []} ) {
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

function getDurations() {
    fetch(url_for_get_durations)
    .then(response => response.json())
    .then(data => {
        document.getElementById('options_duration').innerHTML = '';
        data.forEach(duration => {
            document.getElementById('options_duration').innerHTML += '<input type="radio" name="duration" id="'+duration.Giorni+'"><label for="'+duration.Giorni+'"><p><input type="text" placeholder="Descrizione" value="'+duration.Descrizione+'" disabled>: <input type="number" placeholder="" oninput="acceptInteger(this)" value="'+duration.Giorni+'" disabled></p><label for="discount">Sconto: <input type="float" oninput="acceptFloat(this)" name="discount" value="'+duration.Sconto+'" disabled></label></label>';
        });
        document.querySelectorAll('[name="duration"]').forEach(radio => {
            radio.addEventListener('click', function() {
                getCost();
            });
        });
    });
}

async function createOptionDuration() {

}



document.querySelectorAll('[name="duration"]').forEach(radio => {
    radio.addEventListener('click', function() {
        getCost();
    });
});


function acceptInteger(input) {
    input.value = input.value.replace(/[^0-9]/g, '');
}

function acceptFloat(input) {
    input.value = input.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1').replace(/^0[^.]/, '0');
}

function getCategories() {
    fetch(url_for_get_categories)
    .then(response => response.json())
    .then(data => {
        document.getElementById('options_category').innerHTML = '';
        data.forEach(category => {
            document.getElementById('options_category').innerHTML += '<input type="checkbox" name="category" id="'+category.IdCategoria+'"><label for="'+category.IdCategoria+'">'+category.Nome+'</label>';
        });
    });
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
        dynamicEvents();
    });
}

async function createOptionTariff() {
    const tariffId = 'Tariff' + Date.now();
    const category = await getCategories();
    const formHtml = `
        <input type="radio" name="tariff" id="${tariffId}">
        <label for="${tariffId}">
            <input type="text" name="${tariffId}" placeholder="Nome Tariffa" value="">
            <label for="costogiornaliero">
                <input type="text" class="costogiornaliero" oninput="acceptFloat(this)" name="costogiornaliero" value="15">€ / Giorno
            </label>
            <div id="options_category"></div>
        </label>
    `;

    document.getElementById('options_tariff').insertAdjacentHTML('beforeend', formHtml);
    await getCategories();
    
    document.querySelector('#btn_add_tariff').innerHTML = "S";
    document.querySelector('#btn_add_tariff').onclick = function() {addTariff(tariffId)};
}

async function addTariff(id) {
    const tariffLabel = document.querySelector(`label[for="${id}"]`);
    const tariffName = tariffLabel.querySelector('input[type="text"]').value;
    const dailyCost = parseFloat(tariffLabel.querySelector('input.costogiornaliero').value);
    const selectedCategories = [];
    document.querySelectorAll('[name="category"]:checked').forEach(checkbox => {
        selectedCategories.push({
            IdCategoria: checkbox.id,
            Nome: checkbox.nextElementSibling.textContent
        });
    });

    const Tariff = {
        NomeTariffa: tariffName,
        CostoGiornaliero: dailyCost,
        Categories: selectedCategories
    };

    fetch(url_for_add_tariff, {
        method: 'POST',
        body: JSON.stringify(Tariff),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => statusResponse(response))
    .then(data => getTariffs());
}

function deleteTariff(id) {
    fetch(url_for_add_tariff + '?NomeTariffa=' + id, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response))
    .then(data => getTariffs());
}

function getCost() {
    if(document.querySelector('[name="tariff"]:checked') == null ||
       document.querySelector('[name="duration"]:checked') == undefined) return;
    duration = document.querySelector('[name="duration"]:checked');
    fetch(url_for_cost + '?NomeTariffa=' + document.querySelector('[name="tariff"]:checked').id + '&Giorni=' + document.querySelector('[name="duration"]:checked').id)
    .then(response => response.json())
    .then(data => {
        document.getElementById('costototale').value = data.Costo + '€';
        document.getElementById('box_costototale').style.display = '';
    });
}

function dynamicEvents() {
    let lastTariffSelected = null;
    document.querySelectorAll('[name="tariff"]').forEach(radio => {
        radio.addEventListener('click', async function() {
            if(lastTariffSelected == radio) {
                lastTariffSelected = null;
                radio.checked = false;
                changeTariffButton(createOptionTariff, radio.id, "add");
            } else {
                lastTariffSelected = radio; 
                changeTariffButton(deleteTariff, radio.id, "delete")
            }
        });
        radio.addEventListener('change', async function() {
            document.getElementById('options_duration').parentElement.style.display = '';
            getCost();
        });
    })

    document.querySelectorAll('[name="duration"]').forEach(radio => {
        radio.addEventListener('click', function() {
            getCost();
        });
    });
}

function changeTariffButton(func, id, text) {
    document.querySelector('#btn_add_tariff').innerHTML = text == "add" ? "+" : "x";
    document.querySelector('#btn_add_tariff').className = text;
    document.querySelector('#btn_add_tariff').onclick = function() {func(id)};
}

function getDurations() {
    fetch(url_for_get_durations)
    .then(response => response.json())
    .then(data => {
        document.getElementById('options_duration').innerHTML = '';
        data.forEach(duration => {
            document.getElementById('options_duration').innerHTML += '<input type="radio" name="duration" id="'+duration.Giorni+'"><label for="'+duration.Giorni+'"><p><input type="text" placeholder="Descrizione" value="'+duration.Descrizione+'" disabled>: <input type="number" placeholder="" oninput="acceptInteger(this)" value="'+duration.Giorni+'" disabled></p><label for="discount">Sconto: <input type="float" oninput="acceptFloat(this)" name="discount" value="'+duration.Sconto+'" disabled></label></label>';
        });
        dynamicEvents();
    });
}

async function createOptionDuration() {
    // <input type="radio" name="duration" id="{{ duration.Giorni }}">    
    //                     <label for="{{ duration.Giorni }}">
    //                         <p>
    //                             <input type="text" placeholder="Descrizione" value="{{ duration.Descrizione }}" disabled>: 
    //                             <input type="number" placeholder="" oninput="acceptInteger(this)" value="{{ duration.Giorni }}">
    //                         </p>
    //                         <label for="discount">Sconto: 
    //                             <input type="float" oninput="acceptFloat(this)" name="discount" value="{{ duration.Sconto }}">
    //                         </label>
    //                     </label> 
}


dynamicEvents();

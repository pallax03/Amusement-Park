let flag_new_tariff = false;
let flag_new_duration = false;

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

// TARIFFS
function getTariffs() {
    fetch(url_for_get_tariffs)
    .then(response => response.json()) 
    .then(data => {
        document.getElementById('options_tariff').innerHTML = '';
        data.forEach(tariff => {

            html_tariff = 
            html_tariff = '<input type="radio" name="tariff" id="'+tariff.NomeTariffa+'"><label for="'+tariff.NomeTariffa+'">'+tariff.NomeTariffa+': '+tariff.CostoGiornaliero+'€ / Giorno <ul class="categories">'
            tariff.Categories.forEach(category => {
                html_tariff += '<li>'+category.Nome+'</li>';
            });
            document.getElementById('options_tariff').innerHTML += html_tariff+'</ul></label>';
        });
        flag_new_tariff = false;
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
                <input type="text" class="costogiornaliero" placeholder="Costo Giornaliero" oninput="acceptFloat(this)" name="costogiornaliero" value="">€ / Giorno
            </label>
            <div id="options_category"></div>
        </label>
    `;

    document.getElementById('options_tariff').insertAdjacentHTML('beforeend', formHtml);
    await getCategories();
    
    changeAPIButton('#btn_add_tariff', addTariff, tariffId, "save");
    flag_new_tariff = true;
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
    fetch(url_for_add_tariff + '?NomeTariffa=' + encodeURIComponent(id), {
        method: 'DELETE'
    })
    .then(response => statusResponse(response))
    .then(data => getTariffs());
}

function changeAPIButton(id, func, args, text) {
    document.querySelector(id).innerHTML = { 'add': '+', 'delete': 'x', 'save': 's' }[text];
    document.querySelector(id).className = text;
    document.querySelector(id).onclick = function() {func(args)};
}


// DURATIONS
function getDurations() {
    fetch(url_for_get_durations)
    .then(response => response.json())
    .then(data => {
        document.getElementById('options_duration').innerHTML = '';
        data.forEach(duration => {
            document.getElementById('options_duration').innerHTML += '<input type="radio" name="duration" id="'+duration.Giorni+'"><label for="'+duration.Giorni+'">'+duration.Descrizione+': '+ duration.Giorni+' Sconto: '+duration.Sconto+'%</label>';
        });
        flag_new_duration = false;
        dynamicEvents();
    });
}

async function createOptionDuration() {
    const durationId = 'Duration' + Date.now();
    const formHtml = `
        <input type="radio" name="duration" id="${durationId}">
        <label for="${durationId}">
            <p>
                <input type="text" placeholder="Descrizione" value="">: 
                <input type="number" placeholder="Giorni" oninput="acceptInteger(this)" value="">
            </p>
            <label for="discount">Sconto: 
                <input type="float" oninput="acceptFloat(this)" id="discount" name="discount" value="">%
            </label>
        </label>
    `;
    document.getElementById('options_duration').insertAdjacentHTML('beforeend', formHtml);
    changeAPIButton('#btn_add_duration', addDuration, durationId, "save");
    flag_new_duration = true;
}

async function addDuration(id) {
    const durationLabel = document.querySelector(`label[for="${id}"]`);
    const durationDescription = durationLabel.querySelector('input[type="text"]').value;
    const days = parseInt(durationLabel.querySelector('input[type="number"]').value);
    const discount = parseFloat(durationLabel.querySelector('input#discount').value);

    const Duration = {
        Descrizione: durationDescription,
        Giorni: days,
        Sconto: discount
    };

    fetch(url_for_add_duration, {
        method: 'POST',
        body: JSON.stringify(Duration),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => statusResponse(response))
    .then(data => getDurations());
}

function deleteDuration(id) {
    fetch(url_for_add_duration + '?Giorni=' + id, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response))
    .then(data => getDurations());
}


function getCost() {
    if(document.querySelector('[name="tariff"]:checked') == null ||
       document.querySelector('[name="duration"]:checked') == undefined) return;
    duration = document.querySelector('[name="duration"]:checked');
    fetch(url_for_cost + '?NomeTariffa=' + document.querySelector('[name="tariff"]:checked').id + '&Giorni=' + document.querySelector('[name="duration"]:checked').id)
    .then(response => response.json())
    .then(data => {
        document.getElementById('costototale').value = data.Costo + '€';
    });
}


function dynamicEvents() {  
    
    // TARIFFs
    let lastTariffSelected = null;
    document.querySelectorAll('[name="tariff"]').forEach(radio => {
        radio.addEventListener('click', async function() {
            if(lastTariffSelected == radio) {
                lastTariffSelected = null;
                radio.checked = false;
                changeAPIButton('#btn_add_tariff', createOptionTariff, radio.id, "add");
                document.getElementById('options_duration').parentElement.style.display = 'none';
            } else {
                lastTariffSelected = radio; 
                if(!flag_new_tariff) {
                    changeAPIButton('#btn_add_tariff', deleteTariff, radio.id, "delete")
                    document.getElementById('options_duration').parentElement.style.display = '';
                } else {
                    await getTariffs();
                    changeAPIButton('#btn_add_tariff', createOptionTariff, radio.id, "add");
                }
            }
        });
        radio.addEventListener('change', async function() {
            getCost();
        });
    })

    // DURATIONs
    let lastDurationSelected = null;
    document.querySelectorAll('[name="duration"]').forEach(radio => {
        radio.addEventListener('click', async function() {
            if(lastDurationSelected == radio) {
                lastDurationSelected = null;
                radio.checked = false;
                changeAPIButton('#btn_add_duration', createOptionDuration, radio.id, "add");
                document.getElementById('box_costototale').style.display = 'none';
            } else {
                lastDurationSelected = radio;
                if(!flag_new_duration) {
                    changeAPIButton('#btn_add_duration', deleteDuration, radio.id, "delete");
                    document.getElementById('box_costototale').style.display = '';
                } else {
                    await getDurations();
                    changeAPIButton('#btn_add_duration', createOptionDuration, radio.id, "add");
                }
            }
        });
        
        radio.addEventListener('change', function() {
            getCost();
        });
    });
}

dynamicEvents();
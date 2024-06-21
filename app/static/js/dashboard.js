let entries_chart = null;
let partecipates_chart = null;
let subscriptions_chart = null;


function renderChart(type, data, id) {
    const ctx = document.getElementById(id).getContext('2d');
    
    return new Chart(ctx, {
        type: type,  // bar, line, pie, doughnut, radar, polarArea, bubble, scatter
        data: {
            labels: data.labels,
            datasets: data.datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                  position: 'top',
                }
            }
        }
    });
}

function getCategories() {
    document.getElementById('filter_categorie').innerHTML = '<option value="" selected>Tutte</option>';
    fetch(url_for_get_categories)
    .then(response => response.json())
    .then(data => {
        data.forEach(category => {
            document.getElementById('filter_categorie').innerHTML += '<option value="' + category.Nome + '">' + category.Nome + '</option>';
        });
    });
}

function getTariffs() {
    document.getElementById('filter_tariffe').innerHTML = '<option value="" selected>Tutte</option>';
    fetch(url_for_get_tariffs)
    .then(response => response.json())
    .then(data => {
        data.forEach(tariff => {
            document.getElementById('filter_tariffe').innerHTML += '<option value="' + tariff.NomeTariffa + '">' + tariff.NomeTariffa + '</option>';
        });
    });
}

function getEntriesStats() {
    console.log(document.querySelector("#stats_entries-datainizio").value);
    console.log(document.querySelector("#stats_entries-datafine").value);

    fetch(url_for_stats_entries + "?DataInizio=" + document.querySelector("#stats_entries-datainizio").value + "&DataFine=" + document.querySelector("#stats_entries-datafine").value)
    .then(response => response.json())
    .then(data => {
        if (entries_chart) {
            entries_chart.destroy();
        }

        const labels = data.map(entry => entry.Data);
        const datasets = [{
            label: 'Numero Ingressi',
            data: data.map(entry => entry.NumeroIngressi),
            backgroundColor: data.map(() => getRandomColor()),
            borderColor: data.map(() => getRandomColor()),
            borderWidth: 1
        }];

        entries_chart = renderChart('bar', {labels, datasets}, 'entries_chart');
    })
}


function getPartecipatesStats() {
    fetch(url_for_stats_partecipates + '?NomeCategoria='+document.querySelector('#filter_categorie').value)
    .then(response => response.json())
    .then(data => {
        if (partecipates_chart) {
            partecipates_chart.destroy();
        }

        const labels = data.map(partecipate => partecipate.NomeCategoria);
        const datasets = [{
            label: 'Numero Partecipazioni',
            data: data.map(partecipate => partecipate.PartecipazioniTotali),
            backgroundColor: data.map(() => getRandomColor()),
            borderColor: data.map(() => getRandomColor()),
            borderWidth: 1
        }];

        partecipates_chart = renderChart('doughnut', {labels, datasets}, 'partecipates_chart');
    })
}


function getSubscriptionsStats() {
    fetch(url_for_stats_subscriptions + '?NomeTariffa='+document.querySelector('#filter_tariffe').value)
    .then(response => response.json())
    .then(data => {
        if (subscriptions_chart) subscriptions_chart.destroy();

        const labels = [];
        const datasets = {};
        const colors = [];

        data.forEach(entry => {
            if (!labels.includes(entry.Giorni)) {
                labels.push(entry.Giorni);
                colors.push(getRandomColor());
            }
            if (!datasets[entry.NomeTariffa]) {
                datasets[entry.NomeTariffa] = [];
            }
            datasets[entry.NomeTariffa].push(entry.NumeroAbbonamenti);
        });

        const datasetsArray = Object.keys(datasets).map(tariffa => ({
            label: tariffa,
            data: datasets[tariffa],
            backgroundColor: colors, 
            borderColor: colors,
            borderWidth: 1
        }));

        subscriptions_chart = renderChart('doughnut', {labels: labels.sort((a, b) => a - b), datasets: datasetsArray},'subscriptions_chart');
    })
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

document.addEventListener("DOMContentLoaded", function() {
    getCategories();
    getTariffs();

    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('change', function() {
            getEntriesStats();
        });
    });
    document.querySelector('#filter_categorie').addEventListener('change', function() {
        getPartecipatesStats();
    });
    document.querySelector('#filter_tariffe').addEventListener('change', function() {
        getSubscriptionsStats();
    });

    getEntriesStats();
    getPartecipatesStats();
    getSubscriptionsStats();
});
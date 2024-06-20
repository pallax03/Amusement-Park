globalconfig = {

}

function renderChart(data) {
    const ctx = document.getElementById('entries_chart').getContext('2d');
    const labels = data.map(entry => entry.Data);
    const values = data.map(entry => entry.NumeroIngressi);

    new Chart(ctx, {
        type: 'bar',  // Change this to 'line' if you prefer a line chart
        data: {
            labels: labels,
            datasets: [{
                label: 'Numero Ingressi',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
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
    document.getElementById('filter_tariffe').innerHTML = '<option value="" selected>Qualsiasi</option>';
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
        console.log(data);
        renderChart(data);
    })
}


function getPartecipatesStats() {
    fetch(url_for_stats_partecipates + '?NomeCategoria='+document.querySelector('#filter_categorie').value)
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
}


function getSubscriptionsStats() {
    fetch(url_for_stats_subscriptions + '?NomeTariffa='+document.querySelector('#filter_tariffe').value)
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
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

function getRoles() {
    fetch(url_for_get_roles)
    .then(response => response.json())
    .then(data => {
        document.getElementById('datalist_roles').innerHTML = '';
        data.forEach(role => {
            let option = document.createElement('option');
            option.setAttribute('IdRuolo', role.IdRuolo);
            option.setAttribute('Stipendio', role.Stipendio);
            option.text = role.Nome;
            option.setAttribute('Requires', JSON.stringify(role.Requires));
            document.getElementById('datalist_roles').appendChild(option);
        });
    });
}

function deleteRole(IdRuolo) {
    fetch(url_for_delete_role + '?IdRuolo=' + IdRuolo, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}

function getServices() {
    fetch(url_for_get_services)
    .then(response => response.json())
    .then(data => {
        document.getElementById('employee_servizio').innerHTML = '';
        data.forEach(service => {
            let option = document.createElement('option');
            option.setAttribute('IdServizio', service.IdServizio);
            option.text = service.Nome;
            document.getElementById('services').appendChild(option);
        });
    });
}

function getQuantity(input) {
    input.disabled = !input.disabled;
}

function updateSelectedRole(input) {

    let option = selectedRole(input);

    function selectedRole(input) {
        let selectedOption = null;
        document.querySelector('#datalist_roles').childNodes.forEach( option => {   
            if(selectedOption == null) {
                if (option.text == input.value) selectedOption = option;
            }
        });
        return selectedOption == null ? false : selectedOption;
    }

    showStipendio(option);
    showRequire(option);
    if(option) {
        let button = document.createElement('input');
        button.type = 'button';
        button.className = 'delete';
        button.value = 'elimina ruolo';
        button.onclick = function() {deleteRole(option.getAttribute('IdRuolo'))};

        document.getElementById('roles_require').appendChild(button);
    }

    function showStipendio(option) {
        if(option) {
            document.getElementById('employee_stipendio').disabled = true;
            document.getElementById('employee_stipendio').value = option.getAttribute('stipendio');
        } else {
            document.getElementById('employee_stipendio').value = '';
            document.getElementById('employee_stipendio').disabled = false;
        }
    }

    function getRequires() {
        fetch(url_for_get_categories)
        .then(response => response.json())
        .then(data => {
            data.forEach(category => {
                let li = document.createElement('li');

                let checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = category.Nome;

                let label = document.createElement('label');
                label.htmlFor = category.Nome;
                label.innerHTML = category.Nome;

                let quantity = document.createElement('input');
                quantity.type = 'number';
                quantity.id = 'quantity_'+category.Nome;
                quantity.placeholder = 'quantità';
                quantity.disabled = true;
                
                label.appendChild(quantity);

                checkbox.onclick = function () {getQuantity(quantity)};

                li.appendChild(checkbox);
                li.appendChild(label);
                

                document.getElementById('roles_require').appendChild(li);
            });
        });
    }

    function showRequire(option) {
        document.getElementById('roles_require').innerHTML = '<h3>Necessita:</h3>';
        if(option) {
            requires = JSON.parse(option.getAttribute('Requires'));
            if (requires.length == 0) document.getElementById('roles_require').innerHTML = '';
            else {
                requires.forEach(require => {
                    let li = document.createElement('li');
                    li.innerHTML = require.NomeCategoria + ': ' + require.Quantita;
                    document.getElementById('roles_require').appendChild(li);
                });
            }
        } else {
            getRequires();
        }
    }
}

function modalEmployee() {
    getRoles();
    document.querySelector('.modal#employee').style.display = 'block';
}

function addEmployee() {
    let employee = {
        CodiceFiscale: document.getElementById('employee_codicefiscale').value,
        Nome: document.getElementById('employee_nome').value,
        Cognome: document.getElementById('employee_cognome').value,
        DataNascita: document.getElementById('employee_datadinascita').value,
        Ruolo: {
            Nome: document.getElementById('employee_ruolo').value,
            Stipendio: document.getElementById('employee_stipendio').value
        }
    };

    selected_requires = document.querySelectorAll('input[type=checkbox]:checked');
    dict_requires = {
        Requires: []
    };
    selected_requires.forEach(input => {
        quantity = document.querySelector('#quantity_'+input.id).value;
        quantity = !isNaN(quantity) && quantity<1 ? 1 : quantity; 
        let dict_require = {
            NomeCategoria: input.id,
            Quantita: quantity
        };
        dict_requires.Requires.push(dict_require);
    });
    employee.Ruolo.Requires = dict_requires.Requires;

    fetch(url_for_add_employee, {
        method: 'POST',
        body: JSON.stringify(employee),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => statusResponse(response));
}

function deleteEmployee(codicefiscale) {
    fetch(url_for_add_employee + '?CodiceFiscale=' + codicefiscale, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}

function addService(codicefiscale, service) {
    fetch(url_for_add_employee_service + '?CodiceFiscale=' + codicefiscale + '&IdServizio=' + service, {
        method: 'POST'
    })
    .then(response => statusResponse(response));
}
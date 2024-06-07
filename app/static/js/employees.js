
function getRoles() {
    fetch(url_for_get_roles)
    .then(response => response.json())
    .then(data => {
        document.getElementById('roles').innerHTML = '';
        data.forEach(role => {
            let option = document.createElement('option');
            option.setAttribute('IdRuolo', role.IdRuolo);
            option.setAttribute('Stipendio', role.Stipendio);
            option.text = role.Nome;
            document.getElementById('roles').appendChild(option);
        });
    });
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



function updateStipendio(input) {

    let option = selectedRole(input);

    function selectedRole(input) {
        let selectedOption = null;
        
        return selectedOption == null ? false : selectedOption;
    }

    showStipendio(option);
    // checkRequire(option);

    function showStipendio(option) {
        if(option) {
            document.getElementById('employee_stipendio').disabled = true;
            document.getElementById('employee_stipendio').value = option.getAttribute('stipendio');
        } else {
            document.getElementById('employee_stipendio').value = '';
            document.getElementById('employee_stipendio').disabled = false;
        }
    }


    // function checkRequire(option) {
    //     fetch(url_for_check_require + '?IdRuolo=' + input.value)
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data) {
    //             document.getElementById('employee_servizio').parentElement.style.display = 'none';
    //         } else {
    //             document.getElementById('employee_servizio').parentElement.style.display = '';
    //             getServices();
    //         }
    //     });
    // }

    // <label for="Servizio" style="display: none;">Servizio:
    //                 <select name="Servizio" id="employee_servizio">

    //                 </select>
    //             </label>
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
            Nome: document.getElementById('employee_role').value,
            Stipendio: document.getElementById('employee_stipendio').value
        }
    }

    console.log(employee);

    fetch(url_for_add_employee, {
        method: 'POST',
        body: employee
    })
    .then(response => statusResponse(response));
}

function deleteEmployee(codicefiscale) {
    fetch(url_for_add_employee + '?CodiceFiscale=' + codicefiscale, {
        method: 'DELETE'
    })
    .then(response => statusResponse(response));
}
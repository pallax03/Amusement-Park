
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

    showStipendio();

    function showStipendio() {
        flag = false; 
        document.querySelector('#roles').childNodes.forEach( option => {   
            if(!flag) {
                if (option.text == input.value) {
                    document.getElementById('employee_stipendio').disabled = true;
                    document.getElementById('employee_stipendio').value = option.getAttribute('stipendio');
                    flag = true;
                } else {
                    document.getElementById('employee_stipendio').value = '';
                    document.getElementById('employee_stipendio').disabled = false;
                }
            }
        });
    }

    function checkRequire() {
        fetch(url_for_check_require + '?IdRuolo=' + input.value)
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('employee_servizio').parentElement.style.display = '';
                getServices();
            } else {
                document.getElementById('employee_servizio').parentElement.style.display = 'none';
            }
        });
    }

}

function modalEmployee() {
    getRoles();
    document.querySelector('.modal#employee').style.display = 'block';
}

function deleteEmployee(  ) {
// '{{ employee|tojson }}'
}
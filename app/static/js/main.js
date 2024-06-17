function acceptInteger(input) {
    input.value = input.value.replace(/[^0-9]/g, '');
}

function acceptFloat(input) {
    input.value = input.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1').replace(/^0[^.]/, '0');
}

async function statusResponse(response) {
    response_status = response.status;
    json = await response.json();

    if ( response_status < 300) {        // OK
        document.querySelector('#content').innerHTML = "<img class='status' src='img/status/200.jpg'><p>"+json.message+"</p>";
    } else if ( response_status < 400) { // Redirect
        document.querySelector('#content').innerHTML = "<img class='status' src='img/status/300.jpg'><p>"+json.message+"</p>";
    } else if ( response_status < 500) { // Client Error
        document.querySelector('#content').innerHTML = "<img class='status' src='img/status/400.jpg'><p>"+json.error+"</p>";
    } else {                             // Server Error
        document.querySelector('#content').innerHTML = "<img class='status' src='img/status/500.jpg'><p>"+json.error+"</p>";
    }
    setTimeout(function() {
        location.reload();
    }, 5000);
}


function emptyRow(body, colSpan, func) {
    let row = document.createElement('tr');
    row.className = 'empty_row';
    let cell = document.createElement('td');
    cell.colSpan = colSpan;
    let button = document.createElement('button');
    button.classList.add('add');
    button.onclick = func;
    button.innerHTML = '+';
    cell.appendChild(button);
    row.appendChild(cell);
    body.appendChild(row);
}


document.querySelectorAll('.close').forEach(function(element) {
    element.addEventListener('click', function() {
        document.querySelector('.modal').style.display = 'none';
    }); 
});


window.onclick = function(event) {
    document.querySelectorAll('.modal').forEach(function(element) {
        if (event.target == element) {
            element.style.display = "none";
        }
    });
}


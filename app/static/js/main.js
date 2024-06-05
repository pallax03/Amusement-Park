
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
    }, 10000);
}


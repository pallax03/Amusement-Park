
function statusResponse(response) {
    // Promise {<pending>}
    // [[Prototype]]
    // : 
    // Promise
    // [[PromiseState]]
    // : 
    // "fulfilled"
    // [[PromiseResult]]
    // : 
    // Object
    // message
    // : 
    // "Abbonamento eliminato"
    // [[Prototype]]
    // : 
    // Object
    console.log(response.json());

    if( response.status >= 200 || response.status < 300) {
        document.querySelector('#content').innerHTML = "<img class='status' src='img/status/200.jpg'><p>"+response.json().message+"</p>";
    } else if (response.status >= 400 || response.status < 500) {
        document.querySelector('#content').innerHTML = "<img class='status' src='img/status/400.jpg'><p>"+response.json().error+"</p>";
    } else {
        document.querySelector('#content').innerHTML = "<img class='status' src='img/status/500.jpg'><p>"+response.json().error+"</p>";
    }
    setTimeout(function() {
        location.reload();
    }, 20000);
}


async function getValue(){
    const numero = fetch('http://' + window.location.hostname + '/value')
        .then(response => response.json())
        .then(data => { updateNumber(data.value) });
}

function updateNumber(n) {
    const div = document.getElementById("result");
    div.innerHTML = n;
}

console.log("Funcionando");

window.setInterval(getValue, 250);

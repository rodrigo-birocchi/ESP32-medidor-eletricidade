// Tratar liga e desliga do medidor
var estadoAtual = -1;
const onOffSwitch = document.getElementById("on-off-switch");
onOffSwitch.addEventListener("click", function () {
    estadoAtual *= -1;
    console.log(estadoAtual);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://' + window.location.hostname + '/estado', true);
    xhr.setRequestHeader("Content-Type", "application/json");

    dados = 'estado=' + estadoAtual;

    xhr.send(dados);

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            console.log("Resposta: ", xhr.responseText);
        } else {
            console.error("Erro na requisição: ", xhr.statusText);
        }
    };
});


// Atualiza a lista de dados e move os dados uma unidade para frente
// (Adiciona um dado no fim da lista e remove o primeiro do início da lista)
async function update(data, i){

    const numero = fetch('http://' + window.location.hostname + '/value')
    .then(response => response.json())
    .then(convertido => {
        
        data.append({
            x: i,
            value: convertido.value
        });
        data.remove(0);

        update_valor_atual(convertido.value);
    });
}

// Escreve o valor atual de medição na tela
function update_valor_atual(n) {
    const valor_atual = document.getElementById("valor-atual");
    valor_atual.innerHTML = n;
}

// Inicia o desenho do gráfico
anychart.onDocumentReady(function () {

    // Lista para guardar os últimos 20 valores
    var data = [
        ["20", 0],["19", 0],["18", 0],["17", 0],
        ["16", 0],["15", 0],["14", 0],["13", 0],
        ["12", 0],["11", 0],["10", 0],["9", 0],
        ["8", 0],["7", 0],["6", 0],["5", 0],
        ["4", 0],["3", 0],["2", 0],["1", 0]
    ];

    // Criar um dataset
    var dataSet = anychart.data.set(data);

    // Mapear o dataset para uma curva no gráfico
    var seriesData = dataSet.mapAs({x: 0, value: 1});

    // Cria um gráfico de linha
    var chart = anychart.line();

    // Cria uma série de dados 
    var series = chart.line(seriesData);

    // Especifica o elemento onde o gráfico deve ser renderizado
    chart.container("container");

    // Renderiza o gráfico
    chart.draw();

    // Atualiza o gráfico com novos dados periodicamente
    var indexSetter = 0;
    window.setInterval(function () {

        if (estadoAtual == 1) {
            update(dataSet, indexSetter);
            indexSetter++;
        }
    }, 500);
});



// Updates the data with the latest value and shift data set forward 
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

function update_valor_atual(n) {
    const valor_atual = document.getElementById("valor-atual");
    valor_atual.innerHTML = n;
}

anychart.onDocumentReady(function () {

    // create list to store the last 20s of data
    var data = [
        ["20", 0],["19", 0],["18", 0],["17", 0],
        ["16", 0],["15", 0],["14", 0],["13", 0],
        ["12", 0],["11", 0],["10", 0],["9", 0],
        ["8", 0],["7", 0],["6", 0],["5", 0],
        ["4", 0],["3", 0],["2", 0],["1", 0]
    ];

    // create a data set
    var dataSet = anychart.data.set(data);

    // map the data for series
    var seriesData = dataSet.mapAs({x: 0, value: 1});

    // create a line chart
    var chart = anychart.line();

    // create the series and name it
    var series = chart.line(seriesData);
    // series.name("ACS712");

    // add a legend
    // chart.legend().enabled(true);

    // add a title
    // chart.title("Leitura ACS712");

    // specify where to display the chart
    chart.container("container");

    // draw the resulting chart
    chart.draw();

    var indexSetter = 0;
    window.setInterval(function () {
        update(dataSet, indexSetter);
        indexSetter++;
    }, 500);
});


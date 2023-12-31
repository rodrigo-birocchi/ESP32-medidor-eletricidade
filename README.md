# Medidor de Eletricidade

Repositório criado para disponibilização do código e documentação do projeto de Medição de Eletricidade, criado para a matéria de Computação Física e Aplicações, ministrada pelo Professor Doutor Fábio Nakano na Universidade de São Paulo. Neste projeto estará tanto o código, como a motivação e o racional por trás de decisões.

## Materiais

1. ESP32 microcontrolador
2. Sensor de corrente Allegro ACS712-05
3. Resistor 10KΩ e resistor variável
4. Placa de prototipagem
5. Conectores jumper
6. Módulo de relé
7. Fios elétricos e/ou conectores (Dependendo de como o medidor será conectado ao circuito que se deseja medir)

## Conceito

A ideia central do projeto é obter as leituras do sensor de corrente e então fornencer uma interface de fácil utilização para que os dados coletados sejam demonstrados em tempo real.

## Montagem

1. Pino Vin (5V) e pino GND do ESP32 são conectados aos barramentos de energia da placa de prototipagem.
2. Pino VCC e GND do ACS712 são conectados ao barramento positivo e negativo da placa respctivamente.
3. Pino VCC e GND do módulo de relé são conectados ao barramento positivo e negativo da placa respctivamente.
4. Pino de controle do módulo de relé é conectado ao pino 26 do ESP32.
5. Pino OUT do ACS712 é conectado ao pino 34 do ESP32, passando primeiro pelo divisor de tensão, como explicado a seguir.
6. O ACS712 e o módulo de relé tem os seus conectores de medição ligados em série um com o outro.
7. A carga a ser medida é ligada em série com o medidor, conforme o esquema do circuíto a seguir.

### Divisor de tensão

O conversor analógico digital do ESP32 tem a capacidade de lidar com sinais de amplitude de 0V - 3,3V. Enquanto que o sinal de saída do ACS712 possui amplitude de 0V - 5V. Por essa razão, é necessaŕio que o sinal de saída do ACS712 seja fornecido ao ESP32 por meio de um divisor de tensão o qual pode ser construído utilizando-se de resitores.

A fórmula que relaciona a tensão de entrada e tenão de saída no divisor de tensão é a seguinte:

Vout = (R2 / R1 + R2) Vin

![Esquema técnico de um divisor de tensão](assets/image.png)

Na qual, Vout é a tensão esperada na saída do divisor, Vin é a tensão de entrada, R1 e R2 são os valores da resistividade dos resistores.

No contexto do projeto, é necessário que a tensão de saída seja de 3,3V, no máximo, enquanto que a maior tensão de saída do sensor, é em teoria, 5V. Dessa forma temos:

 Vout = 3,3V
 Vin = 5V
 R1 = 10KΩ (escolhido ao acaso) 
 R2 = 5151Ω (determinado matematicamente) (resistor variável, para que seja possível calibrar a saída do sensor)

Produzindo assim a redução necessária. Além disso, de acordo com a folha de especificações do sensor, é esperado que haja uma variação de 185mV/A em relação a corrente eletrica a qual será medida. Mas ao passar o sinal pelo divisor de tensão, tal valor torna-se 122mV/A. Ou seja, para cada 1A de variação na corrente medida, havera uma variação de 185mV no sinal de saída do sensor e uma variação de 122mV no sinal lido pelo ESP32 através do divisor de tensão.

É esperado, pela folha de especificações do ACS712, que a tensão de saída para o caso de a corrente medida ser 0A deve ser de 2500mV. Porém, foi determinado empiricamente que o valor medido pelo ESP32, sem utilizar o divisor de tensão era de 2260mV, o que pode ser causado por interferências no fornecimento de energia ao ESP32. Por isso, o valor esperado na saída do divisor de tensão é de 1492mV, e dessa forma o divisor teve sua calibração final fina feita ao mover o resistor variável levemente até que o valor lido pelo ESP32 fosse correspondente ao teoricamente esperado (por volta de 1490mV).

### Conversor analógico digital

O ESP32 conta com um conversor analógico digital (ADC) com capacidade de medir sinais de amplitude 0-3,3V. A arquitetura do ADC é de 12 bits e por essa razão, pode representar números inteiros entre 0 e 4096. Assim, um sinal recebido em um pino do ESP32 será representado, de acordo com a sua intensida, em uma escala de 0 a 4095. Com sinal de intensidade 0V sendo lido como 0 e sinais de intensidade 3,3V sendo representados como 4095. Os valores intermediários são proporcionalmente representados na escala dessa forma. Por isso, para se obter o valor da intensidade do sinal recebido do sensor em volts é necessário multiplicar os valores brutos lidos pelo ESP32 por 0,805.

### Esquema de montagem

![Esquema de montagem do circuito](assets/esquema_eletrico.jpg)

## Software | Visão Geral

Foi definido que o ESP32 ficá responsável por executar um programa Python capaz de realizar as medições do sensor de corrente. Para isso, foi necessário instalar o MicroPython no ESP32. Para o desenvolvimento do programa, foi escolhida a IDE Thonny, por sua simplicidade e facilidade de interface com o ESP32 (É necessário instalar na IDE o plug-in do ESP32 o que pode ser feito através da ferramente interna da IDE). Para isso, foi consultado o seguinte guia: https://www.youtube.com/watch?v=rP4E5IyB_E0

No ESP32 foi armazenado o código fonte do projeto MicroWevSrv, disponível em: https://github.com/jczic/MicroWebSrv.git
Esse servidor é capaz de realizar as funções necessárias para o projeto:

1. Prover arquivos HTML, CSS e Javascript
2. Enviar e receber requisições HTTP, transferindo dados JSON

O ESP32 é conectado a uma rede Wi-Fi e ao iniciar o programa, o ESP32 fica preparado para receber requisições de dados no endereço: 
http://ip_do_ESP32_na_rede/valor

Qualquer outro dispositivo na mesma rede pode realizar requisições a esse endereço e obter um dado de medição instantânea do sensor.

A página web (medidor.html) ao ser acessada pelo usuário em outro dispositivo no endereço: http://ip_do_ESP32_na_rede/medidor.html, inicialmente não realiza requisições. Ao acionar o botão on/off na página, a mesma inicia o envio de requisições HTTP para o endereço supramencionado do ESP32 e ao receber os dados da medição instantânea do sensor, os adiciona ao gráfico de linha central na página.

Além disso, a página permite que um limite de corrente seja definido pelo usuário. Ao detectar que o limite foi excedido, a página web envia uma requisição para 
http://ip_do_ESP32_na_rede/estado, solicitando que a medição seja enterrompida. O ESP32 então desliga o circuíto com o relé.

O relé tembém pode ser acionado pelo mesmo esquema de comunicação quando o usuário interage com o botão On/Off no topo da página.

### Esquema de comunicação

![Esquema de comunicação](assets/esquema_comunicação.png)

### Software - ./www/medidor.html

Contém a página web com os principais elementos: botão on/off, que quando ligado realiza a medição de corrente através do sensore. Gráfico com a medição de corrente produzido através da biblioteca AnyChart (ver mais em: https://www.anychart.com/). Link para o github do projeto (https://github.com/rodrigo-birocchi/ESP32-medidor-eletricidade).

![Página inicial do projeto](assets/inicial.png)

### Software - ./www/script.js

Arquivo responsável pela inclusão do gráfico e sua atualização na interface. Realiza chamadas periódicas ao ESP32 com o método window.setInterval(). É possível configurar a frequência de medição em milissegundos por essa função.

### Software - ./ACS721/current_sensor.py

Escrito em python contém de fato a medição e gestão do sensor.

leitura(): realiza a leitura analógica, conforme o datasheet do sensor.

auto_zero(): encontra o zero do sensor, isto é, valor medido com ausência de corrente.
Essa função deve encontrar um valor próximo do valor esperado empiricamente (1492 ~ 1650) para que o sensor esteja funcionando corretamente. Caso o valor encontrado seja muito alto ou muito baixo, é provavel que haja algo de errado com a montegem do circuito. Além disso, caso o valor encontrado não seja correto a medição mostrada não ficará próxima de 0.0A mesmo sem carga alguma no circuito.

valor(): retorna corrente em ampéres, conforme especificações acima.
Obtém a diferença entre a medição atual e o zero do sensor, ou seja, o quanto a medida do sensor se afastou do zero por conta da corrente que está sendo medida. Então o valor é dividido pela variação indicada pela folha de especificações do ACS712 (185mV/A ou 122mV/A com o divisor de corrente), pois para cada 1A de variação na corrente, há um aumento de 185mV na saída do sensor.

### Software - ./relay/relay.py

Também escrito em python, responsável pela interação com o relay.

Utilizando o pino 26 do ESP32, manda comandos para ligar e desligar.

on(): Liga o relé

off(): Desliga o relé

### Software - ./network_credentials.py

Nesse arquivo devem ser preenchidas as credenciais da rede Wi-Fi desejada.
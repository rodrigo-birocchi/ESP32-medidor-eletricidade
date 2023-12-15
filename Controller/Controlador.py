import json
from microWebSrv import MicroWebSrv
from ACS712 import current_sensor as cs
from Relay import relay as rl


def _httpHandlerInstantPowerValueGet(httpClient, httpResponse):
    data = {
        "value": cs.valor()  
    }
    data = json.dumps(data)

    httpResponse.WriteResponseOk(
        headers = ({'Cache-Control': 'no-cache'}),
        contentType = 'application/json',
        contentCharset = 'UTF-8',
        content = data
    )

def _httpHandlerLigaDesligaMedidor(httpClient, httpResponse):

    data = httpClient.ReadRequestPostedFormData()
    estadoAtual = data["estado"]

    if (estadoAtual == "1"):
        print("Ligar")
        rl.on()
    else:
        print("Desligar")
        rl.off()

    httpResponse.WriteResponseOk(
        headers = None,
        contentType = 'application/json',
        contentCharset = 'UTF-8',
        content = "estado: " + estadoAtual
    )
    
routeHandlers = [ ( "/value", "GET", _httpHandlerInstantPowerValueGet ),
                 ( "/estado", "POST", _httpHandlerLigaDesligaMedidor ) ]


srv = MicroWebSrv(routeHandlers=routeHandlers, webPath='/www/')
srv.Start(threaded=False)


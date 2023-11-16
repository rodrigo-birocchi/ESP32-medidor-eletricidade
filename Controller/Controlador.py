from Medidor import medidor as med
import json
from microWebSrv import MicroWebSrv

def _httpHandlerInstantPowerValueGet(httpClient, httpResponse):
    data = {
        "value": med.potencia_atual()    
    }
    data = json.dumps(data)

    httpResponse.WriteResponseOk(
        headers = ({'Cache-Control': 'no-cache'}),
        contentType = 'application/json',
        contentCharset = 'UTF-8',
        content = data
    )
    
routeHandlers = [ ( "/value", "GET", _httpHandlerInstantPowerValueGet ) ]

srv = MicroWebSrv(routeHandlers=routeHandlers, webPath='/www/')
srv.Start(threaded=False)

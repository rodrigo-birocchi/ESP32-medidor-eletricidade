import json
from microWebSrv import MicroWebSrv
from ACS712 import current_sensor as cs


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

    
routeHandlers = [ ( "/value", "GET", _httpHandlerInstantPowerValueGet ) ]


srv = MicroWebSrv(routeHandlers=routeHandlers, webPath='/www/')
srv.Start(threaded=False)

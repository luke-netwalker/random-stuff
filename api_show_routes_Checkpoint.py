#definizione librerie utilizzate
import requests
import json
import urllib3
#-----------------------------------------------------------------------------------------------------
urllib3.disable_warnings() #disabilitazione warning dovuti dall'assenza di un certificato valido sul firewall
#-----------------------------------------------------------------------------------------------------
#definizione variabili
utenza = 'xxxx'
secret = 'xxxxxxx'
ip = 'x.x.x.x'
porta = '443' #default 443
#-----------------------------------------------------------------------------------------------------
#Funzione chiamate API
def api_call(ip_addr, port, command, json_payload, sid):
    url = 'https://' + ip_addr + ':' + port + '/gaia_api/' + command
    if sid == '':
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : sid}
    r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
    return r.json()
#-----------------------------------------------------------------------------------------------------
#Funzione di Login
def login(user,password):
    payload = {'user':user, 'password':password}
    response = api_call(ip, porta, 'login', payload, '')
    #print(response)
    return response["sid"]
#-----------------------------------------------------------------------------------------------------
#Generatore del SID necessario per le future chiamate API
sid = login(utenza,secret)
#print("session id: " + sid)
#-----------------------------------------------------------------------------------------------------
#Estrazione delle rotte (JSON)
static_route_result = api_call(ip, porta, 'show-static-routes', {"limit":200, "offset":0, "order": "DESC"}, sid) #se il firewall interrogato ha più di 200 rotte allora va ripetuto più volte alzando l'offset
JRoute = json.dumps(static_route_result))
#-----------------------------------------------------------------------------------------------------
#Logout
logout_result = api_call(ip, porta, 'logout', {}, sid)
#print("logout result: " + json.dumps(logout_result))
#-----------------------------------------------------------------------------------------------------
#Programma

#definizione librerie utilizzate
import requests
import json
import urllib3
from ipaddress import IPv4Address, IPv4Network
import pandas as pd
#-----------------------------------------------------------------------------------------------------
urllib3.disable_warnings() #disabilitazione warning dovuti dall'assenza di un certificato valido sul firewall
#-----------------------------------------------------------------------------------------------------
#definizione variabili
utenza = 'xxxx'
secret = 'xxxxxxx'
ip = 'x.x.x.x'
porta = '443' #default 443
cols = ["flags", "destination", "nexthop", "descr_NH", "interface", "virtual-router"]
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
#Estrazione delle intefacce (JSON) e ottimizzazione dell'output
interface_result = api_call(ip, porta, 'show-interfaces', {}, sid) #se il firewall interrogato ha più di 200 rotte allora va ripetuto più volte alzando l'offset
JInterface = {"destination": [], "nexthop": [], "interface": []}
k=0 #variabile per fare da contatore utile a scorrere tutti i valori della lista degli oggetti contenuti nel json
y=0 #variabile necessaria a contare quante interfacce sono effettivamente configurate, servirà più avanti
for object in interface_result["objects"]:
    address = interface_result["objects"][k]["ipv4-address"]
    mask = str(interface_result["objects"][k]["ipv4-mask-length"])
    network = address + "/" + mask
    interface = interface_result["objects"][k]["name"]
    if address == "Not-Configured":
        pass
    else:
        JInterface["destination"].append(network)
        JInterface["interface"].append(interface)
        JInterface["nexthop"].append("is directly connected")
        y += 1
    k += 1
#-----------------------------------------------------------------------------------------------------
#Estrazione delle rotte (JSON) e ottimizzazione dell'output
static_route_result = api_call(ip, porta, 'show-static-routes', {"limit":200, "offset":0, "order": "DESC"}, sid) #se il firewall interrogato ha più di 200 rotte allora va ripetuto più volte alzando l'offset
JRoute = {"destination": [], "nexthop": [], "interface": []}
i=0 #variabile per fare da contatore utile a scorrere tutti i valori della lista degli oggetti contenuti nel json
for object in static_route_result["objects"]:
    address = static_route_result["objects"][i]["address"]
    mask = str(static_route_result["objects"][i]["mask-length"])
    network = address + "/" + mask
    next_hop = static_route_result["objects"][i]["next-hop"][0]["gateway"]
    host = IPv4Address(next_hop)
    error_Counter = 0
    z = y #assegna alla variabile z dello stesso valore di interfacce utilizzate
    while z > 0: #verifica dietro quale interfaccia si trova il next hop 
        rete = IPv4Network(JInterface["destination"][z-1], strict=False)
        if host in rete: 
            JRoute["interface"].append(JInterface["interface"][z-1])
        else:
            error_Counter += 1
            if error_Counter == y:
                JRoute["interface"].append("ERRORE di Configurazione") #se non trova nessuna interfacca evidentemente è stata configurata male una rotta lato firewall
        z -= 1
    z = y
    JRoute["destination"].append(network)
    JRoute["nexthop"].append(next_hop)
    i += 1
#-----------------------------------------------------------------------------------------------------
#Logout
logout_result = api_call(ip, porta, 'logout', {}, sid)
#print("logout result: " + json.dumps(logout_result))
#-----------------------------------------------------------------------------------------------------
#Programma
df_int = pd.DataFrame(JInterface, columns=cols)
df_rou = pd.DataFrame(JRoute, columns=cols)
df = pd.concat([df_int, df_rou], axis=0, ignore_index=True)
df.to_csv("routing_CP_" + ip + "_.csv") 

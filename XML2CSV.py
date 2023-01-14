#-------------------inizio---------------------------
#lib
import xml.etree.ElementTree as Xet
import pandas as pd
import requests
import urllib3
#fine lib
#----------------------------------------------------
urllib3.disable_warnings() #disabilitazione warning dovuti dall'assenza di un certificato valido sul firewall
#-----------------------------------------------------------------------------------------------------
#variabili
cols = ["flags", "destination", "nexthop", "descr_NH", "interface", "virtual-router"] #in questa lista si definiscono i valori dell'intestazione del file CSV
rows = []
ip = "x.x.x.x"
REST_API_TOKEN = "xxxxxxx"
Authorization = "Basic xxxxxxxxxxx"
output = "Rounting_PA_" + ip + "_.csv"
#fine variabili
#----------------------------------------------------
#Chiamata API
url = "https://" + ip + "/api/?REST_API_TOKEN=" + REST_API_TOKEN + "&type=op&cmd=%3Cshow%3E%3Crouting%3E%3Croute%3E%3C%2Froute%3E%3C%2Frouting%3E%3C%2Fshow%3E"
payload={}
headers = {
  'Authorization': Authorization
}
response = requests.request("GET", url, headers=headers, data=payload, verify=False)
response = response.content.decode()
#fine chiamata API
#----------------------------------------------------
#programma
root = Xet.fromstring(response)                             #esegue il parse dell'informazioni presenti nel file XML che gli viene passato in "input"
for i in root.findall('./result/entry'):                    #esegue un ciclo for per ogni tag <entry> presente nel file xml
    flags = i.find("flags").text                            #estrae il valore contenuto all'interno del tag <flags>
    destination = i.find("destination").text                #estrae il valore contenuto all'interno del tag <destination>
    nexthop = i.find("nexthop").text                        #estrae il valore contenuto all'interno del tag <nexthop>
    interface = i.find("interface").text                    #estrae il valore contenuto all'interno del tag <interface>
    virtual_router = "PA_"+i.find("virtual-router").text    #estrae il valore contenuto all'interno del tag <virtual-router> e gli aggiunge il prefisso "PA_"
    rows.append({"flags": flags,                            #inserisce i valori estratti nella lista "rows" secondo la formattazione indicata
        "destination": destination,
        "nexthop": nexthop,
        "interface": interface,
        "virtual-router": virtual_router})
df = pd.DataFrame(rows, columns=cols)                       #construisce il data frame                  
df.to_csv(output,  index = False)                           #onverte il data frame in CSV
#fine programma
#----------------------fine--------------------------
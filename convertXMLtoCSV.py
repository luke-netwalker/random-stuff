#-------------------inizio---------------------------
#lib
import xml.etree.ElementTree as Xet
import pandas as pd
import sys
#fine lib
#----------------------------------------------------
#variabili
cols = ["flags", "destination", "nexthop", "descr_NH", "interface", "virtual-router"] #in questa lista si definiscono i valori dell'intestazione del file CSV
rows = []
Input = sys.argv[1] + '.xml'
Output = sys.argv[1] + '.csv'
#fine variabili
#----------------------------------------------------
#programma
xmlparse = Xet.parse(Input)                                 #esegue il parse dell'informazioni presenti nel file XML che gli viene passato in "input"
root = xmlparse.getroot()                                   #estrae i tag xml
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
df.to_csv(Output)                                           #onverte il data frame in CSV
#fine programma
#----------------------fine--------------------------

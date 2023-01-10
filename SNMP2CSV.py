#-------------------inizio---------------------------
#lib
import pandas as pd
import sys
#fine lib
#----------------------------------------------------
#variabili
cols = ["flags", "destination", "nexthop", "descr_NH", "interface", "virtual-router"] #in questa lista si definiscono i valori dell'intestazione del file CSV
rows = []
dest = []
mask = []
destination = []
nexthop = []
interface = []
virtual_router = []
ro = [0,0,0,0,0,0]          #se si vuole aggiungere altri virtual system vanno aggiunti altri valori in questa lista e successivamente adattare le funzioni "extract_row" e "fill_vr"
input = "./"+sys.argv[1]    #file txt contenente l'output dei comandi SNMP relativi alle routing table
output = Routing_CheckPoint.csv
#fine variabili
#----------------------------------------------------
#funzioni
def extract_row(r):         #ha lo scopo di indicare quante rotte ha ogni singolo Virtual Sysyem analizzato
    if ro[0] < r:           #si basa sul fatto che il numero di righe è differente nei vari VS
        ro[0] = r           #pertanto quando c'è una differenza questa sezione salva l'ultimo valore prima che il contatore venge resettato   
    else:
        if ro[1] == 0:
            ro[1] = ro[0]
            ro[0] = 0
        elif ro[2] == 0:
            ro[2] = ro[0]
            ro[0] = 0
        elif ro[3] == 0:
            ro[3] = ro[0]
            ro[0] = 0
        elif ro[4] == 0:
            ro[4] = ro[0]
            ro[0] = 0
        else: 
            ro[5] = ro[0]   #attualmente il programma è settato per ospitare 5 VS ma è facilmente scalabile
def mask_2_barra(mask):     #converte la subnetmask nel barra equivalente
    m = ''
    if mask == "0.0.0.0":
        m = "/0"
    elif mask == "128.0.0.0":
        m = "/1"
    elif mask == "192.0.0.0":
        m = "/2"
    elif mask == "224.0.0.0":
        m = "/3"
    elif mask == "240.0.0.0":
        m = "/4"
    elif mask == "248.0.0.0":
        m = "/5"
    elif mask == "252.0.0.0":
        m = "/6"
    elif mask == "254.0.0.0":
        m = "/7"
    elif mask == "255.0.0.0":
        m = "/8"
    elif mask == "255.128.0.0":
        m = "/9"
    elif mask == "255.192.0.0":
        m = "/10"
    elif mask == "255.224.0.0":
        m = "/11"
    elif mask == "255.240.0.0":
        m = "/12"
    elif mask == "255.248.0.0":
        m = "/13"
    elif mask == "255.252.0.0":
        m = "/14"
    elif mask == "255.254.0.0":
        m = "/15"
    elif mask == "255.255.0.0":
        m = "/16"
    elif mask == "255.255.128.0":
        m = "/17"
    elif mask == "255.255.192.0":
        m = "/18"
    elif mask == "255.255.224.0":
        m = "/19"
    elif mask == "255.255.240.0":
        m = "/20"
    elif mask == "255.255.248.0":
        m = "/21"
    elif mask == "255.255.252.0":
        m = "/22"
    elif mask == "255.255.254.0":
        m = "/23"
    elif mask == "255.255.255.0":
        m = "/24"
    elif mask == "255.255.255.128":
        m = "/25"
    elif mask == "255.255.255.192":
        m = "/26"
    elif mask == "255.255.255.224":
        m = "/27"
    elif mask == "255.255.255.240":
        m = "/28"
    elif mask == "255.255.255.248":
        m = "/29"
    elif mask == "255.255.255.252":
        m = "/30"
    elif mask == "255.255.255.254":
        m = "/31"
    elif mask == "255.255.255.255":
        m = "/32"
    else:
        m = mask
    return m 
def assegna_lista(v,c):     #inserisce i valori estratti dal file di testo e li inserisce nell'apposita lista basandosi sul valore presente nella variabile "col"
    if c == "2":
        dest.append(v)
    elif c == "3":
        mask.append(v)
    elif c == "4":
        nexthop.append(v)
    elif c == "5":
        interface.append(v)
    else:
        return 0
def unisci_valori_dst():    #concatena l'elemento "i" della lista "dest" con l'elemento "i" della lista "mask" 
    i = 0
    x = len(dest)
    while i < x:
        destination.append(dest[i]+mask[i])
        i += 1
def fill_vr():              #inserisce dei valori statici relativi al nome del Virtual System per il numero di righe necessario
    for x in range(ro[1]):
        virtual_router.append("VS_BUSINESS")
    for x in range(ro[2]):
        virtual_router.append("VS_DMZ_INTERNAL")
    for x in range(ro[3]):
        virtual_router.append("VS_MGMT")
    for x in range(ro[4]):
        virtual_router.append("VS_CAMPUS")
    for x in range(ro[5]):
        virtual_router.append("VS_EXTRANET")
def fill_rows():            #sostituisce i next hop "0.0.0.0" con "is directly connected" e successivamente inserisce i valori delle varie liste nella lista "rows" formattandole adeguatamente
    i = 0
    s = ro[1] + ro[2] + ro[3] + ro[4] + ro[5]
    while i < s:
        if nexthop[i] == "0.0.0.0":
            nexthop[i] = "is directly connected"
        dst = destination[i]
        next = nexthop[i]
        intf = interface[i]
        vr = virtual_router[i]
        rows.append({"destination": dst,
                        "nexthop": next,
                        "interface": intf,
                        "virtual-router": vr})
        i += 1
#fine funzioni
#----------------------------------------------------
#programma
with open(input) as file:                                           #carica il file definito nella variabile "input" 
    while True:                                                     #cicla fino a quando non ci sono più righe da analizzare
        line = file.readline()                                      #legge il contenuto di una singola riga
        if not line:                                                #se finisce le righe da analizzare esce dal ciclo
            ro[5] = last_row                                        #ro[x] con x = ultimo valore della lista
            break                                                   #esce dal ciclo
        col = line[27:28]                                           #estrae il numero relativo alla colonna
        value_1 = line[str.find(line, ':') + 2 : len(line) - 1]     #estrae il contenuto relarivo alla riga analizzata
        if col == "3":                                              #nella colonna "3" ci sono le subnetmask
            value = mask_2_barra(value_1)                           #converte la subnetmask nella relativa barra (es. 255.255.255.0 -> /24)
        else:                                                       #altrimenti
            value = value_1                                         #per le altre colonne lascia il valore invariato
        if col == "1":                                              #nella colonna "1" ci sono il numero di righe
            last_row = int(value)                                   #serve per inserire il numero di righe dell'ultimo VS analizzato
            extract_row(int(value))                                 #calcola quante rotte ha ogni signolo virtual system analizzato
        assegna_lista(value,col)                                    #inserisce i valori nelle apposite liste
    unisci_valori_dst()                                             #concatena i valori delle colonne 2 e 3 (es. "10.238.0.0" e "255.255.0.0" -> "10.238.0.0/16")
    fill_vr()                                                       #aggiunge i valori relativi al virtual system nella lista "virtual_router"
    fill_rows()                                                     #unisce le varie liste nella lista "rows" formattandolo nel formato necessario alla libreria "pandas"
    df = pd.DataFrame(rows, columns=cols)                           #crea il data frame
    df.to_csv(output)                                               #converte il data frame nel file CSV
#fine programma
#----------------------fine--------------------------


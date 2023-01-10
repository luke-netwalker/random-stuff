#-------------------inizio---------------------------
#lib
import pandas as pd
import sys
#fine lib
#----------------------------------------------------
#variabili
palo_alto = sys.argv[1]
chekpoint = sys.argv[2]
file = [palo_alto, chekpoint]
output = "routing.csv"
#fine variabili
#----------------------------------------------------
#programma
combined_csv = pd.concat([pd.read_csv(f) for f in file ])           #concatena i file presenti nella lista in un unico file
combined_csv.to_csv( output, index=False, encoding='utf-8-sig')     #esporta in csv
#fine programma
#----------------------fine--------------------------

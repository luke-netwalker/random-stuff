"""
questo script è il terzo passaggio, qui si confrontano i due file CSV contenenti i gateway e i tunnel attivi, se vi sono delle differenze
qui verranno elencate a schermo e a scelta dell'utente si potranno riavviare tutti o solo alcuni gateway, nel passaggio successivo verrà chiesta
la stessa cosa per i tunnel
"""
import pandas as pd
import requests
import time
import urllib3

urllib3.disable_warnings()
df1 = pd.read_csv('tunnel_1.csv')
df2 = pd.read_csv('tunnel_2.csv')
gw1 = list(df1["gateway"])
gw2 = list(df2["gateway"])
diff_gw = list(set(gw1).difference(set(gw2)))
len_diff_gw = len(diff_gw)
tu1 = list(df1["name"])
tu2 = list(df2["name"])
diff_tu = list(set(tu1).difference(set(tu2)))
len_diff_tu = len(diff_tu)
df_gw = pd.DataFrame(diff_gw, columns=["gateway"])
df_tu = pd.DataFrame(diff_tu,columns=["tunnel"])

ip = "x.x.x.x"
REST_API_TOKEN = "xxxx"
Authorization = "Basic xxxxxxx"
Cookie = "PHPSESSID=xxxxxxxxxxxxxxxxx"

if len(diff_gw) == 0:
  print(f'non ci sono fasi 1 "down" rispetto a prima\n')
else:
  print(df_gw)
  
  s_gw = int(input("scegli quale tunnel restartare [0-" + str(len_diff_gw-1) + "] [999 = tutti]: "))
  if s_gw == 999:
    for i_gw in range(len_diff_gw):
      url = "https://" + ip + "/api/?REST_API_TOKEN=" + REST_API_TOKEN + "&type=op&cmd=%3Ctest%3E%3Cvpn%3E%3Cike-sa%3E%3Cgateway%3E" + diff_gw[i_gw] + "%3C%2Fgateway%3E%3C%2Fike-sa%3E%3C%2Fvpn%3E%3C%2Ftest%3E"

      payload={}
      headers = {
      'Authorization': Authorization,
      'Cookie': Cookie
      }

      response = requests.request("GET", url, headers=headers, data=payload, verify=False)

      print(f"\n" + response.text + f"\n")
      time.sleep(0.5)
  else:
    url = "https://" + ip + "/api/?REST_API_TOKEN=" + REST_API_TOKEN + "&type=op&cmd=%3Ctest%3E%3Cvpn%3E%3Cike-sa%3E%3Cgateway%3E" + diff_gw[s_gw] + "%3C%2Fgateway%3E%3C%2Fike-sa%3E%3C%2Fvpn%3E%3C%2Ftest%3E"

    payload={}
    headers = {
    'Authorization': Authorization,
    'Cookie': Cookie
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    print(f"\n" + response.text + f"\n")

if len(diff_tu) == 0:
  print(f'non ci sono fasi 2 "down" rispetto a prima\n')
else:
  print(df_tu)

  s_tu = int(input("scegli quale tunnel restartare [0-" + str(len_diff_tu-1) + "] [999 = tutti]: "))
  if s_tu == 999:
    for i_tu in range(len_diff_tu):
      url = "https://" + ip + "/api/?REST_API_TOKEN=" + REST_API_TOKEN + "&type=op&cmd=%3Ctest%3E%3Cvpn%3E%3Cipsec-sa%3E%3Ctunnel%3E" + diff_tu[i_tu].replace(":", "%3A") + "%3C%2Ftunnel%3E%3C%2Fipsec-sa%3E%3C%2Fvpn%3E%3C%2Ftest%3E"

      payload={}
      headers = {
      'Authorization': Authorization,
      'Cookie': Cookie
      }

      response = requests.request("GET", url, headers=headers, data=payload, verify=False)

      print(f"\n" + response.text + f"\n")
      time.sleep(0.5)
  else:
    url = "https://"+ip+"/api/?REST_API_TOKEN=" + REST_API_TOKEN + "&type=op&cmd=%3Ctest%3E%3Cvpn%3E%3Cipsec-sa%3E%3Ctunnel%3E" + diff_tu[s_tu].replace(":", "%3A") + "%3C%2Ftunnel%3E%3C%2Fipsec-sa%3E%3C%2Fvpn%3E%3C%2Ftest%3E"

    payload={}
    headers = {
    'Authorization': Authorization,
    'Cookie': Cookie
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    print(f"\n" + response.text + f"\n")

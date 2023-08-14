import requests
import datetime
import time
import re
from bs4 import BeautifulSoup


print('-'*30)
print('Subtinator: subdomain extraction to txt')
print('-'*30+'\n')

# input du dns
domain_name = input('Enter the domain to search (exemple: google.com): ')

print('-'*30+'\n')
# Fonctions pour rapiddns

def request_rdns(domain,page=""):
    url="https://rapiddns.io/s/"
    r=requests.get(url+str(domain))
    result = r.text
    return str(result)

def pageNum(req):
    # extraction du nombre de pages pour le parsing
    print("[*] Number of results: "+re.findall('>[0-9]+<\/s',req)[0][1:-3])
    pagenum = (int(re.findall('>[0-9]+<\/s',req)[0][1:-3])//100)+2
    return pagenum

def parsePage(pagenum,req):
    url="https://rapiddns.io/s/"
    lt = []
    # ajout ?page=num_id pour parser
    page = "?page="
    time.sleep(0.5)
    print(f'[*] Number of page to parse: {pagenum-1}')
    time.sleep(0.5)
    print('[*] Please wait, parsing in progress...')
    for i in range(2,pagenum):
        #sleep 0.7s pour éviter de se faire tej par rapiddns
        time.sleep(0.7)
        r=requests.get(url+str(domain_name)+page+str(i))
        req = r.text
        # extraction de tous les sous domaines de la page:
        soup = BeautifulSoup(req, 'html.parser')
        tbody = soup.find('tbody')


        for tr in tbody.find_all('tr'):
            td = tr.find('td')  # Get the first <td> tag
            lt.append(td.text)

        print(f'[*] Page {str(i)} parsed, next page...')

    time.sleep(1)
    print('[+] All page parsed for rapiddns.')
    return lt

# Fonctions pour crt.sh

def crtShReq(lt,domain):
    crt_url="https://crt.sh/?q="
    output="&output=json"
    r = requests.get(crt_url+str(domain_name)+output)
    extracted = r.json()
    if len(extracted) == 0:
        print("[-] No value found in crt.sh.")
        return lt
    else:
        print("[*] Values found!")
        time.sleep(2)
        for domain in range(len(extracted)):
            unformated_name = extracted[domain]['name_value']
            formated = unformated_name.split()[0]
            lt.append(formated)
    lt = set(lt)
    lt = list(lt)
    return lt

def saveFile(lt):
    print(f'[*] {len(lt)} domains found for {domain_name}\n')
    with open(f'{datetime.date.today()}-{domain_name}.txt','w') as file:
        for link in sorted(lt):
            file.write(link+"\n")
    file.close()

    
# ----------
# execution
# ----------

print('\n[*] Searching on rapiddns...')
time.sleep(1)
# rapid dns en premier
rapiddns = request_rdns(domain_name)
rdns_page_numbers = pageNum(rapiddns)
rdns_parsed = parsePage(rdns_page_numbers,rapiddns)

# puis crt.sh
print('-'*30)
print('[*] Trying to search domains on crt.sh')
subCrt = crtShReq(rdns_parsed,domain_name)
saveFile(subCrt)
print("[*] Please wait until the program finish.")
time.sleep(2)
print('-'*30)
print('Finished')


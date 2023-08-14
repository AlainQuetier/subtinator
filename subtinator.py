import requests
import datetime
import time

print('-'*30)
print('Subtinator: crt.sh extraction to txt')
print('-'*30+'\n')

crt_url="https://crt.sh/?q="
domain_name = input('Enter the domain to search (exemple: google.com): ')
output="&output=json"


print('\n[*] Searching...')
r = requests.get(crt_url+str(domain_name)+output)
extracted = r.json()

linktab=[]

if len(extracted) == 0:
    print("[-] No value found in crt.sh.")
else:
    print("[*] Values found!")
    time.sleep(2)
    print("[*] Please wait until the program finish.")
    time.sleep(2)
    for domain in range(len(extracted)):
        unformated_name = extracted[domain]['name_value']
        formated = unformated_name.split()[0]
        linktab.append(formated)
    linktab = set(linktab)
    linktab = list(linktab)
    print(f'[*] {len(linktab)} domains found for {domain_name}\n')
    #write in file
    with open(f'{datetime.date.today()}-{domain_name}.txt','w') as file:
        for link in sorted(linktab):
            file.write(link+"\n")
        file.close()

print('-'*30)
print('Finished')

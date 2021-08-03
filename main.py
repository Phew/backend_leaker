import sys, os, requests, ipapi, colorama, socket
import bs4 as BeautifulSoup

from colorama import Fore

#modules
from modules.banner import *
from modules.url_handling import UrlHandling
from modules.backend_leaks import BackEnd
from modules.dnsdumpster import DNSDumpsterAPI


colorama.init(convert=True)
os.system('cls')
print(BANNER)
URL = input(f' {Fore.CYAN}URL {Fore.WHITE}-->{Fore.WHITE} ')

TARGET = {
    "url": URL,
    "domain": "",
    "domain_ip": "",
    "favicon_hash": ""
}

def dnsdumpster(target):
    res = DNSDumpsterAPI(False).search(target)

    if res['dns_records']['host']:
        for entry in res['dns_records']['host']:
            provider = str(entry['domain'])
            if "cloudflare" not in provider or "ddos-guard" not in provider:
                ip = entry['ip']

                if "172." in ip or "103." in ip or "104." in ip or "23." in ip or "173." in ip:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found HOST: {Fore.WHITE}{entry['domain']}{entry['ip']} (CloudFlare)")
                else:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found HOST: {Fore.WHITE}{entry['domain']}{entry['ip']}")
    else:
        print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}]0 HOST records found!")

    if res['dns_records']['dns']:
        for entry in res['dns_records']['dns']:
            provider = str(entry['domain'])
            if "cloudflare" not in provider or "ddos-guard" not in provider:
                ip = entry['ip']
                if "172." in ip or "103." in ip or "104." in ip or "23." in ip or "173." in ip:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found DNS:{Fore.WHITE} {entry['domain']} {entry['ip']} (CloudFlare)")
                else:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found DNS:{Fore.WHITE} {entry['domain']} {entry['ip']}")
    else:
        print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}]0 DNS records found!")

    if res['dns_records']['mx']:
        for entry in res['dns_records']['mx']:
            provider = str(entry['domain'])
            if "cloudflare" not in provider or "ddos-guard" not in provider:
                ip = entry['ip']
                if "172." in ip or "103." in ip or "104." in ip or "23." in ip or "173." in ip:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found MX:{Fore.WHITE} {entry['domain']} {entry['ip']} (CloudFlare)")
                else:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found MX:{Fore.WHITE} {entry['domain']} {entry['ip']}")

    else:
        print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}]0 MX records found!")


def subdomain(URL):

    oop = URL.replace('https:', '').replace('/', '').replace('http:', '').replace('//', '')
    URL = 'https://www.virustotal.com/vtapi/v2/domain/report'
    params = {'apikey': "3efa6fc22eb53ade73ed29357896233fb1007d40c354afe0451a607f7157f64b", 'domain': oop}

    response = requests.get(URL, params=params)
    jdata = response.json()

    domains = sorted(jdata['subdomains'])
    try:
        io = jdata['undetected_referrer_samples'][1]['date']
    except:
        io = ""
        pass
    # print(jdata)
    for domain in domains:
        try:

            ip = socket.gethostbyname(domain)
        except:
            ip = f"None"
            pass



        try:
            stat = False

            if "172." in ip or "8." in ip or "103." in ip or "104." in ip or "23." in ip or "173." in ip:
                if "104" in ip:
                    stat = True
                stat = True

            if len(io) == 0:
                io = f"None"


            req = requests.get(f"https://{ip}/", timeout=10)
            soup = BeautifulSoup(req.text, 'html.parser')
            print(stat)
            if stat == True:
                print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} {domain}, IP: {ip}, ",
                      f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE}" + io + f"(CloudFlare/DDoS Prot)")
            else:
                oo = 0
                for title in soup.find_all('title'):
                    oo = title.get_text()
                if len(oo) == 0:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} {domain}, IP: {ip}, {Fore.WHITE}HeaderTitle: empty")
                else:
                    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} {domain}, IP: {ip}, {Fore.WHITE}HeaderTitle:{oo}")
        except:
           print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} {domain}, IP: {ip}, {Fore.WHITE}HeaderTitle: empty (CloudFlare)")
        if "172." in ip or "8." in ip or "103." in ip or "104." in ip or "23." in ip or "173." in ip:

                print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} {domain}, IP: {ip}, {Fore.WHITE}HeaderTitle: empty (CloudFlare/DDoS Prot)")



def main():
    os.system('cls; clear')
    print(BANNER)
    
    MainURLHandle = UrlHandling(URL)

    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE} Checking if URL is VALID (Format).")

    if MainURLHandle.CheckValid() == True:
        print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} URL is VALID")
    else:
        print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} URL is not valid to perform backend checks.")
        exit(0)

    print("")

    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE} Getting target information.")

    TARGET['domain'] = MainURLHandle.GetDomainFromUrl()
    TARGET['domain_ip'] = MainURLHandle.GetDomainIP()
    TARGET['favicon_hash'] = MainURLHandle.FaviconHash()
    ip_info = ipapi.location(f'{TARGET["domain_ip"]}')
    TARGET['ip_org2'] = ip_info['org']

    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} Url: {TARGET['url']}")
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} Domain: {TARGET['domain']}")
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} Domain IP: {TARGET['domain_ip']}")
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} IP Org: {TARGET['ip_org2']}")
    #print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} Resquest Content: {MainURLHandle.GetReponse()}")
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} Favicon Hash: {TARGET['favicon_hash']} (http.favicon.hash:{TARGET['favicon_hash']})")

    print("")

    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE} Testing for backend leaks.")
    print('[?] {"url", "return", "domain_ip", "status_code", "raw_connection", "protected_info"}')

    print("")
    
    BackEndTester = BackEnd(TARGET['url'])

    cPanelResults = BackEndTester.GetCpanel()
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}cPanel [{cPanelResults['url']} | {cPanelResults['return']} | {cPanelResults['domain_ip']}| {cPanelResults['raw_connection']}]")

    PhpmyadminResults = BackEndTester.Getphpmyadmin()
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}PhPmyAdmin [{PhpmyadminResults['url']} | {PhpmyadminResults['return']} | {PhpmyadminResults['domain_ip']}| {PhpmyadminResults['raw_connection']}]")

    RawConnBackendResults = BackEndTester.RawConnectionBackend()
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Raw Connection [{RawConnBackendResults['url']} | {RawConnBackendResults['return']} | {RawConnBackendResults['domain_ip']}| {RawConnBackendResults['raw_connection']}]")

    SSHBackEndResults = BackEndTester.SSHConnectionBackend()
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}SSH Backend [{SSHBackEndResults['url']} | {SSHBackEndResults['return']} | {SSHBackEndResults['domain_ip']}| {SSHBackEndResults['raw_connection']}]")

    MailmanBackEndResults = BackEndTester.CheckMailman()
    print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Mailman Backend [{MailmanBackEndResults['url']} | {MailmanBackEndResults['return']} | {MailmanBackEndResults['domain_ip']}| {MailmanBackEndResults['raw_connection']}| {MailmanBackEndResults['protected_info']}]")
    shodan = BackEndTester.shodain()
    try:
        #shodan()
        print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Shodan Backend [{shodan['url']} | {shodan['return']} | {shodan['domain_ip']}| {shodan['raw_connection']}| {shodan['protected_info']}]")
    except Exception as e:
        pass

    print("") 
    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE}Checking DNSDumpster API.")
    
    dnsdumpster(TARGET['domain'])
    print("")
    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE}Scanning for subdomains.")
    subdomain(URL)

    print("")
main()

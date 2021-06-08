import sys, os, requests, ipapi

import colorama
from colorama import Fore

#modules
from modules.url_handling import UrlHandling
from modules.backend_leaks import BackEnd
from modules.dnsdumpster import DNSDumpsterAPI


colorama.init(convert=True)
os.system('cls')
BANNER = f'''{Fore.MAGENTA}
   {Fore.MAGENTA}___           __    ____        __ {Fore.RED} __            __  
  {Fore.MAGENTA}/ _ )___ _____/ /__ / __/__  ___/ / {Fore.RED}/ /  ___ ___ _/ /__   {Fore.YELLOW} - github.com/Phew
 {Fore.MAGENTA}/ _  / _ `/ __/  '_// _// _ \/ _  / {Fore.RED}/ /__/ -_) _ `/  '_/   {Fore.YELLOW} - github.com/BlackRabbit-0
{Fore.MAGENTA}/____/\_,_/\__/_/\_\/___/_//_/\_,_/ {Fore.RED}/____/\__/\_,_/_/\_\ 
                                                         

                {Fore.YELLOW}- Oops gotcha backend!{Fore.RESET}
                
                
'''
print(BANNER)
URL = input(f' {Fore.YELLOW}URL {Fore.WHITE}-->{Fore.WHITE} ')

TARGET = {
    "url": URL,
    "domain": "",
    "domain_ip": "",
    "favicon_hash": ""
}

SETTINGS = {
    "subdomain_list": "lsts/subdomains.txt",
    "subdomains": []
}

DIR_SETTINS = {
    'directory_list': 'lsts/dirs.txt',
    'dirs': []

}

def dnsdumpster(target):
    res = DNSDumpsterAPI(False).search(target)

    if res['dns_records']['host']:
        for entry in res['dns_records']['host']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found HOST: {entry['domain']} | {str(entry['provider'])} | {entry['country']}")

    if res['dns_records']['dns']:
        for entry in res['dns_records']['dns']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found DNS: {entry['domain']} | {str(entry['provider'])} | {entry['country']}")

    if res['dns_records']['mx']:
        for entry in res['dns_records']['mx']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Found MX: {entry['domain']} | {str(entry['provider'])} | {entry['country']}")

def subdomain():
    discovered_subdomains = []
    
    for subdomain in SETTINGS['subdomains']:
            url = f"http://{subdomain}.{URL}".replace('https://', '')
            urlhandle = UrlHandling(url)

            try:
                requests.get(url)
            except requests.ConnectionError:
                #print(f"{Fore.RED}[+]{Fore.WHITE} Connection Error ({subdomain})")
                pass
            except Exception as e:
                #print(f"{Fore.RED}[+]{Fore.WHITE} Encountered error ({subdomain})")
                pass
            else:
                print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Discovered subdomain: {url} ({urlhandle.GetDomainIP()})")

                discovered_subdomains.append(url)

                with open(f"target_scans/discovered_subdomains_{TARGET['domain']}.txt", "w") as f:
                    for subdomain in discovered_subdomains:
                        print(subdomain, file=f)

def dirscanner():
    discovered_directory = []
    
    for directories in DIR_SETTINS['dirs']:
            url = f"http://{URL}/{directories}".replace('https://', '')
            urlhandle = UrlHandling(url)

            try:
                x = requests.get(url)
            except requests.ConnectionError:
                #print(f"{Fore.RED}[+]{Fore.WHITE} Connection Error ({subdomain})")
                pass
            except Exception as e:
                #print(f"{Fore.RED}[+]{Fore.WHITE} Encountered error ({subdomain})")
                pass
            else:
                bytes = len(UrlHandling(url).GetReponse())
                if x.status_code == 404:
                    #print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE} This might take awhile")
                    pass
                else:

                    print(f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Discovered Directory: {url} ({urlhandle.GetDomainIP()}) ({x.status_code}) ({bytes})")

                    discovered_directory.append(url)

                    with open(f"target_scans/discovered_directorie_{TARGET['domain']}.txt", "w") as f:
                        for directories in discovered_directory:
                            print(directories, file=f)


if __name__ == "__main__":
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
        shodan()
        print(f"{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}] {Fore.WHITE}Shodan Backend [{shodan['url']} | {shodan['return']} | {shodan['domain_ip']}| {shodan['raw_connection']}| {shodan['protected_info']}]")
    except Exception as e:
        pass

    print("") 
    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE}Checking DNSDumpster API.")
    
    dnsdumpster(TARGET['domain'])
    print("") 
    q = input(f'{Fore.MAGENTA}Do you want to scan for directories? (y/n):{Fore.WHITE} ')
    if q == "y":
        print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE}Scanning for Directories.")
        with open(DIR_SETTINS['directory_list'], encoding="utf-8", errors="ignore") as infile:
            for line in infile:
                DIR_SETTINS['dirs'].append(line.strip("\n"))

        dirscanner()
    print("") 
    y = input(f'{Fore.MAGENTA}Do you want to scan for Subdomains? (y/n):{Fore.WHITE} ')
    if y == 'y':
        print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE}Scanning for subdomains.")

        with open(SETTINGS['subdomain_list'], encoding="utf-8", errors="ignore") as infile:
            for line in infile:
                SETTINGS['subdomains'].append(line.strip("\n"))

        subdomain()

    print("")
    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE}Manual Checks.")
    print(f"{Fore.YELLOW}[{Fore.WHITE}!{Fore.YELLOW}] {Fore.WHITE}ZoomEyE, Shodan, Censys: DOMAIN + FAVICON(http.favicon.hash:HASH).")
    

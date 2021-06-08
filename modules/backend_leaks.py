import socket, re, requests, os, subprocess

import shodan
from shodan import Shodan
from bs4 import BeautifulSoup

#modules
from modules.url_handling import UrlHandling

class BackEnd:
    def __init__(self, target):
        self.target = target
    
    def GetCpanel(self):
        REQ_URL = f"{self.target}/cpanel"
        UrlHandler = UrlHandling(REQ_URL)
        
        try:
            cpanel = requests.get(REQ_URL)
            if cpanel.status_code == 404:
                return {
                    "url": REQ_URL,
                    "return": "error",
                    "domain_ip": "not found",
                    "raw_connection": "not found"
                }
            else:

                return {
                    "url": REQ_URL,
                    "return": "success",
                    "domain_ip": UrlHandler.GetDomainIP(),
                    "raw_connection": UrlHandler.RawConnection(),
                }
        except:
            return {
                "url": REQ_URL,
                "return": "error",
                "domain_ip": "not found",
                "raw_connection": "not found"
            }
    
    def Getphpmyadmin(self):
        REQ_URL = f"{self.target}/phpmyadmin"
        UrlHandler = UrlHandling(REQ_URL)
        
        try:
            phpmy = requests.get(REQ_URL)
            if phpmy.status_code == 404:
                return {
                    "url": REQ_URL,
                    "return": "error",
                    "domain_ip": "not found",
                    "raw_connection": "not found"
                }
            else:
                return {
                    "url": REQ_URL,
                    "return": "success",
                    "domain_ip": UrlHandler.GetDomainIP(),
                    "raw_connection": UrlHandler.RawConnection(),
                }
        except:
            return {
                "url": REQ_URL,
                "return": "error",
                "domain_ip": "not found",
                "raw_connection": "not found"
            }
    
    def RawConnectionBackend(self):
        REQ_URL = self.target
        UrlHandler = UrlHandling(REQ_URL)

        return {
            "url": REQ_URL,
            "return": "success",
            "domain_ip": UrlHandler.GetDomainIP(),
            "raw_connection": UrlHandler.RawConnection(),
        }


    def shodain(self):
        REQ_URL = self.target
        UrlHandler = UrlHandling(REQ_URL)
        try:
            API = Shodan("eutNHipEhVtJhBIGdzltWKOgOKOOmxJ6")
            results = API.search(REQ_URL)
            for result in results['matches']:

                return {
                     "url": REQ_URL,
                        "return": "success",
                        "domain_ip": UrlHandler.GetDomainIP(),
                        "raw_connection": UrlHandler.RawConnection(),
                        "protected_info": result['ip_str']
                }

        except shodan.APIError as e:
            return {
                "url": REQ_URL,
                "return": "error",
                "domain_ip": "not found",
                "raw_connection": "not found",
                "protected_info": "not found"
            }




    def SSHConnectionBackend(self):
        REQ_URL = self.target
        UrlHandler = UrlHandling(REQ_URL)

        try:
            SSHHost = socket.gethostbyname('ssh.'+UrlHandler.GetDomainFromUrl())

            return {
                "url": REQ_URL,
                "return": "success",
                "domain_ip": SSHHost,
                "raw_connection": SSHHost
            }
        except:
            return {
                "url": REQ_URL,
                "return": "error",
                "domain_ip": "not found",
                "raw_connection": "not found"
            }
    
    def CheckMailman(self):
        REQ_URL = f"{self.target}//mailman/listinfo/mailman"
        UrlHandler = UrlHandling(REQ_URL)
        
        try:
            r = requests.get(REQ_URL)
            if r.status_code == 404:

                return {
                    "url": REQ_URL,
                    "return": "error",
                    "domain_ip": "not found",
                    "raw_connection": "not found",
                    "protected_info": "not found"
                }
            else:

                soup = subprocess.getoutput(f"curl {REQ_URL} -s | findstr POST").split('"')[1].replace('/mailman/listinfo/mailman', '')


                return {
                    "url": REQ_URL,
                    "return": "success",
                    "domain_ip": UrlHandler.GetDomainIP(),
                    "raw_connection": UrlHandler.RawConnection(),
                    "protected_info": soup
                }
        except:
            return {
                "url": REQ_URL,
                "return": "error",
                "domain_ip": "not found",
                "raw_connection": "not found",
                "protected_info": "not found"
            }

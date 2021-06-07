import socket, re, requests, os
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
            requests.get(REQ_URL)

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
            requests.get(REQ_URL)
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
            soup = os.system(f"curl {REQ_URL} -s | findstr POST")

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

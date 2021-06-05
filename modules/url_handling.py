import re, requests, socket, codecs, mmh3
#mmh3
from urllib.parse import urlparse

class UrlHandling:
    def __init__(self, url):
        self.url = url
        self.regex = re.compile( # thanks https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    def CheckValid(self):
        return re.match(self.regex, self.url) is not None
    
    def CheckOnline(self):
        try:
            requests.get(self.url)
            return True
        except:
            return False
    
    def GetDomainFromUrl(self):
        return urlparse(self.url).netloc

    def GetDomainIP(self):
        domain = urlparse(self.url).netloc
        try:
            return socket.gethostbyname(domain)
        except:
            return "Not Found"
    
    def RawConnection(self):
        try:
            with requests.get(self.url, stream=True) as rsp:
                conn = rsp.raw._connection.sock.getpeername()

            return conn
            
        except:
            return "Not Found"
    
    def FaviconHash(self):
        try:
            r = requests.get(self.url+"/favicon.ico")
            favicon = codecs.encode(r.content,"base64")
            return str(mmh3.hash(favicon))

        except:
            return "Not Found"
    
    def GetReponse(self):
        try:
            r = requests.get(self.url)
            return r.text
        except:
            return "Not Found"
        




        

import mechanicalsoup
from enum import Enum

class CrawlerInfoBase():
    
    class TypeResult(Enum):
        REDIRECT = 0
        ITEMS = 1
    
    name = "BASE_ID"
    type = "UNDEFINED"
    browser = mechanicalsoup.StatefulBrowser()
    
    def run(self, params):
        ## abstratc method to override!
        return
    
    def getName(self):
        return self.name
    
    def getTypeAction(self):
        return self.type
import re
from core.CrawlerInfoBase import CrawlerInfoBase

class WikiPlant(CrawlerInfoBase):
    
    def __init__(self):
        self.name = "wikiplant"
        self.type = CrawlerInfoBase.TypeResult.REDIRECT
        
    def run(self, params):
        
        PREFIX_FILTER_URL = "www.gardenology.org/wiki"
        
        self.browser.open("https://www.google.com/")

        first_label = params["result"]["recognition"][0]["label"].split(", ")[0]
        input_search = first_label
        
        # Fill-in the form
        self.browser.select_form('form[action="/search"]')
        self.browser["q"] =  input_search +" site:" + PREFIX_FILTER_URL
        self.browser.submit_selected(btnName="btnG")
        
        # Display links
        for link in self.browser.links():
            target = link.attrs['href']
            # Filter-out unrelated links and extract actual URL from Google's
            # click-tracking.
            if (target.startswith('/url?') and not target.startswith("/url?q=http://webcache.googleusercontent.com")):
                target = re.sub(r"^/url\?q=([^&]*)&.*", r"\1", target)
                print(target)
                if input_search.lower() in target.lower() : 
                    print(target)
                    return target
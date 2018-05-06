from core.CrawlerInfoBase import CrawlerInfoBase

class Wiki(CrawlerInfoBase):
    
    def __init__(self):
        self.name = "wiki"
        self.type = CrawlerInfoBase.TypeResult.REDIRECT
    
    def run(self, params):
        
        first_label = params["result"]["recognition"][0]["label"].split(", ")[0]
        input_search = first_label
        
        input_search = input_search.replace(" ", "+")
        self.browser.open("http://en.wikipedia.com/wiki?search=" + input_search )
        
        # .searchresults     https://en.wikipedia.com/wiki?search=dog+chiwawa
        
        output = []
        
        curr_url = self.browser.get_url()
        
        ## fa match su un risultato prefissato, prendi il link del redirect
        if curr_url.find('wiki?search') < 0 :
            #print "curr_url : " + curr_url
            output.append(curr_url)
        
        ## altrimenti perndi il primo link tra i risultati della ricerca
        else :
            first_link = "http://en.wikipedia.com" + self.browser.get_current_page().select(".mw-search-results a")[0].attrs['href']
            #print "first_link : " + first_link
            output.append(first_link)
            
        return output
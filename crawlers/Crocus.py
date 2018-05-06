import re
from core.CrawlerInfoBase import CrawlerInfoBase
from core import SIFTImageCompare
from pprint import pprint

# memo : non funziona la SIFT sulle immagini di crocus
class Crocus(CrawlerInfoBase):
    
    def __init__(self):
        self.name = "crocus"
        self.type = CrawlerInfoBase.TypeResult.ITEMS
    
    def run(self, params):
        
        first_label = params["result"]["recognition"][0]["label"].split(", ")[0]
        
        
        URL_PATTERN = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        URL_BASE = "https://www.crocus.co.uk"
        input_search = first_label
        
        self.browser.open("https://www.crocus.co.uk/search/_/?se=all&searchType=all&searchBox=" + input_search + "&search=search")

        output = []
        tmp_links_img = {}

        for elem in self.browser.get_current_page().select('div[itemtype="http://schema.org/Product"]'):
            
            
            link = URL_BASE + elem.select("a")[0].attrs['href']
            style_img = elem.select(".results-image-container")[0].attrs['style']
            url_img = re.findall(URL_PATTERN, style_img)[0]
                        
            #print("link :: " + link)
            
            tmp_links_img[url_img] = link
            

        
        pprint(tmp_links_img)
        
        linkUrlImages = tmp_links_img.keys()
        rank_results = SIFTImageCompare.multipleCompareFromURL(linkUrlImages, params["path"])
        #ordered_rank_result = collections.OrderedDict(sorted(rank_results.items()))
        
        
        for img, rank in sorted(rank_results.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            output.append({ "link" : tmp_links_img[img], "url_img" : img, "rank": rank  })
        
        
        return output
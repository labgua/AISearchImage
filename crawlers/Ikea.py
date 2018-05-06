import json
from core.CrawlerInfoBase import CrawlerInfoBase
from core import SIFTImageCompare
from pprint import pprint

# memo : ok funziona
class Ikea(CrawlerInfoBase):
    
    def __init__(self):
        self.name = "ikea"
        self.type = CrawlerInfoBase.TypeResult.ITEMS
     
    def run(self, params):
        
        first_label = params["result"]["recognition"][0]["label"].split(", ")[0]
        
        URL_BASE = "http://www.ikea.com"
        input_search = first_label
        input_search = input_search.replace(" ", "+")
        
        self.browser.open("http://www.ikea.com/gb/en/search/?k=" + input_search )
        
        output = []
        tmp_links_img = {}
        
        for elem in self.browser.get_current_page().select(".Product_Compact.item") : 
            
            img_set_json = elem.select_one('img').attrs['data-srcset']
            img_set = json.loads(img_set_json)
            first_img = img_set.values()[0]
            
            
            url_img = URL_BASE + first_img
            #pprint("url_img (src) :: " + url_img)
            url_img = url_img.encode('unicode-escape')
            url_img = url_img.replace("/\\", "/")
            url_img = url_img.replace("\\", "/")
            
            link = URL_BASE + elem.select_one('a').attrs['href']
            
            
            tmp_links_img[url_img] = link
        
        
        linkUrlImages = tmp_links_img.keys()
        rank_results = SIFTImageCompare.multipleCompareFromURL(linkUrlImages, params["path"])
        #ordered_rank_result = collections.OrderedDict(sorted(rank_results.items()))
        
        
        for img, rank in sorted(rank_results.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            output.append({ "link" : tmp_links_img[img], "url_img" : img, "rank": rank  })
        
        
        #for img, rank in ordered_rank_result.items():
        #    output.append({ "link" : tmp_links_img[img], "url_img" : img, "rank": rank  })
        
        
        return output
        
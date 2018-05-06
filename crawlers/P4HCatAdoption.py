import re
from core.CrawlerInfoBase import CrawlerInfoBase
from pprint import pprint
from core import SIFTImageCompare

class P4HCatAdoption(CrawlerInfoBase):
    
    def __init__(self):
        self.name = "p4hcatadoption"
        self.type = CrawlerInfoBase.TypeResult.ITEMS
    
    def run(self, params):
        
        first_label = params["result"]["recognition"][0]["label"].split(", ")[0]
        
        FILTER_URL_SEARCH = "https://www.pets4homes.co.uk/cat-breeds/"
        PREFIX_URL_ADOPTION = "https://www.pets4homes.co.uk/adoption/cats"
        
        output = []
        tmp_links_img = {}
        
        input_search = first_label
        
        self.browser.open("https://www.google.com/")
        
        self.browser.select_form('form[action="/search"]')
        self.browser["q"] = input_search +" site:pets4homes.co.uk/cat-breeds"
        self.browser.submit_selected(btnName="btnG")
        
        links = self.browser.links()
        first_link = None
        
        
        for l in links:
            
            target = l.attrs['href']
            
            if (target.startswith('/url?') and not target.startswith("/url?q=http://webcache.googleusercontent.com")) :
                target = re.sub(r"^/url\?q=([^&]*)&.*", r"\1", target)
                ###pprint(target)
                if target.startswith( FILTER_URL_SEARCH ) :
                    first_link = target
                    break
        
        if first_link == None:
            return output
        
        # 1passo
        # costruisci il link per l'adozione dei gatti
        # del tipo """https://www.pets4homes.co.uk/adoption/cats/<<CODICE CANE>>/"""
        # calcolando il codice partendo dal link fist_link
        code_category_p4h = first_link[ len(FILTER_URL_SEARCH): ]
        url_adoption = PREFIX_URL_ADOPTION + "/" + code_category_p4h
        
        ###print "url_adoption :: " + url_adoption
        
        # 2passo
        # aprire la pagina
        self.browser.open(url_adoption)
        
        # 3passo
        # leggere dal risultato tutti i link e le immagini associate
        items_adoption = self.browser.get_current_page().select('[itemtype="http://schema.org/Product"]')
        ###pprint(items_adoption)
        
        for i in items_adoption:
            link = i.select_one("a").attrs['href']
            url_img = i.select_one("img").attrs['src']
            
            if url_img.startswith("//") :
                url_img = "http://" + url_img.replace("//", "")
            
            
            tmp_links_img[url_img] = link
            #rank = SIFTImageCompare.compareFromURL(url_img, params["path"])
            
            #output.append({ "link" : link, "url_img" : url_img, "rank": rank })

        pprint(tmp_links_img)
        
        linkUrlImages = tmp_links_img.keys()
        rank_results = SIFTImageCompare.multipleCompareFromURL(linkUrlImages, params["path"])
        
        for img, rank in sorted(rank_results.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            output.append({ "link" : tmp_links_img[img], "url_img" : img, "rank": rank  })
        
        
        # 4passo
        # restituire i link e le immagini
        return output
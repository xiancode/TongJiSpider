#!/usr/bin/python
#encoding:utf-8

#from items              import TutorialItem
#from scrapy.selector    import Selector

from urlparse                       import urlparse
from scrapy.http                    import Request
from string                         import find,replace
from scrapy.contrib.spiders         import CrawlSpider
import scrapy.cmdline
import os


def loadsites(filename):
    """
    """
    sites = []
    fin = open(filename)
    text = fin.readlines()
    for line in text:
        sites.append(line.strip())
    return sites


class MySpider(CrawlSpider):
    name         = "TongJiSpider"
    #allowed_domains    = ["www.stats.gov.cn"]
    #start_urls    = ["http://www.stats.gov.cn/tjsj/tjgb/"]
    start_urls = loadsites("Site.txt")
    #keywords = ["国名经济","经济发展","社会发展","统计公报","报告"]
    #rules = (
    #         Rule(LinkExtractor(allow = (),deny = () )),
    #         Rule(LinkExtractor(allow = ()),callback = 'parse_title' ),
    #      )

    def parse(self, response):
        #print response.url
        links   = response.xpath('//a/@href').extract()
        dom = self.getdomsuffix(response)
        #title = response.xpath('//head//title/text()').extract()
        #titletext = "".join(title)
        #for word in self.keywords:
        #    if find(titletext,word.decode('utf-8')) != -1:
        #        self.download(response)
        #        break
        
        self.download(response)
        crawledLinks = []

        
        for link in links:
            fullurl = ""
            if not link in crawledLinks:
                if link[:2] == "./":
                    fullurl = response.url + link[2:].strip()
                elif link[0] == "/":
                    fullurl = dom + link[1:].strip()
                elif link.endswith("html"):
                    fullurl = link
                #makesure url  under the current start url fold
                if find(fullurl,response.url) != -1:
                        crawledLinks.append(fullurl) 
            else:
                continue  
        for link in crawledLinks:
            yield Request(link,self.parse)
            
            
    def parse_title(self,response):
        """
        """
        pass
                         
    def download(self,response):
        """
        download the page
        """ 
        filename = self.getfilename(response)
        with open(filename,'wb') as f:
            f.write(response.body)
            
    def getdomsuffix(self,response):
        """
        """
        o = urlparse(response.url)
        return o[0] + "://" +  o[1] + "/"
        
    def getfilename(self,response):
        """
        return the page name
        """
        fullurl = ""
        if response.url[-1] =="/" or response.url[-1] =="\\":
            fullurl += response.url + "index.html"
        else:
            fullurl = response.url
        o = urlparse(fullurl)
        pathname = o[1] + o[2]
        ldir = os.path.dirname(pathname)
        if os.sep!='/':
            ldir=replace(ldir,'/',os.sep)
            pathname=replace(pathname,'/',os.sep)
        
        #print ldir    
        if os.path.isdir(ldir):
            pass
        else:
            if os.path.exists(ldir):
                pass
            else:    
                os.makedirs(ldir)
        return pathname
                    
                               
def main():
    #scrapy.cmdline.execute(argv=['scrapy','crawl','nettuts','-o','data.csv','-t','csv']) 
    scrapy.cmdline.execute(argv=['scrapy','crawl','TongJiSpider']) 
     
          
                        
if __name__ == "__main__":
    main()

    
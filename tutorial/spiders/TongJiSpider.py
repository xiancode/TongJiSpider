#!/usr/bin/python
#encoding:utf-8

#from items              import TutorialItem
#from scrapy.selector    import Selector

from urlparse                       import urlparse
from scrapy.http                    import Request
from scrapy.selector                import Selector
from string                         import find,replace
from scrapy.contrib.spiders         import CrawlSpider
from bs4                            import BeautifulSoup 
import scrapy.cmdline
import os,sys,re


def loadsites(filename):
    """
    """
    sites = []
    fin = open(filename)
    text = fin.readlines()
    for line in text:
        sites.append(line.strip())
    return sites

def getcurdir():
    path = sys.path[0]
    #
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

class MySpider(CrawlSpider):
    name         = "TongJiSpider"
    #allowed_domains    = ["www.stats.gov.cn"]
    #start_urls    = ["http://www.stats.gov.cn/tjsj/tjgb/"]
    cur_dir = getcurdir()
    #start_urls = loadsites(cur_dir + os.sep +  "Site.txt")
    start_urls = loadsites("D:\\data\\Site.txt")
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
            #f.write(response.body)
            soup = BeautifulSoup(response.body)
            #text = response.selector.xpath('//span/text()').extract()
            text = soup.get_text().replace('\n','')
            #para = soup.html.find_all('p')
            #html = soup.prettify("utf-8")
            #html = ""
            #for p in para:
            #    html += p + "\n"
            #html = ''.join(para)
            #text = re.sub('<[^>]+>','',html)
            #text = re.sub('\n','',text)
            #text = re.sub('\\r','',text)
            text_str = ''.join(text)
            f.write(text_str.encode('GB18030'))
            
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
        #pathname = o[1] + o[2]
        pathname = "D:\\data" + os.sep +   o[1] + o[2]
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
        if pathname.endswith(".html"):
            pathname = pathname[:-5] + ".txt" 
        return pathname
                    
                               
#def main():
    #scrapy.cmdline.execute(argv=['scrapy','crawl','nettuts','-o','data.csv','-t','csv']) 
    #print getcurdir()
#    scrapy.cmdline.execute(argv=['scrapy','crawl','TongJiSpider']) 
          
                        
#if __name__ == "__main__":
#    main()

    

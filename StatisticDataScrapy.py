from os import system
import scrapy
import tutorial

def execute(cmd):
    system(cmd)
    
execute("scrapy crawl TongJiSpider")
from gc import callbacks
from re import M
from typing import overload
import scrapy;

class GpuSpider(scrapy.Spider):
    name = "gpu"
    start_urls = [
        'https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966937&myStore=false',
    ]
    current_url = ''

    def parse(self, response):

        yield response.follow(self.start_urls[0], callback=self.parsePage)
        for page in response.css('div.pagination a::attr(href)'):
            yield response.follow(page.get(), callback=self.parsePage)

    def parsePage(self, response):
        for gpu_link in response.css('li.product_wrapper a[class*=ProductLink]::attr(href)'):
            yield response.follow(gpu_link.get(), callback=self.parseSpecs)

    def parseSpecs(self, response):
        self.current_url = response.url
        specs = response.css('main')
        for spec in specs:
            yield {
                'Name': spec.css('span[class*=ProductLink]::attr(data-name)').get(),
                'Price': spec.css('span[class*=ProductLink]::attr(data-price)').get(),
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[7]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[7]/div[2]/text()').get(),     #GPU Manufacturer
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[8]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[8]/div[2]/text()').get(),     #Number of GPUs
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[9]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[9]/div[2]/text()').get(),     #GPU Chipset
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[10]/div[1]/text()').get() : spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[10]/div[2]/text()').get(),  #Overclocked
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[11]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[11]/div[2]/text()').get(),   #Boost Core Clock Speed
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[12]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[12]/div[2]/text()').get(),   #Cuda processors
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[13]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[13]/div[2]/text()').get(),   #PCIe Bandwidth
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[14]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[14]/div[2]/text()').get(),   #Max Monitors Supported
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[16]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[16]/div[2]/text()').get(),   #Video memory
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[17]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[17]/div[2]/text()').get(),   #Memory type
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[18]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[18]/div[2]/text()').get(),   #Memory bus
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[20]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[20]/div[2]/text()').get(),   #Led Color
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[21]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[21]/div[2]/text()').get(),   #Color
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[22]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[22]/div[2]/text()').get(),   #VR Ready
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[23]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[23]/div[2]/text()').get(),   #OpenGL Support
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[24]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[24]/div[2]/text()').get(),   #Direct X support
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[25]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[25]/div[2]/text()').get(),   #PCB color
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[26]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[26]/div[2]/text()').get(),   #HDCP Support
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[27]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[27]/div[2]/text()').get(),   #3D ready
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[34]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[34]/div[2]/text()').get(),   #Interface
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[30]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[30]/div[2]/text()').get(),   #HDMI ports
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[31]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[31]/div[2]/text()').get(),   #Displayport
                spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[37]/div[1]/text()').get(): spec.xpath('//*[@id="tab-specs"]/div/div[2]/div[37]/div[2]/text()').get()    #Recommended power supply
            }

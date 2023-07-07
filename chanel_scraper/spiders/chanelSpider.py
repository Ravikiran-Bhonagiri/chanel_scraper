import scrapy
import re


class ChanelspiderSpider(scrapy.Spider):
    name = "chanelSpider"
    allowed_domains = ["chanel.com"]
    start_urls = ["https://www.chanel.com"]

    def parse(self, response):
        # Extract text and attributes from the HTML snippet
        elements = response.css('li.cc-nav-item')

        for element in elements:
            text = element.css('a::text').get()
            href = element.css('a::attr(href)').get()

            if href is not None and len(href.split('/')) > 5:
                #print(href)
                #print(href.split('/'))
                yield response.follow(href, callback=self.parse_category_page)


    def parse_category_page(self, response):

        print(response.url)

        class_name_pattern1 = re.compile(r'Text_root__\w+')
        class_name_pattern2 = re.compile(r'CTA_root__\w+')

        if response.url in ['https://www.chanel.com/ww/haute-couture/']:
            for span in response.css('h2 span'):
                class_names = span.attrib.get('class')
                if class_names and class_name_pattern1.match(class_names):
                    print(span.css('::text').get())

            for a in response.css('a'):
                class_names = a.attrib.get('class')
                if class_names and class_name_pattern2.match(class_names):
                    print(a)
                    href = a.css('::attr(href)').get()
                    if href is not None:
                        yield response.follow(href, callback=self.parse_leaf_category_page)
                           
        

    def parse_leaf_category_page(self, response):
        
        yield{
            'url': response.url,
            'data': response.css('p.fs-text__content::text').getall(),
            }
        

        
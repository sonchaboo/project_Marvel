import scrapy
from ..items import UniItem
from scrapy.selector import Selector
from datetime import datetime

class MarvelOrg(scrapy.Spider):

    name = "MO"

    allowed_domains = ["marvelcinematicuniverse.fandom.com"]
    start_urls = ["https://marvelcinematicuniverse.fandom.com/ru/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9E%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8"]

    def __init__(self, ver='', **kwargs):
        self.ver = ver

    def parse(self, response):
        for item in response.css('.category-page__member-link').xpath('@href'):
            yield response.follow(item, self.parse2)

    def parse2(self, response):
        org = response.css('center font::text').get() 
        dct = {}
        # получаю все должности (члены, основатели, тд)
        roles = response.css('.pi-item.pi-data.pi-item-spacing.pi-border-color b::text').extract()
        for i, name in enumerate(response.css('.pi-item.pi-data.pi-item-spacing.pi-border-color')):
            dct[roles[i]] = name.css('a::text').extract()
        final_names = []
        for r in dct.keys():
            if r in ['Члены', 'Основатель', 'Глава', 'Бывшие руководители', 'Бывшие члены']:
                for nm in dct[r]:
                    final_names.append([r, nm])
        for nm in final_names:
            yield {
                'Org': org,
                'Role': nm[0],
                 'Name': nm[1]
            }

class MarvelPers(scrapy.Spider):

    name = "MOP"

    allowed_domains = ["marvelcinematicuniverse.fandom.com"]
    start_urls = ["https://marvelcinematicuniverse.fandom.com/ru/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9E%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8"]

    def __init__(self, ver='', **kwargs):
        self.ver = ver

    def parse(self, response):
        for item in response.css('.category-page__member-link').xpath('@href'):
            yield response.follow(item, self.parse2)

    def parse2(self, response):
        # получаю все должности (члены, основатели, тд)
        # roles = response.css('.pi-item.pi-data.pi-item-spacing.pi-border-color b::text').extract()
        for i, name in enumerate(response.css('.pi-item.pi-data.pi-item-spacing.pi-border-color a').xpath('@href')):
            yield response.follow(name, self.parse3)


    def parse3(self, response):
            # response.css('.pi-data-label.pi-secondary-font b::text').extract()
            dct = {}
            name = response.css('.page-header__title::text').get()
            # получаю все фичи
            roles = response.css('.pi-item.pi-data.pi-item-spacing.pi-border-color b::text').extract()
            for i, name in enumerate(response.css('.pi-data-value.pi-font::text, .pi-data-value.pi-font a::text').extract()):
                if i <= 4:
                    dct[roles[i]] = name # name.css('a::text').get()
            final = []
            for r in dct.keys():
                if r == 'Настоящее имя':
                    n = dct[r]
                # if r in ('Вид', 'Гражданство', 'Пол', 'Статус'):
                final.append([r, dct[r]])
            for i, nm in enumerate(final):
                yield {
                    'name': n,
                    'feature': nm[0],
                    'what': nm[1]
                }
                
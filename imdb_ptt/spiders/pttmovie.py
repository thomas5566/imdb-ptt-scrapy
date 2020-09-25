import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from imdb_ptt.items import MoviePttItem


class PttmovieSpider(CrawlSpider):
    name = 'pttmovie'
    rotate_user_agent = True
    
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/movie/index.html']

    custom_settings = {
        'ITEM_PIPELINES': {'imdb_ptt.pipelines.PttMoviePttPipeline': 100, },
        'CLOSESPIDER_ITEMCOUNT': 150,
    }

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='title']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='btn-group btn-group-paging']/a[2]"))
    )

    def parse_item(self, response):
        i = MoviePttItem()
        i['title'] = response.xpath(
            "normalize-space((//span[@class='article-meta-value'])[3]/text())").extract()
        # i['title'] = ''.join(title)

        i['author'] = response.xpath(
            "(//span[@class='article-meta-value'])[1]/text()").extract()
        # i['author'] = ''.join(author)

        i['date'] = response.xpath(
            "(//span[@class='article-meta-value'])[4]/text()").extract()
        # i['date'] = ''.join(date)

        i['contenttext'] = response.xpath(
            "//div[@id='main-content']/text()").extract()

        return i

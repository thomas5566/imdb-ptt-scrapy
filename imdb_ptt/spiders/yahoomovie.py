import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from imdb_ptt.items import YahooPttItem


class YahoomovieSpider(CrawlSpider):
    name = 'yahoomovie'
    allowed_domains = ['yahoo.com.tw']

    IMAGE_DIR = 'D:\\Users\\Administrator\\gb5566\\imdb_ptt\\media\\movie\\images'

    custom_settings = {
        "IMAGES_STORE": IMAGE_DIR,
        'ITEM_PIPELINES': {'imdb_ptt.pipelines.ImdbPttPipeline': 100,
                           'imdb_ptt.pipelines.CustomImagePipeline': 200,
                           },
    }
    start_urls = ['https://movies.yahoo.com.tw/movie_intheaters.html?page=1']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='release_movie_name']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='nexttxt']/a"))
    )

    def parse_item(self, response):
        i = YahooPttItem()
        title = response.xpath(
            "normalize-space(//div[@class='movie_intro_info_r']/h1/text())").extract()
        i['title'] = ''.join(title)

        critics_consensus = response.xpath(
            "normalize-space(//span[@id='story']/text())").extract()
        i['critics_consensus'] = ''.join(
            [i.replace(u'\xa0', u'') for i in critics_consensus])

        i['date'] = response.xpath(
            "//div[@class='movie_intro_info_r']/span[1]/text()").extract

        duration = response.xpath(
            "//div[@class='movie_intro_info_r']/span[2]/text()").extract()
        i['duration'] = ''.join([i.replace(u'\\u3000\\', u'')
                                 for i in duration])

        i['genre'] = response.xpath(
            "normalize-space((//div[@class='level_name'])[2]/a/text())").extract()
        # i['rating'] = response.css(
        #     '.ratingValue ::text').extract()[1]
        i['rating'] = response.xpath(
            "//div[@class='score_num count']/text()").extract()
        i['amount_reviews'] = response.xpath(
            "//div[@class='circlenum']/div[@class='num']/span/text()").extract()
        url = response.xpath(
            "//div[@class='movie_intro_foto']/img/@src").extract()
        link = ''.join(url)
        i['images'] = {i['title']: link}
        return i

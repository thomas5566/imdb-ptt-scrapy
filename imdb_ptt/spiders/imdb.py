import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from imdb_ptt.items import ImdbPttItem


class ImdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    IMAGE_DIR = 'D:\\Users\\Administrator\\gb5566\\imdb_ptt\\media\\movie\\images'

    custom_settings = {
        "IMAGES_STORE": IMAGE_DIR,
        'ITEM_PIPELINES': {'imdb_ptt.pipelines.ImdbPttPipeline': 100,
                           'imdb_ptt.pipelines.CustomImagePipeline': 200,
                           },
    }
    start_urls = [
        'https://www.imdb.com/search/title/?year=2020&title_type=feature&ref_=tt_ov_inf']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//div[@class='desc']/a)[1]"))
    )

    def parse_item(self, response):
        i = ImdbPttItem()
        title = response.xpath(
            "normalize-space(//div[@class='title_wrapper']/h1/text())").extract_first()
        i['title'] = ''.join(title.replace(u'\xa0', u''))
        i['critics_consensus'] = response.xpath(
            "normalize-space(//div[@class='summary_text']/text())").extract()
        i['date'] = response.xpath(
            "//span[@id='titleYear']/a/text()").extract
        i['duration'] = response.xpath(
            "normalize-space((//time)[1]/text())").extract()
        i['genre'] = response.xpath(
            "//div[@class='subtext']/a[1]/text()").extract()
        # i['rating'] = response.css(
        #     '.ratingValue ::text').extract()[1]
        i['rating'] = response.xpath(
            "//span[@itemprop='ratingValue']/text()").extract()
        amount_reviews = response.xpath(
            "//span[@class='small']/text()").extract()
        i['amount_reviews'] = [str(x.replace(',', '')) for x in amount_reviews]
        url = response.xpath(
            "//div[@class='poster']/a/img/@src").extract()
        link = ''.join(url)
        i['images'] = {i['title']: link}
        return i

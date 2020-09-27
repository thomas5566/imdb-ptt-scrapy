# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from movie_star.models import Movie
from movie_star.models import PttMovie


class ImdbPttItem(DjangoItem):
    django_model = Movie
    # title = scrapy.Field()
    # critics_consensus = scrapy.Field()
    # date = scrapy.Field()
    # duration = scrapy.Field()
    # genre = scrapy.Field()
    # rating = scrapy.Field()
    # amount_reviews = scrapy.Field()
    # average_grade = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()


class YahooPttItem(DjangoItem):
    django_model = Movie


class MoviePttItem(DjangoItem):
    django_model = PttMovie

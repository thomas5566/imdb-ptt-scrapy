# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django.db.utils import IntegrityError
from itemadapter import ItemAdapter
from movie_star.models import Movie
from movie_star.models import PttMovie
import scrapy
import os
import re

from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from urllib.parse import urljoin
from .items import Movie
from .items import MoviePttItem

from datetime import datetime
from decimal import Decimal


def clean_ptttitle(param):
    try:
        for s in param:
            if "雷" in s:
                return "".join(param)
    except IntegrityError:
        return None


def clean_title(param):
    return "".join(param)


def clean_critics_consensus(param):
    return "".join(param)


def clean_date(param):
    regex = "[^0-9\-]+"
    param = re.sub(regex, "", str(param))
    return param


def clean_duration(param):
    try:
        return "".join(param.split())
    except:
        return "".join(param)


def clean_genre(param):
    return "".join(param)


def clean_rating(param):
    return "".join(param)


def clean_images(param):
    if param:
        try:
            param = param[0]["path"]
        except TypeError:
            pass
    return param
    # return "".join(param)


def clean_amount_reviews(param):
    regex = "[^A-Za-z0-9]+"
    param = re.sub(regex, "", str(param))
    return "".join(param)


def clean_author(param):
    return "".join(param)


def clean_contenttext(param):
    return "".join(param)


class ImdbPttPipeline:
    def process_item(self, item, spider):
        movie = Movie()
        movie.title = clean_title(item["title"])
        movie.critics_consensus = clean_critics_consensus(item["critics_consensus"])
        movie.date = clean_date(item["date"])
        movie.duration = clean_duration(item["duration"])
        movie.genre = clean_genre(item["genre"])
        movie.rating = clean_rating(item["rating"])
        movie.images = clean_images(item["images"])
        movie.amount_reviews = clean_amount_reviews(item["amount_reviews"])
        movie.save()

        return item


class PttMoviePttPipeline:
    def process_item(self, item, spider):
        moviePtt = PttMovie()
        moviePtt.title = clean_ptttitle(item["title"])
        moviePtt.author = clean_author(item["author"])
        moviePtt.date = clean_date(item["date"])
        moviePtt.contenttext = clean_contenttext(item["contenttext"])
        if moviePtt.title is not None:
            moviePtt.save()

        return item


class CustomImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # for (image_url, image_name) in zip(item['images'], item['title']):
        #     yield scrapy.Request(url=image_url, meta={"image_name": image_name})
        if "images" in item:
            for img_name, image_url in item["images"].items():
                request = scrapy.Request(url=image_url)
                new_img_name = ("%s.jpg" % (img_name)).replace(" ", "")
                request.meta["img_name"] = new_img_name
                yield request

    def file_path(self, request, response=None, info=None):
        return request.meta["img_name"]
        # return os.path.join(info.spider.IMAGE_DIR, request.meta["img_name"])

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item


class DeleteNullTitlePipeline(object):
    def process_item(self, item, spider):
        title = item["title"]
        if title:
            return item
        else:
            raise DropItem("found null title %s", item)


class DuplicatesTitlePipeline(object):
    def __init__(self):
        self.movie = set()

    def process_item(self, item, spider):
        title = item["title"]
        if title in self.movie:
            raise DropItem("duplicates title found %s", item)
        self.movie.add(title)
        return item

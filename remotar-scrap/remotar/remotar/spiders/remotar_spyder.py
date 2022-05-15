import scrapy
import re
from remotar.items import RemotarItem
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class RemotarSpider(scrapy.Spider):
    name = "remotar"
    # allowed_domains = ["remotar.com.br/"]

    def start_requests(self):
        urls = ["https://remotar.com.br/vagas/"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for job in response.css("article.loadmore-item"):

            item = RemotarItem()
            job_url = job.css("a.job-details-link::attr(href)").get()

            url = job.css("a.job-details-link::attr(href)").get()
            title = job.css("div.loop-item-content h2.loop-item-title a::text").get()

            link = job.css("a.job-details-link::attr(href)").get()
            type = job.css(
                "div.loop-item-content p.content-meta span.job-type span::text"
            ).get()
            company = job.css(
                "div.loop-item-content p.content-meta span.job-company span::text"
            ).get()
            category = job.css(
                "div.loop-item-content p.content-meta span.job-category a::text"
            ).get()

            date = job.css(
                "div.loop-item-content p.content-meta span.job-date time::attr(datetime)"
            ).get()

            if title is not None:
                item["title"] = title
            else:
                item["title"] = ""

            if link is not None:
                item["link"] = link
            else:
                item["link"] = ""

            if type is not None:
                item["type"] = type
            else:
                item["type"] = ""

            if company is not None:
                item["company"] = company
            else:
                item["company"] = ""

            if category is not None:
                item["category"] = category
            else:
                item["category"] = ""

            if date is not None:
                item["date"] = date
            else:
                item["date"] = ""

            yield scrapy.Request(
                url=job_url,
                callback=self.parse_job_description,
                meta={"item": item},
            )

        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_job_description(self, response):

        item = response.meta["item"]
        # raw = response.css("div.description::text").get()

        # if raw is '':
        raw = response.css("div.description__about").get()
        if raw is None:
            raw = response.css("div.job-desc").get()

        raw = remove_tags(raw)
        regex = re.compile(r"[\n\r\t]")
        output = regex.sub("", raw)

        item["description"] = output

        return item

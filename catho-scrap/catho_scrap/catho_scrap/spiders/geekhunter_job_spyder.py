import scrapy
import re


class CathoJobSpider(scrapy.Spider):
    name = "geekhunter"

    def start_requests(self):
        urls = [
            "https://www.geekhunter.com.br/vagas",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = 1
        for job in response.css("ul li article article div div h2"):

            yield {
                "url": job.css("a::attr(href)").get(),
                "title": job.css("a::text").get(),
                "job_id": int(re.findall(r"\d+", job.css("a::attr(href)").get())[0]),
            }
            page += 1
            next_page = "&page={}".format(page)

            response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)
            # next_page = response.urljoin(next_page)
            # print("PAgina: {page}")
            # yield scrapy.Request(next_page, callback=self.parse)

import scrapy
import re
from catho_scrap.items import CathoScrapItem
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class CathoJobSpider(scrapy.Spider):
    name = "cathojob"

    def start_requests(self):
        urls = [
            "https://www.catho.com.br/vagas/tecnologia/?q=Tecnologia&page=1",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = 1

        # print(f"URL da Pagina: {next_page}")
        for job in response.css("ul li article article div div h2"):
            print(f"PAgina Interacao: {page}")
            item = CathoScrapItem()

            link = job.css("a::attr(href)").get()
            title = job.css("a::text").get()

            # yield {
            #     "url": job.css("a::attr(href)").get(),
            #     "title": job.css("a::text").get(),
            #     "job_id": int(re.findall(r"\d+", job.css("a::attr(href)").get())[0]),
            # }

            item["link"] = link
            item["title"] = title

            yield scrapy.Request(
                url=link,
                callback=self.parse_job_description,
                meta={"item": item},
            )
        page += 1

        # next_page = "?q=Tecnologia&page={}".format(page)

        next_page = "".join("".join([i for i in response.url if not i.isdigit()]))
        page = "".join([i for i in response.url if i.isdigit()])
        page = int(page) + 1
        abs_url = next_page + str(page)

        if next_page is not None:
            # next_page = response.urljoin(next_page)
            yield response.follow(abs_url, callback=self.parse)
        # next_page = response.urljoin(next_page)

        # yield scrapy.Request(next_page, callback=self.parse)

    def parse_job_description(self, response):
        item = response.meta["item"]
        # raw = response.css("div.description::text").get()

        # if raw is '':
        description = response.css("span.job-description").get()
        description = remove_tags(description)
        regex = re.compile(r"[\n\r\t]")
        output = regex.sub("", description)

        item["description"] = output

        return item

import scrapy
import datetime

job_list = []


class JobUrlSpider(scrapy.Spider):
    name = "urls"
    base_url = "http://resume.doska.kg"
    filename = "core/management/commands/parse_data/job_urls.csv"

    def start_requests(self):
        open(self.filename, "w").close()

        urls = ["http://resume.doska.kg/vacancy/&sortby=new",
                "http://resume.doska.kg/vacancy/&page=2&sortby=new"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        with open(self.filename, "a") as out:
            for job_title in response.css("div.list_full_title"):
                job_url = job_title.css("a.title_url").attrib["href"]
                full_url = self.base_url + ''.join(job_url.split('?')[:1])
                out.write(full_url+"\n")


class JobSpider(scrapy.Spider):
    name = "jobs"

    def start_requests(self):
        with open("core/management/commands/parse_data/job_urls.csv", "r") as f:
            for line in f:
                yield scrapy.Request(url=line.rstrip(), callback=self.parse)

    def parse(self, response, **kwargs):
        data = {
            "category": response.css("div.kroshki").css("a[href*=cat]::text").get(),
            "title": response.css("div.title::text").get(),
            'description': ''.join(response.xpath("//div[contains(@class, 'desc')]/text()")[2:].getall()),
            'city': response.xpath("//div[contains(@class, 'title')]/following-sibling::div[1]/text()").get(),
            'contacts': {"phone number": response.xpath("//div[contains(@class, 'desc')]/text()")[1].get().strip()},
            'created_on': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }
        job_list.append(data)


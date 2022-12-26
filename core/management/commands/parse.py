import json
from twisted.internet import defer, reactor
from scrapy.crawler import CrawlerRunner
from django.core.management.base import BaseCommand

from .spiders import JobUrlSpider, JobSpider, job_list


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        runner = CrawlerRunner()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(JobUrlSpider)
            yield runner.crawl(JobSpider)
            reactor.stop()

        crawl()
        reactor.run()

        filename = "core/management/commands/parse_data/jobs.json"

        with open(filename, 'w', encoding="utf-8") as json_file:
            json.dump(job_list, json_file, indent=4, ensure_ascii=False)

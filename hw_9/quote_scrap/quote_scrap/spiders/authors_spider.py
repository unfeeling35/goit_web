import scrapy


class AuthorsSpiderSpider(scrapy.Spider):
    name = "authors_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        links = response.xpath('//span[2]/a/@href')
        for link in links:
            yield scrapy.Request(url=self.start_urls[0] + link.get())

        author_path = response.xpath('/html//div[@class="author-details"]')
        for info in author_path:
            name = info.xpath('h3[@class="author-title"]/text()').get().strip()
            yield {
                "fullname": name,
                "born_date": info.xpath('p/span[@class="author-born-date"]/text()').get().strip(),
                "born_location": info.xpath('p/span[@class="author-born-location"]/text()').get().strip(),
                "description": info.xpath('div[@class="author-description"]/text()').get().strip()
            }
        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
import scrapy


class HardwarezoneSpider(scrapy.Spider):
    name = 'hardwarezone'

    start_urls = [
        'https://forums.hardwarezone.com.sg/forums/pc-gaming.382/',
    ]

    def parse(self, response):
        for topic_list in response.xpath('//div[@class="structItem-title"]'):
            yield response.follow(topic_list.xpath('a/@href').get(), \
                self.parse)
        
        topic = response.xpath('//h1[@class="p-title-value"]/text()')
        
        for post in response.xpath('//div[@class="message-inner"]'):
            new_content = ""
            new_content_list = []
            for content_list in post.xpath('*//div[@class="bbWrapper"]//text()').getall():
                new_content = content_list.strip()
                new_content_list.append(new_content)
            
            author_position = post.xpath('div/section/div[has-class("message-userDetails")]/h5//text()').get()
            if author_position == "*":
                    author_position = post.xpath('div/section/div[has-class("message-userDetails")]/div/strong/text()').get()

            yield {
                'topic': topic.get(),
                'post-position': post.xpath('*//ul[contains(@class, "message-attribution-opposite")]/li[2]/a/text()').get().strip(),
                'author': post.xpath('div/section/div[has-class("message-userDetails")]/h4/a//text()').get(),
                'author-position': author_position,
                'post-date-time': post.xpath('*//ul[@class="message-attribution-main listInline "]/li/a/time[@class="u-dt"]/@title').get(),
                'content': " ".join(new_content_list),
                'joined-date': post.xpath('*//div/dl/dd/text()').get(),
                'num-messages': post.xpath('*//div/dl[2]/dd/text()').get(),
                'reaction-score': post.xpath('*//div/dl[3]/dd/text()').get(),}

        next_page = response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
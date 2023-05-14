import scrapy
import re

def clean_html(text_html):
    import lxml.html.clean as clean
    safe_attrs = set(['src', 'alt', 'href', 'title', 'width', 'height'])
    kill_tags = ['object', 'iframe']
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=safe_attrs, kill_tags=kill_tags)
    cleaned_html = cleaner.clean_html(text_html)
    regex = r"<a .*?>"
    text_remove_html = re.sub(regex, " ", cleaned_html)
    cleanr = re.compile(r'<(?!p|h3).*?>')
    clean_text_with_p = cleanr.sub('', text_remove_html)
    cleanr = re.compile('<.*?>')
    clean_text_none_p = re.sub(cleanr, '\n', clean_text_with_p)
    return (remove_multi_space(clean_text_none_p.strip()))


def remove_multi_space(text):
    return ("\n".join([c for c in re.sub(r'(\r\n|\r|\n)', '\n', re.compile(r"[\t ]+").sub(" ", text.strip())).splitlines() if c != " "]))


class HoiDapVinmecSpider(scrapy.Spider):
    name = 'vinmec_hoi_dap'
    allowed_domains = ['vinmec.com']
    start_urls = ['https://vinmec.com/vi/tin-tuc/hoi-dap-bac-si/']

    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        list_url = response.xpath('//h2/a/@href').getall()
        for url in list_url:
            yield scrapy.Request(url="https://vinmec.com" + url, callback=self.parse_detail_medicine)
        for i in range(582):
            yield scrapy.Request(url="https://www.vinmec.com/vi/tin-tuc/hoi-dap-bac-si/?page=" + str(i+2), callback=self.parse)

    def parse_detail_medicine(self, response):
        sum_question = (response.xpath('(//h1/text())|(//title/text())').get()).replace("| Vinmec", "")
        text = response.xpath('//div[@class="rich-text"]').get()
        try:
            answer = (remove_multi_space(clean_html(text))).split("Chào bạn,")[1]
        except:
            try:
                answer = (remove_multi_space(clean_html(text))).split("Trả lời")[1]
            except:
                text = response.xpath('//div[@class="rich-text"][2]').get()
                answer = (remove_multi_space(clean_html(text))).split("Trả lời")[1]
        data = {
            "question": sum_question,
            "answer": answer.replace("\n", ""),
            "link": response.url
        }
        # print(data)
        yield (data)

import scrapy
import re

class CrawlBenhVaCoThe(scrapy.Spider):
    name = 'vinmec_benh'
    allowed_domains = ['vinmec.com']
    start_urls = ['https://vinmec.com/vi/benh/']
    domain = 'https://vinmec.com'

    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # yield scrapy.Request(url="https://vinmec.com/vi/benh/viem-hong-man-tinh-4460/", callback=self.parse_item)
        characters = ['a', 'b', 'c', 'd', 'đ', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                      'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        total_link = []
        for c in characters:
            # css = 'section#'+c+' ul.collapsible-target li a::attr(href)'
            css = 'section#' + c + ' ul.collapsible-target li'
            for ele in response.css(css):
                temp = {}
                link = ele.css('a::attr(href)').get()
                name = ele.css('a::text').get()
                temp['link'] = link
                temp['name'] = name
                total_link.append(temp)

        for item in total_link:
            new_url = self.domain + item['link']
            # print(new_url)
            request = scrapy.Request(url=new_url, callback=self.parse_item)
            request.meta['name'] = item['name']
            yield request
            # break

    def parse_item(self, response):
        item = dict()
        item['tong_quan'] = ''
        item['question_tong_quan'] = ''
        item['nguyen_nhan'] = ''
        item['question_nguyen_nhan'] = ''
        item['trieu_chung'] = ''
        item['question_trieu_chung'] = ''
        item['doi_tuong'] = ''
        item['question_doi_tuong'] = ''
        item['phong_ngua'] = ''
        item['question_phong_ngua'] = ''
        item['bien_phap_chan_doan'] = ''
        item['question_bien_phap_chan_doan'] = ''
        item['bien_phap_dieu_tri'] = ''
        item['question_bien_phap_dieu_tri'] = ''
        item['duong_lay_truyen'] = ''
        # item['raw_data'] = response.body
        item['ten_benh'] = response.meta['name']
        item['chu_de'] = response.css('div.tags a::text').getall()
        item['link'] = response.url
        item['title'] = response.css('h1::text').get().strip()
        item['anh_benh'] = []
        # with open("test.html", "wb") as f:
        #     f.write(response.body)
        list_anh_benh = response.css('div#hero-image-section ::attr(data-images)').get()
        import json
        for anh in json.loads(list_anh_benh):
            item['anh_benh'].append(anh["origin_url"])
        item['anh_benh'] = json.dumps(item['anh_benh'])
        # print(item['anh_benh'])
        # print(type(json.loads(list_anh_benh)))

        for ele in response.css('section.collapsible-container'):
            sub_question = ""
            text = ''
            tieu_de = ele.css('h2 span::text').get()
            list_text = ele.css('div.collapsible-target p::text,strong::text, a::text, li::text, h3::text').getall()
            for i in range(len(list_text)):
                if "?" in list_text[0]:
                    sub_question = list_text[0]
                text += list_text[i] + "\n"

            if tieu_de.lower().find('tổng quan') != -1:
                item['tong_quan'] = text
                item['question_tong_quan'] = sub_question
            if tieu_de.lower().find('nguyên nhân') != -1:
                item['nguyen_nhan'] = text
                item['question_nguyen_nhan'] = sub_question
            if tieu_de.lower().find('triệu chứng') != -1:
                item['trieu_chung'] = text
                item['question_trieu_chung'] = sub_question
            if tieu_de.lower().find('đối tượng') != -1:
                item['doi_tuong'] = text
                item['question_doi_tuong'] = sub_question
            if tieu_de.lower().find('phòng ngừa') != -1:
                item['phong_ngua'] = text
                item['question_phong_ngua'] = sub_question
            if tieu_de.lower().find('biện pháp chẩn đoán') != -1:
                if "xem thêm" in text.lower():
                    item['bien_phap_chan_doan'] = text.split("Xem thêm")[0]
                else:
                    item['bien_phap_chan_doan'] = text
                item['question_bien_phap_chan_doan'] = sub_question
            if tieu_de.lower().find('biện pháp điều trị') != -1:
                if "xem thêm" in text.lower():
                    item['bien_phap_dieu_tri'] = text.split("Xem thêm")[0]
                else:
                    item['bien_phap_dieu_tri'] = text
                item['question_bien_phap_dieu_tri'] = sub_question
            if tieu_de.lower().find('đường lây truyền bệnh') != -1:
                text_list = text.split("Xem thêm")
                item['duong_lay_truyen'] = text_list[0]

        # print(item['bien_phap_dieu_tri'])
        # yield item
        # print(item)
        yield (item)





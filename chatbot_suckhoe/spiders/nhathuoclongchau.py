from scrapy.spiders import CrawlSpider, Rule
import scrapy
# from .thuoc_biet_duoc import parse_text
import json
from lxml.html.soupparser import fromstring
import html2text
import re

def process(list_gia_tri):
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    no_tags = tag_re.sub('', list_gia_tri)
    thong_tin = (no_tags.strip()).replace("\r\n\r\n", " ")
    txt = re.sub(r'(\s*)([\,\.\(\)\:\?\-])(\s*)', r' \2 ', thong_tin)
    txt = re.sub(r'(\d+)(\s)([\,\.])', r'\1\3', txt)
    txt = re.sub(r'([\,\.])(\s)(\d+)', r'\1\3', txt)
    txt = re.sub('\s+', ' ', txt)
    return txt

class ThuocLongChauSpider(CrawlSpider):
    name = "longchau"

    def __init__(self, crawlMode='', **kwargs):
        super().__init__(**kwargs)
        self.page_num = 1

    def start_requests(self):
        urls = ['https://nhathuoclongchau.com/benh']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for index in range(16, 34):
            import requests
            url = "https://nhathuoclongchau.com/benh/loadmore?cate_id={}&limit=100&page=1".format(str(index))
            payload = {}
            headers = {
                'Cookie': 'PHPSESSID=845htbc2599p2soqfhcdebtr3q; XSRF-TOKEN=eyJpdiI6IkswWHJBekFuUmo0NDBscXZsRzlrYmc9PSIsInZhbHVlIjoiN0I5RDFUUGhwekVzS3N3RTFpL25ROWZSYW4zMlNEdFZrV3lNSDlzVGRGTWhPU29XTzlLTmpTRWJZMEN4STNjVTYxWkhCSTF5MXJISDNkdXBMbmhKRWM2QXBWWExIN1VSMFdxKzhEMUY0TzJvbWxjZ2lNS0Vva1lXRlQ1NDROZ2UiLCJtYWMiOiIzNmQ1MzM4OTVkMmU2ZDU5YjgzYjZmZWYxNzRiZTM1Y2VmMzdhYWRhNDI2ODQ4ODIwMzAzOTMzNzA2MzUxMmZmIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6InlrS01Rc2JFL0F3VmRXZWdJeE9OQ2c9PSIsInZhbHVlIjoiclhFVm1raWlaaXFMYmVUdjhGM042MzFXZjVmbHNIblBmMUJhcWd1ekVJMng5bXBSWXA1Ykw0NzR0dVNEczd1cEJmd0lidzFpMEhqN1h2M0tPQnYvSWhiS3diTElQOS84NGJ6MTFicklQR0QrYXMwUFZQdHNsMUpOMmdDb0orVVEiLCJtYWMiOiIwYTBmNjM3MDhkNmMwYTM2MDlmZDRlYTliNWI4ODIzMjdhNGNmNjU1OTVmY2Q1NjBlMDM3YjEzYTgwOWY1YWYzIiwidGFnIjoiIn0%3D'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            html = json.loads(response.text)["view"]
            tree = fromstring(html)
            list_link = tree.xpath("//li/a/@href")
            list_ten_benh = tree.xpath("//li/a/text()")
            for index in range(len(list_link)):
                yield scrapy.Request(url=list_link[index], callback=self.parse_detail, meta={"ten_benh": list_ten_benh[index]})
                # break
            # break

        # list_disease = response.xpath('')


    def parse_detail(self, response):
        import re
        print(response.url)
        text = response.xpath('//div[@class="cs-base-custom cs-benh-content"]').get()
        list_tag_h2 = re.findall(r"<h2\b[^<]*(?:(?!<\/h2>)<[^<]*)*<\/h2>", text)
        # print((len(list_tag_h2)))
        if (len(list_tag_h2)) == 6:
            data = dict()
            for i in range(len(list_tag_h2)):
                if i == 0:
                    list_gia_tri = (text.split(list_tag_h2[i + 1]))[0].replace(list_tag_h2[0], "")
                    data.update({
                        "tong_quan": process(list_gia_tri)
                    })
                    thong_tin = html2text.html2text(list_gia_tri)
                    print(thong_tin)
                elif i == 4:
                    list_gia_tri = (text.split(list_tag_h2[i + 1]))[0].split(list_tag_h2[i])[1]
                    list_tag_strong = re.findall(r"<strong>.*<\/strong>", list_gia_tri)
                    for tag_strong in list_tag_strong:
                        if "chẩn đoán" in tag_strong:
                            thong_tin = list_gia_tri.split(list_tag_strong[1])[0].split(list_tag_strong[0])[1]
                            data.update({
                                "bien_phap_chan_doan": process(thong_tin)
                            })
                        else:
                            thong_tin = list_gia_tri.split(list_tag_strong[1])[1]
                            data.update({
                                "bien_phap_dieu_tri": process(thong_tin)
                            })
                    # print(list_tag_strong)
                elif i == 5:
                    list_gia_tri = (text.split(list_tag_h2[i]))[1].replace(list_tag_h2[i], "")
                    # thong_tin = html2text.html2text(list_gia_tri)
                    data.update({
                        "phong_ngua": process(list_gia_tri)
                    })
                else:
                    if i == 1:
                        key = "trieu_chung"
                    elif i == 2:
                        key = "nguyen_nhan"
                    elif i == 3:
                        key = "doi_tuong_nguy_co"

                    list_gia_tri = (text.split(list_tag_h2[i + 1]))[0].split(list_tag_h2[i])[1]
                    data.update({
                        key: process(list_gia_tri)
                    })
            data["ten_benh"] = response.meta["ten_benh"].strip().lower()
            # yield data
            if "\r\n\t\n" in data["trieu_chung"]:
                a = (data["trieu_chung"].replace('\r\n\t\n', "bullet").rstrip("\n"))
                a = a.replace("\n", "bulletbullet")
                a = a.replace("bulletbullet", " ")
                # a = a.replace(":bullet", "\n\t* ")
                # a = a.replace("bullet", "\n")s
            else:
                a = data["trieu_chung"].rstrip("\n")
                a = a.replace("\n", " ")
                # a = a.replace("\n", "\n\t* ")
            a = a.replace("bullet", "")
            # txt = word_tokenize(a, format="text")
            print("---------------------")
            txt = re.sub( r'([\,\.\(\)\:\?\-])', r' \1', a)
            # txt = re.sub(r'(\s*)([\,\.\(\)\:\?\-])(\s*)', r' \2 ', a)
            # txt = re.sub(r'(\d+)(\s)([\,\.])', r'\1\3', txt)
            # txt = re.sub(r'([\,\.])(\s)(\d+)', r'\1\3', txt)
            txt = re.sub( r'(\d+)([a-zA-Z]+)', r'\1 \2', txt)
            txt = re.sub( r'([\,\.\(\)\:\?])([a-zA-Z])', r'\1 \2', txt)
            txt = re.sub('\s+', ' ', txt)
            print(txt)
            with open("./dataset/dataset_" + str("longchau") + ".txt", "a", encoding="utf-8") as f:
                if txt != "":
                    f.write(txt.strip() + "\n")
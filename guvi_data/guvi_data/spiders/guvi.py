import scrapy
import json

class scrap_data(scrapy.Spider):
    name="guvi_scrap"
    start_urls=["https://www.guvi.in/courses"]

    header= {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
  }

    def parse(self, response):
        base_url="https://www.guvi.in/model/v2/courseFetchByCategory.php"
        payload="myData=%7B%22requestType%22%3A%22allCourses%22%2C%22authtoken%22%3Anull%2C%22originUrl%22%3A%22www.guvi.in%22%7D"
        yield scrapy.Request(base_url,method='POST',body=payload,headers=self.header,callback=self.parse_data)
    def parse_data(self, response):
        data=json.loads(response.body)
        data=data['allCourses']['courses']
        for i in data:
            name =i["cname"]
            key  =i["ckey"]
            Course_Type=i["courseType"]
            Price=i["discountPrice"]
            Enrolled=i["enrolled"]
            Language=i["lang"]
            base_url="https://www.guvi.in/courses/"+key
            yield scrapy.Request(base_url,callback=self.parse2,cb_kwargs={
                "name":name,
                'key':key,
                'Course_Type':Course_Type,
                'Price':Price,
                "Enrolled":Enrolled,
                "Language":Language    
            })

    def parse2(self,response,name,key,Course_Type,Price,Enrolled,Language):
        base_url="https://www.guvi.in/model/v2/course_details.php"
        payload="myData=%7B%22requestType%22%3A%22details%22%2C%22key%22%3A%22data_science_with_r_malayalam%22%2C%22source%22%3Afalse%2C%22medium%22%3Afalse%2C%22campaign%22%3Afalse%2C%22authtoken%22%3Anull%2C%22originUrl%22%3A%22www.guvi.in%22%7D"
        yield scrapy.Request(base_url,method='POST',body=payload,headers=self.header,callback=self.parse_data2,cb_kwargs={
                "name":name,
                'key':key,
                'Course_Type':Course_Type,
                'Price':Price,
                "Enrolled":Enrolled,
                "Language":Language    
            })
    def parse_data2(self, response,name,key,Course_Type,Price,Enrolled,Language):
        data=json.loads(response.body)
        description=data["details"][0]["description"]
        yield{
            "name":name,
                'key':key,
                'Course_Type':Course_Type,
                'Price':Price,
                "Enrolled":Enrolled,
                "Language":Language,
                "Description":description
        }

        
    




        

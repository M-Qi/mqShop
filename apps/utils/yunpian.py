import requests
import json
from django.conf import settings

class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self,code,mobile):
        # 需要传递的参数
        parmas = {
            'apikey':self.api_key,
            'mobile':mobile,
            'text':"【马琦】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict

# if __name__ == '__main__':
#     # 例如：654153asd1536asds5adsa2dsa
#     yun_pian = YunPian("411dfdcef6eaea8f85569d737f19ffe8")
#     yun_pian.send_sms('2018','18295903413')



from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,ImageSendMessage
from bs4 import BeautifulSoup
import requests

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


def BigLottery():
    try:
        url = 'https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,'lxml')
        trs = soup.find('table',class_="table_org td_hm").find_all('tr')
        date = [td.text.strip() for td in trs[0].find_all('td')]
        data1=[td.text.strip() for td in trs[1].find_all('td')]
        data2=[td.text.strip() for td in trs[4].find_all('td')[1:]]
        data = ''
        for i in range(len(date)):
            data +=f'{date[i]}:{data1[i]}\n'
        data += ','.join(data2[:-1])+ ' 特別號:'+ data2[-1]
        print(data)
        return data
    except Exception as e:
        print(e)
        return  "取得大樂透號碼，請稍後再試..."
@csrf_exempt

def lottery(request):
    text = BigLottery().replace('\n','<br>')
    return HttpResponse(f'<h1>{BigLottery()}</h1>')

def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
                text = event.message.text
                message = None
                print(text)
                if text == '1':
                    message = '早安'
                elif text == '2':
                    message = '午安'
                elif text == '3':
                    message = '晚安'
                elif '早安' in text:
                    message = '早安你好!'
                elif '捷運' in text:
                    # 台北/台中/高雄
                        mrts={
                            '台北捷運':'https://tw.images.search.yahoo.com/search/images;_ylt=AwrthrFPX01kwVQkNKlr1gt.;_ylu=Y29sbwN0dzEEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?p=%E5%8F%B0%E5%8C%97%E6%8D%B7%E9%81%8B&fr2=piv-web&type=E211TW885G0&fr=mcafee#id=1&iurl=https%3A%2F%2Fcg2010studio.files.wordpress.com%2F2011%2F12%2Fmrt.png&action=click',
                            '台中捷運':'https://tw.images.search.yahoo.com/search/images;_ylt=Awrt4BGXX01kcHA1PUNt1gt.;_ylu=c2VjA3NlYXJjaARzbGsDYnV0dG9u;_ylc=X1MDMjExNDcwNTAwNQRfcgMyBGZyA21jYWZlZQRmcjIDcDpzLHY6aSxtOnNiLXRvcARncHJpZAN6blNFb1U4TFRIR3p4cTExNlBObF9BBG5fcnNsdAMwBG5fc3VnZwM0BG9yaWdpbgN0dy5pbWFnZXMuc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAzAEcXN0cmwDNwRxdWVyeQMlRTUlOEYlQjAlRTQlQjglQUQlRTYlOEQlQjclRTklODElOEIlRTglQjclQUYlRTclQjclOUElRTUlOUMlOTYEdF9zdG1wAzE2ODI3OTIzNDU-?p=%E5%8F%B0%E4%B8%AD%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B7%9A%E5%9C%96&fr=mcafee&fr2=p%3As%2Cv%3Ai%2Cm%3Asb-top&ei=UTF-8&x=wrt&type=E211TW885G0#id=1&iurl=https%3A%2F%2Fbuuz.tw%2Fwp-content%2Fuploads%2F20201110204645_26.png&action=click',
                            '高雄捷運':'https://tw.images.search.yahoo.com/search/images;_ylt=Awrt4BGaX01kqVQ2nm1t1gt.;_ylu=c2VjA3NlYXJjaARzbGsDYnV0dG9u;_ylc=X1MDMjExNDcwNTAwNQRfcgMyBGZyA21jYWZlZQRmcjIDcDpzLHY6aSxtOnNiLXRvcARncHJpZANiVUlWOU9zbVRhdVZOUEZrVVhnT09BBG5fcnNsdAMwBG5fc3VnZwMzBG9yaWdpbgN0dy5pbWFnZXMuc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAzAEcXN0cmwDNwRxdWVyeQMlRTklQUIlOTglRTklOUIlODQlRTYlOEQlQjclRTklODElOEIlRTglQjclQUYlRTclQjclOUElRTUlOUMlOTYEdF9zdG1wAzE2ODI3OTIzNzc-?p=%E9%AB%98%E9%9B%84%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B7%9A%E5%9C%96&fr=mcafee&fr2=p%3As%2Cv%3Ai%2Cm%3Asb-top&ei=UTF-8&x=wrt&type=E211TW885G0#id=1&iurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F3%2F33%2F%25E9%25AB%2598%25E9%259B%2584%25E6%258D%25B7%25E9%2581%258B%25E8%25B7%25AF%25E7%25B6%25B2%25E5%259C%2596_(C1-C14%25E7%25AB%2599%25E5%2590%258D%25E7%25A2%25BA%25E5%25AE%259A%25E7%2589%2588).png&action=click'
                        }
                        image_url = 'https://web.metro.taipei/pages/assets/images/routemap2023n.png'
                        for mrt in mrts:
                            print(mrt)
                            if mrt in text:
                                image_url  = mrts[mrt]
                                print(image_url)
                                break
                elif '樂透' in text:
                    message = BigLottery()
                else:
                    message = '抱歉，我不知道你說甚麼?'

                if message is None:
                    message_obj = ImageSendMessage(image_url, image_url)
                else:
                    message_obj = TextSendMessage(text=message)

                line_bot_api.reply_message(event.reply_token, message_obj)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def index(request):
    return HttpResponse("<h1>你好，我是AI機器人</h1>")

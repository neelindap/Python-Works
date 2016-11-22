import requests
import time
from lxml import html
from twilio.rest import TwilioRestClient
import smtplib

def getProductData(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    res = requests.get(url, headers=headers)
    htmlContent = html.fromstring(res.content)

    raw_name = htmlContent.xpath('//*[@id="productTitle"]/text()')
    raw_sellPrice = htmlContent.xpath('//*[@id="priceblock_ourprice"]/text()') 

    # If sale price is present
    if not raw_sellPrice:
        raw_sellPrice = htmlContent.xpath('//*[@id="priceblock_saleprice"]/text()')
    raw_discountedPrice = htmlContent.xpath('//*[@id="priceblock_dealprice"]/text()')

    name = ' '.join(''.join(raw_name).split())
    sellPrice = ' '.join(''.join(raw_sellPrice).split())
    discountedPrice = ' '.join(''.join(raw_discountedPrice).split())

    if raw_discountedPrice:
        data = name + ' was ' + sellPrice + ' is now ' + discountedPrice
    else:
        data = name + ' costs ' + sellPrice

    print(data)
    return data

def getURL():
    url = "http://www.amazon.com/dp/" # Can be update to country domain

    # Array list of products, asin number from Amazon's site for the product : https://www.amazon.com/dp/B00X4WHP5E
    # Example : productList = ["B01DFKC2SO","B00X4WHP5E"]
    productList = ""
        
    content = ''
    for i in productList:
        content += getProductData(url+i)+'\n\n'

    sendEmail(content)
    sendSMS(content)
    writeToFile(content)

def sendEmail(content):
    sender = <SENDER_EMAIL_ID>
    receiver = <RECEIVER_EMAIL_ID> # Can be an array
    subject = 'Amazon prices'
    body = 'Following are the prices :\n'+content

    email_text = """\
From: %s
To: %s
Subject: %s

%s
    """ % (sender, ",".join(receiver), subject, body)

    server = smtplib.SMTP_SSL() # Update SMTP details
    server.ehlo()
    server.login() # Sender email details. Google for implementation

    server.sendmail(sender, receiver, email_text)
    server.quit()

def sendSMS(content):

    ACCOUNT_SID = <ACCOUNT_SID>
    AUTH_TOKEN = <AUTH_TOKEN>

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(
        to=<YOUR_MOBILE_NUMBER>,
        from_=<YOUR_TWILIO_NUMBER>,
        body=content,
    )

def writeToFile(content):
    with open('AmazonPrices.txt', 'a') as file:
        file.write('At '+time.strftime("%c")+'\n')
        file.write(content)
        file.write('\n')
        file.close()

if __name__ == "__main__":
    getURL()
#Scraper to check for USD to INR exchange rate and sms (Using Twilio)

from urllib.request import urlopen
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient
import time

ACCOUNT_SID = <ACCOUNT_SID>
AUTH_TOKEN = <AUTH_TOKEN>


def exchangeRate():
    response = urlopen('https://www.google.com/finance/converter?a=1&from=USD&to=INR')
    html = BeautifulSoup(response, "lxml")
    rate= html.find('div', id='currency_converter_result').text

    smsContent = "Current exchange rate "+rate

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(
        to=<YOUR_NUMBER>,
        from_=<YOUR_TWILIO_NUMBER>,
        body=smsContent,
    )
    print(smsContent)

    writeToFile(smsContent)
    # Uncomment the below line to for this to keep running every 6 minutes
 #   time.sleep(3600)         
    return

def writeToFile(content):

    with open('ExchangeRate.txt', 'a') as file:
        file.write('On '+time.strftime("%c")+'\n')
        file.write(content)
        file.write('\n')
        file.close()

def main():
    # Uncomment the below line to for this to keep running
#    while(True):
        exchangeRate()

if __name__ == "__main__":
    main()

import requests
import smtplib
from bs4 import BeautifulSoup

k = 1
content = ''

def scrapeMe(pageNumber):
    for count in range(1,pageNumber):

        innerContent = ''
        j = 0
        global k
        global content

        count = str(count)
        url = "https://www.redwolf.in/t-shirts-for-men?filter=&tags=&sizes=&sort=p.date_added&order=DESC&page="+count
        page = requests.get(url)
        htmlContent = BeautifulSoup(page.text, "lxml")

        x_name = htmlContent.findAll('p', {'class':'category-product'})
        x_price = htmlContent.findAll('p', {'class':'price'})

        for i in x_name:
           name = ' '.join(''.join(i.text).split())
           price = ''.join(x_price[j].text.split())

           # If discounted
           if(len(price) > 9):
               discount = int(price[3:6]) - int(price[12:15])
               innerContent += '~' + str(k) + '.' + name + 'costs '+ price[9:]+ '. Discount of Rs.'+ str(discount)+'\n'

           # Normal price
           else:
               innerContent += str(k)+'.'+ name + ' costs ' + price+'\n'
           j+=1
           k+=1
        content += innerContent+'\n'
    sendEmail(content)



def sendEmail(content):
    sender = <SENDER_EMAIL>
    receiver = <RECEIVER_EMAIL> # Can be an array
    subject = 'Redwolf Tshirt prices'

    email_text = """\
From: %s
To: %s
Subject: %s

%s
    """ % (sender, ",".join(receiver), subject, content)

    server = smtplib.SMTP_SSL() # Configure SMTP details
    server.ehlo()
    server.login() # Sender's email details. Google for implementation

    server.sendmail(sender, receiver, email_text)
    server.quit()


if __name__ == '__main__':
    scrapeMe(5) # Page count. Can be increased if catalog increases.(Currently only 2 pages worth of products on the site)
import requests
import os
from bs4 import BeautifulSoup
import yagmail
import time
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

delay_time=15#seconds

url_to_monitor="https://xxx"

sender_email_username="xxxx"
sender_email_password="xxxx"
recipient_email="xxxxx"

def send_email_notification(alert_str):
    #sends an email notification
    yagmail.SMTP(sender_email_username,sender_email_password).send(recipient_email,alert_str,alert_str)


#process function that removes <script> & <meta> tags
def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    # make the html look good
    soup.prettify()
    # remove script tags
    for s in soup.select('script'):
        s.extract()
    # remove meta tags 
    for s in soup.select('meta'):
        s.extract()   
    # convert to a string, remove '\r', and return
    return str(soup).replace('\r', '')

def has_webpage_changed():
    #returns true if webpage has changed
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    ,'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}#prevent caching
    response=requests.get(url_to_monitor,headers=headers)
    print(url_to_monitor)
    print(response.status_code)

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"):
        open("previous_content.txt", 'w+',encoding="utf-8").close()
    
    filehandle = open("previous_content.txt", 'r',encoding="utf-8")
    previous_response_html = filehandle.read()
    filehandle.close()

    processed_response_html = process_html(response.text)

    if processed_response_html == previous_response_html:
        return False
    else:
        filehandle = open("previous_content.txt", 'w',encoding="utf-8")
        filehandle.write(processed_response_html)
        filehandle.close()
        return True

while True:
    try:
        if(has_webpage_changed()):
            send_email_notification(f"URGENT! {url_to_monitor} WAS CHANGED!")
            #print(dt_string+" ")
            #print("Webpage was changed")
            f = open("webpage.txt", 'a',encoding="utf-8")
            f.write(dt_string+" Webpage was changed\n")
            f.close()
            break
        else:
            #print(dt_string+" ")
            #print("Webpage was not changed")
            f = open("webpage.txt", 'a',encoding="utf-8")
            f.write(dt_string+" Webpage was not changed\n")
            f.close()
            break
    except:
        #print(dt_string+" ")
        #print("Error checking webpage")
        f = open("webpage.txt", 'a',encoding="utf-8")
        f.write(dt_string+" Error checking webpage\n")
        f.close()
      
   
    time.sleep(delay_time)

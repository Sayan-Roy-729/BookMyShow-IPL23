from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from email.message import EmailMessage
from selenium import webdriver
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()


def browser_function(url="https://www.google.com"):
    # define the driver path
    driver_path = Service("./drivers/chromedriver.exe")
    # set the different options for the browser
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # ignore the certificate and SSL errors
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # maximize the browser window
    chrome_options.add_argument("start-maximized")
    # define with the driver and open the browser
    chrome_driver = webdriver.Chrome(service=driver_path, options=chrome_options)
    # open the Google search page, for Google search engine
    chrome_driver.get(url)
    # then return the driver object
    return chrome_driver


def send_email(content: list, to: str) -> bool:
    # define a flag variable to check if the email is sent or not
    flag = True
    # get the email credentials from the .env file
    from_email = os.getenv("FROM_EMAIL")
    email_password = os.getenv("EMAIL_PASSWORD")
    try:
        # create the HTML content
        html_content = "<ul>"
        for match in content:
            html_content += f"<li>{match}</li>"
        html_content += "</ul>"

        # create a message object
        msg = EmailMessage()
        # setup the parameters of the message
        msg.set_content(html_content, subtype='html')
        msg['Subject'] = "IPL 2023 Matches"
        msg['From'] = from_email
        msg['To'] = to

        # create a SMTP session
        session = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        session.starttls()
        # Authentication
        session.login(from_email, email_password)
        # send the message via the session
        session.send_message(msg)
    except Exception as e:
        print(e)
        flag = False
    finally:
        # terminating the session
        session.quit()
        return flag

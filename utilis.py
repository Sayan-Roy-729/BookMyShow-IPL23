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
    # add aditional options (for hosting)
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless')
    # chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument('--no-sandbox')
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
        # create the HTML content for the email
        html_content = """
        <html>
            <head>
                <style type="text/css">
                    tr {
                        border-bottom: 1px solid #ddd;
                    }
                    tr:hover {background-color: #D6EEEE;}
                    table, th, td {
                        border: 1px solid black;
                        border-radius: 10px;
                    }
                    .center {
                        margin-left: auto;
                        margin-right: auto;
                        width: 70%;
                    }
                </style>
            </head>
                <body style="width:100%;">
                    <table class="center" style="width:100%">
                        <tr>
                            <th>Match Between</th>
                            <th>Month</th>
                            <th>Date</th>
                        </tr>
        """
        for match in content:
            html_content += f"""
                <tr style="text-align:center">
                    <td>{match[0]}</td>
                    <td>{match[1]}</td>
                    <td>{match[2]}</td>
                </tr>"""
        html_content += "</table></body></html>"

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

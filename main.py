from playwright.sync_api import sync_playwright
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import bs4

from utilis import browser_function, send_email


def select_component() -> str:

    # Search the BookMyShow webpage for the IPL matches
    # driver = browser_function(
    #     url="https://in.bookmyshow.com/kolkata/sports/indian-premier-league/ET00354770")

    # Select the city as Kolkata
    # driver.find_element(
    #     by=By.XPATH,
    #     value='//*[@id="modal-root"]/div/div/div/div[2]/ul/li[9]'
    # ).click()

    # wait 5 seconds for the page to load
    # time.sleep(5)

    # Select all the matches
    # whole_section = driver.find_element(
    #     by=By.CLASS_NAME,
    #     value="df-h.df-im.df-in"
    # )

    url = 'https://in.bookmyshow.com/kolkata/sports/indian-premier-league/ET00354770'
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/69.0.3497.100 Safari/537.36"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=ua)
        page.goto(url)
        page.wait_for_timeout(1000)
        
        html = page.content()

    soup = BeautifulSoup(html, 'html.parser')
    whole_html = soup.find('div', class_='df-h df-im df-in')

    # return the HTML content of our required section
    # return driver.execute_script("return arguments[0].innerHTML;", whole_section)
    return whole_html


def find_match_details(soup_obj: bs4.element.Tag) -> list:
    # find the match name (match between two teams)
    match_name = soup_obj.find(
        'div', class_='df-b df-dg df-ed df-ja df-jb').text
    # find the month in which the match will be played
    month_name = soup_obj.find('div', class_='df-ch df-ed df-iy').text
    # find the date of the match
    month_date = soup_obj.find("div", class_='df-ch df-ix').text
    return match_name, month_name, month_date


def filter_matches(matches: list, month: str, date: str) -> list:
    # if match found, then store the match name, month and date in a list
    match_found = []
    all_matches = []
    for _, match in enumerate(matches):
        try:
            # get the match name, month and date
            match_name, month_name, month_date = find_match_details(
                soup_obj=match)
            # store the match name, month and date in a list
            all_matches.append([match_name, month_name, month_date])
            # if we found our match, then store it in the match_found list
            if month_name == month and month_date == date:
                match_found.append([match_name, month_name, month_date])
        # if there is an error, print the error and continue
        except Exception as e:
            print(e)
            continue
    else:
        return match_found, all_matches


# get the list of all the required matches
def get_matches(month_name: str, month_date: str) -> list:
    # create a soup object
    # soup = BeautifulSoup(select_component(), 'html.parser')
    soup = select_component()

    # Get the list of all the matches
    matches = soup.find_all(
        'div', class_='df-b df-eb df-gq df-io df-ip df-iq df-m')

    # get the matches for the month of our required date
    return filter_matches(matches=matches, month=month_name, date=month_date)


def main(month_name: str, month_date: str, to: str) -> bool:
    # get the matches for the month of April and date 23
    filtered_matches, all_matches  = get_matches(month_name=month_name, month_date=month_date)
    # send the email
    if len(filtered_matches) == 0:
        return send_email(content=all_matches, to=to)
    return send_email(content=filtered_matches, to=to)


if __name__ == "__main__":
    # get the matches for the month of April and date 6
    counter = 0
    while True:
        response = main(month_name="Apr", month_date="6", to="rsayan553@gmail.com")
        print(response)
        counter += 1
        print(f"COUNTER: {counter}")
        time.sleep(900) # 15 minutes delay

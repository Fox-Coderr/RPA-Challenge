import time
import requests
import os.path
import re
from datetime import date
from dateutil.relativedelta import relativedelta
from SeleniumLibrary.errors import ElementNotFound
from pathlib import Path
from openpyxl import Workbook
from variables import *


def open_the_website(url):
    browser_lib.open_available_browser(url)


def handle_unknown_error(filename):
    browser_lib.screenshot(filename=filename)


def click_button(term):
    browser_lib.click_button_when_visible(term)


def get_img(url, title):
    Path(os.path.dirname(__file__), "output", "downloads").mkdir(
        parents=True, exist_ok=True)
    filename = title+" image.jpg"
    filepath = os.path.join(os.path.dirname(__file__),
                            "output", "downloads", filename)
    response = requests.get(url, timeout=10)
    with open(filepath, "wb") as file:
        file.write(response.content)
    return filename


def define_date(number):
    if number > 0:
        number -= 1
    elif number < 0:
        raise Exception("Number can't be lower than 0")

    today = date.today()
    start_date = today - relativedelta(months=number)
    return start_date.replace(day=2).strftime("%m/%d/%Y")


def select_checkbox(term):
    try:
        browser_lib.checkbox_should_be_selected(term)
    except:
        browser_lib.select_checkbox(term)


def click_checkbox(terms):
    for term in terms:
        select_checkbox(term)


def search_for(term):
    input_field = "name:query"
    browser_lib.input_text_when_element_is_visible(input_field, term)
    browser_lib.press_keys(input_field, "ENTER")


def input_date(term1, start_date):
    browser_lib.input_text_when_element_is_visible(term1, start_date)


def select_date_range(num_months):
    limit_date = define_date(num_months)
    click_button("class:css-p5555t")
    click_button(
        "xpath:/html/body/div/div[2]/main/div/div[1]" +
        "/div[2]/div/div/div[1]/div/div/div/ul/li[6]/button")
    input_date("id:startDate", limit_date)
    input_date("id:endDate", date.today().strftime("%m/%d/%Y"))
    browser_lib.click_element_when_visible(
        "xpath:/html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]" +
        "/div/div/div/div[2]/div/div/div/div/div[2]/div/div[3]/div[6]/div[1]")


def main():
    try:
        wi.get_input_work_item()
        search_phrase = wi.get_work_item_variable("SEARCH_PHRASE")
        if not isinstance(search_phrase, str):
            raise Exception("SEARCH_PHRASE must be a string")
        section_checkbox_list = wi.get_work_item_variable(
            "SECTION_CHECKBOX_LIST")
        if not isinstance(section_checkbox_list, list):
            raise Exception("section_checkbox_list must be a list")
        stop_on_section_error = wi.get_work_item_variable(
            "STOP_ON_SECTION_ERROR")
        if not isinstance(stop_on_section_error, bool):
            raise Exception("stop_on_section_error must be a bool")
        type_checkbox_list = wi.get_work_item_variable("TYPE_CHECKBOX_LIST")
        if not isinstance(type_checkbox_list, list):
            raise Exception("type_checkbox_list must be a list")
        stop_on_type_error = wi.get_work_item_variable("STOP_ON_TYPE_ERROR")
        if not isinstance(stop_on_type_error, bool):
            raise Exception("stop_on_type_error must be a bool")
        num_months = wi.get_work_item_variable("NUM_MONTHS")
        try:
            num_months = int(num_months)
        except ValueError:
            raise Exception("num_months must be a interger")
    except:
        raise Exception(
            "Make sure that all variables are configured correctly")
    try:
        open_the_website("www.nytimes.com")
        browser_lib.click_button("data:testid:GDPR-reject")
        search_for(search_phrase)

        try:
            # select section
            click_button(
                "xpath:/html/body/div/div[2]/main/div/div[1]/div[2]" +
                "/div/div/div[2]/div/div/button")
            click_checkbox(section_checkbox_list)
        except ElementNotFound:
            if stop_on_section_error:
                raise Exception("Wrong Section locator")
        except:
            if stop_on_section_error:
                handle_unknown_error("section_error")
                raise Exception("Error in Section selection")

        try:
            # select type
            click_button(
                "xpath:/html/body/div/div[2]/main/div/div[1]/div[2]" +
                "/div/div/div[3]/div/div/button")
            click_checkbox(type_checkbox_list)
        except ElementNotFound:
            if stop_on_section_error:
                raise Exception("Wrong Type locator")
        except:
            if stop_on_type_error:
                handle_unknown_error("type_error")
                raise Exception("Error in Type selection")

        # select sort
        browser_lib.select_from_list_by_value("class:css-v7it2b", "newest")

        select_date_range(num_months)

        run = True
        i = 1
        wb = Workbook()
        ws = wb.active
        ws.append(["Date", "Title", "Description",
                  "Image name", "Count", "Money"])
        path_xlsx = os.path.join(os.path.dirname(
            __file__), "output", "nytimesnews.xlsx")
        retry = False

        while run:
            if not (not i == 5 and not (i-5) % 11 == 0):
                i += 1
                continue
            if i == 12 or (i-2) % 10 == 0:
                try:
                    browser_lib.wait_until_page_contains_element(
                        "data:testid:search-show-more-button", 20)
                except AssertionError:
                    run = False
                    continue
                browser_lib.scroll_element_into_view(
                    "data:testid:search-show-more-button")
                browser_lib.click_button_when_visible(
                    "data:testid:search-show-more-button")
            try:
                browser_lib.wait_until_page_contains_element(
                    "xpath:/html/body/div/div[2]/main/div/div[2]/div[2]" +
                    "/ol/li[{}]/div/span".format(i), 20)
                news_date = browser_lib.get_text(
                    "xpath:/html/body/div/div[2]/main/div/div[2]/div[2]" +
                    "/ol/li[{}]/div/span".format(i))
                title = browser_lib.get_text(
                    "xpath:/html/body/div/div[2]/main/div/div[2]/div[2]" +
                    "/ol/li[{}]/div/div/div/a/h4".format(i))
                description = browser_lib.get_text(
                    "xpath:/html/body/div/div[2]/main/div/div[2]/div[2]" +
                    "/ol/li[{}]/div/div/div/a/p[1]".format(i))
                try:
                    img = get_img(browser_lib.get_element_attribute(
                        "xpath:/html/body/div/div[2]/main/div/div[2]/div[2]" +
                        "/ol/li[{}]/div/div/figure/div/img".format(i),
                        'src'), title)
                except:
                    img = None
                count = title.count(search_phrase) + \
                    description.count(search_phrase)
                money = True if re.search(regex, title) or re.search(
                    regex, description) else False

                ws.append(
                    [news_date, title, description, img, count, money])
                i += 1

                wb.save(path_xlsx)
                retry = False
            except:
                if retry:
                    run = False
                retry = True

    finally:
        browser_lib.close_all_browsers()


if __name__ == "__main__":
    main()

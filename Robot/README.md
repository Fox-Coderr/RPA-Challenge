This project is my answer to [RPA Challenge - Fresh news](https://thoughtfulautomation.notion.site/RPA-Challenge-Fresh-news-fa3f504bb7824e1aa9c083906ca1bba7).

After setting the config variables the project will search nytimes.com for the specified phrase/word and create an nytimesnews.xlsx with all the news with the corresponding configurations.

# Instalation/Requirements

Install the Robocorp code extension for vscode and it will autodetect the robot and allow you to run it.

# Variables
* **SEARCH_PHRASE** defines the word/phrase to be searched

* **SECTION_CHECKBOX_LIST** is the list of [locators](https://rpaframework.org/libdoc/RPA_Browser_Selenium.html#Explicit%20locator%20strategy) to select sections

* **STOP_ON_SECTION_ERROR** defines if the project should stop when an error in the section part happens or not.

* **TYPE_CHECKBOX_LIST** is the list of [locators](https://rpaframework.org/libdoc/RPA_Browser_Selenium.html#Explicit%20locator%20strategy) to select types

* **STOP_ON_TYPE_ERROR** defines if the project should stop when an error in the type part happens or not.

* **NUM_MONTHS** number of months which you need to receive news(0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on)

# Output folder

The output Folder contains outputed log, downloaded files and the xmlx created during execution.




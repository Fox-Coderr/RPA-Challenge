from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems

browser_lib = Selenium()
wi = WorkItems()
regex = "(\$[\d,]+(\.\d{1,2})?)|(\d+ dollars)|(\d+ USD)"
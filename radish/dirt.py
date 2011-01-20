from lettuce import before, after, world
from lettuce.django import django_url
import os
from selenium import get_driver
from selenium.remote.webelement import WebElement
from selenium.remote.webdriver import WebDriver

from radish.settings import *

@before.harvest
def prepare_browser_driver(variables):
	world.browser = get_driver(BROWSER)
	world.root_url = django_url()
	world.instances = {}

	# Set up a temporary directory for testing
	if not os.path.exists('tmp'): # to store local images and screenshots
		os.mkdir('tmp')

@after.harvest
def shutdown_browser_driver(results):
	# NOTE: A bug in selenium2.05a causes an output error at this point:
	# !!! error running onStopped callback: TypeError: callback is not a function
	# Hopefully this bug will disappear with a new version of selenium
	world.browser.quit()
	# ALTERNATIVE:
	# world.browser.stop()
	# TODO: empty and remove the "tmp" dir? Maybe not as it contains test
	# result information

@after.each_scenario
def screenshot_on_error(scenario):
	if scenario.failed:
		world.browser.save_screenshot("tmp/last_failed_scenario.png")

##### Useful functions added to Selenium ones

def find_element_by_tag_name_and_text(self, name, text):
    """Finds an element by its name and the included text."""
    return self.find_element_by_xpath('%s[text() = "%s"]' % (name, text))
WebElement.find_element_by_tag_name_and_text = find_element_by_tag_name_and_text
WebDriver.find_element_by_tag_name_and_text = find_element_by_tag_name_and_text

def find_elements_by_tag_name_and_text(self, name, text):
    """Finds elements by their name and the included text."""
    return self.find_elements_by_xpath('%s[text() = "%s"]' % (name, text))
WebElement.find_elements_by_tag_name_and_text = find_elements_by_tag_name_and_text
WebDriver.find_elements_by_tag_name_and_text = find_elements_by_tag_name_and_text


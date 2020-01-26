import bcolors
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .functions import suffix_number, month_string_to_number, get_date_from_hour_mark
from .comment import Comment
import os
import time
import re
from datetime import date



class Scraper(object):
    # Public variables used by the class.
    comments = []
    channel_name = None
    channel_subscribers = None
    date = None
    title = None
    likes = None
    dislikes = None
    views = None
    Date = None
    comments_count = None
    video_id = None
    video_url = None
    description = None
    speak = True
    category = None
    comments_to_scrape = None


    def __init__(self, id=None, driver=None, scrape=True, speak=True, close_on_complete=True, comments_to_scrape = None):
        #
        # [IMPORTANT] If an array is not defined in the constructor,
        # it will be shared by every process
        #
        self.comments = []
        self.comments_to_scrape = comments_to_scrape
        self.speak = speak

        if id == None:
            print(bcolors.ERR+"[ERROR] No video id given."+bcolors.END)
            return -1

        self.video_id = id
        self.video_url = "https://www.youtube.com/watch?v="+str(self.video_id)

        if self.speak:
            print("[INFO] Scraping webpage:", self.video_url)
        # If no information is given for the driver, I will try to find it.
        if driver is None:
            print("[INFO] NO driver specified - trying to find one")
            try:
                # Check if the driver is in the Path
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(os.path.dirname(__file__), 'drivers/chromedriver')
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        # Get to the webpage
        if self.speak:
            print("[INFO] Webpage loading")
        driver.get(self.video_url)
        if self.speak:
            print("[INFO] Webpage loaded")

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete=close_on_complete)
    #
    #
    #
    def get_category(self):
        driver = self.driver
        try:
        # There is not a specification for the Category tab: it shares construct with other things.
        # I have to look through all of them to find the one called category.
            category_path = None
            for title in driver.find_elements_by_id("title"):
                if title.text.strip() == "Category":
                    # I know, SPAGHETTI-CODE time. I just didn't bother, sorry.
                    category_path = title
                    break
            return category_path.find_element_by_xpath("./../div/yt-formatted-string/a").text.strip()
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find category information."+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_title(self):
        driver = self.driver
        try:
            return driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find title information"+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_views(self):
        driver = self.driver
        try:
            views_text = driver.find_element_by_class_name("view-count").text
            return int(re.sub(r'\D', "", views_text))
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find views information"+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_channel_name(self):
        driver = self.driver
        try:
            channel_name_path = driver.find_element_by_id("channel-name")
            return channel_name_path.find_element_by_xpath('./div/div/yt-formatted-string/a').text.strip()
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find channel name information"+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_channel_subscribers(self):
        driver = self.driver
        try:
            subscribers_string = driver.find_element_by_id("owner-sub-count").text.strip()
            try:
                numbers = float(re.sub(r"[A-Z].*$","",subscribers_string))
            except:
                if self.speak:
                    print(bcolors.WARN+"[WARNING] Problem converting subscriber count. Maybe the number has a coma."+bcolors.END)
                try:
                    auxiliary_string = subscribers_string.replace(',','.')
                    numbers = float(re.sub(r"[A-Z].*$","",auxiliary_string))
                except:
                    try:
                        if self.speak:
                            print(bcolors.WARN+"[WARNING] Problem converting subscriber count. Maybe the number is whole"+bcolors.END)
                        numbers = int(re.sub(r"\D", "", subscribers_string))
                    except:
                        #
                        # [NOTE] Most of the times, when this is outputted, it's
                        # due to abscence of subscribe number desplayed
                        #
                        print(bcolors.ERR+"[ERROR] Could not convert subscribe count from string to number"+bcolors.END)
                        return "Unknown"

            specification_letter = re.sub(r"[^A-Z]","",subscribers_string)
            # Youtube stores views using abbreviations
            return suffix_number(numbers, specification_letter)

        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find subscriber count information"+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_likes_dislikes(self):
        driver = self.driver
        likes_aux = None
        dislikes_aux = None
        try:
            menu_container_path = driver.find_element_by_id("menu-container")
            try:
                likes_string = menu_container_path.find_element_by_xpath("./div/ytd-menu-renderer/div/ytd-toggle-button-renderer/a/yt-formatted-string").get_attribute("aria-label").strip()
                likes_aux = int(re.sub(r'\D', "", likes_string))
            except:
                if self.speak:
                    print(bcolors.WARN+"[WARNING] Could not find like count information"+bcolors.END)
                likes_aux = "Unknown"
            try:
                dislikes_string = menu_container_path.find_element_by_xpath("./div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string").get_attribute("aria-label").strip()
                dislikes_aux = int(re.sub(r'\D', "", dislikes_string))
            except:
                if self.speak:
                    print(bcolors.WARN+"[WARNING] Could not find dislike count information"+bcolors.END)
                dislikes_aux = "Unknown"
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find like and dislike count information."+bcolors.END)
            likes_aux = "Unknown"
            dislikes_aux = "Unknown"
        return likes_aux, dislikes_aux
    #
    #
    #
    def get_description(self):
        driver = self.driver
        try:
            return driver.find_element_by_xpath('//*[@id="description"]/yt-formatted-string').text.strip()
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find description information."+bcolors.END)
            return "Unknown"

    #
    #
    #
    def get_comments_count(self):
        driver = self.driver
        try:
            comments_text = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string').text.strip()

            return int(re.sub(r"\D", "", comments_text))
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find comments count information."+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_date(self):
        driver = self.driver
        #
        #   [EXPLANATION]
        #   Dates can be in two format:
        #   1. {Jan 20, 2020}
        #   2. {Premiered 14 hours ago}
        #
        try:
            date_string = driver.find_element_by_xpath('//*[@id="date"]/yt-formatted-string').text.strip()
            try:
        # Test form 1
        # [NOTE] I could use regular expressions, but the format is always the same.
        #
                year = int(date_string[-4:])
                month = int(month_string_to_number(date_string[:3]))
                day = int(re.sub(r"\D", "", date_string).replace(date_string[-4:], ""))
                return date(year, month, day)
            except:
                try:
                    # Test form 2
                    #
                    #
                    return get_date_from_hour_mark(date_string[10:12])
                except:
                    if self.speak:
                        print(bcolors.WARN+"[WARNING] Could not find date information."+bcolors.END)
                    return "Unknown"
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find date information."+bcolors.END)
            return "Unknown"
        return 0
    #
    #
    #
    def scrape(self, close_on_complete=True):
        driver = self.driver

        if self.speak:
            print("[INFO] Maximizing window")
        driver.maximize_window()

        sleep_time = 2
        if self.speak:
            print("[INFO] Sleeping for", sleep_time,"seconds")
        time.sleep(sleep_time)

        # Get title
        self.title = self.get_title()

        # Get views
        self.views = self.get_views()

        # Get channel name
        self.channel_name = self.get_channel_name()

        # Get channel subscribers
        self.channel_subscribers = self.get_channel_subscribers()

        # Get likes and dislikes
        self.likes, self.dislikes = self.get_likes_dislikes()

        # Get date
        self.date = self.get_date()

        # I have to press the "Show more" button.
        try:
            driver.find_element_by_id("more").click()
            if self.speak:
                print("[INFO] 'Show more' button pressed.")
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find 'Show more' button"+bcolors.END)

        # Get description
        self.description = self.get_description()

        # Get category
        self.category = self.get_category()

        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Sleep, to allow for page rendering
        sleep_time_2 = 2
        if self.speak:
            print("[INFO] Sleeping for", sleep_time_2, "seconds")
        time.sleep(sleep_time_2)

        # Get comments count
        self.comments_count = self.get_comments_count()

        if self.speak:
            print("[INFO] Scraping comments")
        count = 0
        self.comments = []
        for comment_path in driver.find_elements_by_id("comment"):
            self.comments.append(Comment(path=comment_path, speak=self.speak).as_dict())
            if(self.comments_to_scrape != None):
                count = count + 1
                if(count > self.comments_to_scrape):
                    break

        # END
        if self.speak:
            print("[INFO] Scraping webpage completed")
        if close_on_complete:
            if self.speak:
                print("[INFO] Closing browser")
            driver.close()
    #
    #
    #
# Function to print out object representation
    def __repr__(self):
        result_dic = {
        "id": self.video_id,
        "url": self.video_url,
        "title": self.title,
        "views": self.views,
        "likes": self.likes,
        "dislikes": self.dislikes,
        "channel_name": self.channel_name,
        "channel_subscribers": self.channel_subscribers,
        "category": self.category,
        "description": self.description,
        "comments count": self.comments_count,
        "comments": self.comments
        }
        return str(result_dic)

    #
    #
    #
    def as_dict(self):
        return {
        "id": self.video_id,
        "url": self.video_url,
        "title": self.title,
        "views": self.views,
        "likes": self.likes,
        "dislikes": self.dislikes,
        "channel_name": self.channel_name,
        "channel_subscribers": self.channel_subscribers,
        "category": self.category,
        "description": self.description,
        "date": self.date.__str__(),
        "comments count": self.comments_count,
        "comments": self.comments
        }

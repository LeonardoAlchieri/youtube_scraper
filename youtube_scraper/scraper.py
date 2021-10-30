from bcolors import ERR, END, WARN
from selenium import webdriver
from .functions import suffix_number, month_string_to_number, get_date_from_hour_mark
from .comment import Comment
from os import getenv, path 
from time import sleep
from re import sub
from datetime import date as formatdate
from typing import List, Union, Literal



class Scraper(object):
    # Public variables used by the class.
    comments: List[str] = []
    channel_name: str = None
    channel_subscribers: Union[float, Literal['Unknown'], None]= None
    date: formatdate = None
    title: str = None
    likes: Union[int, Literal['Unknown'], None] = None
    dislikes: Union[int, Literal['Unknown'], None] = None
    views: Union[int, Literal['Unknown'], None] = None
    Date = None
    comments_count: Union[int, Literal['Unknown'], None] = None
    video_id: Union[str, Literal['Unknown'], None] = None
    video_url: Union[str, Literal['Unknown'], None] = None
    description: Union[str, Literal['Unknown'], None] = None
    speak: bool = True
    category: Union[str, Literal['Unknown'], None] = None
    comments_to_scrape: Union[int, Literal['Unknown'], None] = None


    def __init__(self, id=None, driver=None, scrape=True, speak=True, close_on_complete=True, comments_to_scrape = None):
        #
        # [IMPORTANT] If an array is not defined in the constructor,
        # it will be shared by every process
        #
        self.comments = []
        self.comments_to_scrape = comments_to_scrape
        self.speak = speak

        if id == None:
            print(ERR+"[ERROR] No video id given."+END)
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
                if getenv("CHROMEDRIVER") == None:
                    driver_path = path.join(path.dirname(__file__), 'drivers/chromedriver')
                else:
                    driver_path = getenv("CHROMEDRIVER")

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
                print(WARN+"[WARNING] Could not find category information."+END)
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
                print(WARN+"[WARNING] Could not find title information"+END)
            return "Unknown"
    #
    #
    #
    def get_views(self):
        driver = self.driver
        try:
            views_text = driver.find_element_by_class_name("view-count").text
            return int(sub(r'\D', "", views_text))
        except:
            if self.speak:
                print(WARN+"[WARNING] Could not find views information"+END)
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
                print(WARN+"[WARNING] Could not find channel name information"+END)
            return "Unknown"
    #
    #
    #
    def get_channel_subscribers(self):
        driver = self.driver
        try:
            subscribers_string = driver.find_element_by_id("owner-sub-count").text.strip()
            try:
                numbers = float(sub(r"[A-Z].*$","",subscribers_string))
            except:
                if self.speak:
                    print(WARN+"[WARNING] Problem converting subscriber count. Maybe the number has a coma."+END)
                try:
                    auxiliary_string = subscribers_string.replace(',','.')
                    numbers = float(sub(r"[A-Z].*$","",auxiliary_string))
                except:
                    try:
                        if self.speak:
                            print(WARN+"[WARNING] Problem converting subscriber count. Maybe the number is whole"+END)
                        numbers = int(sub(r"\D", "", subscribers_string))
                    except:
                        #
                        # [NOTE] Most of the times, when this is outputted, it's
                        # due to abscence of subscribe number desplayed
                        #
                        print(ERR+"[ERROR] Could not convert subscribe count from string to number"+END)
                        return "Unknown"

            specification_letter = sub(r"[^A-Z]","",subscribers_string)
            # Youtube stores views using abbreviations
            return suffix_number(numbers, specification_letter)

        except:
            if self.speak:
                print(WARN+"[WARNING] Could not find subscriber count information"+END)
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
                likes_aux = int(sub(r'\D', "", likes_string))
            except:
                if self.speak:
                    print(WARN+"[WARNING] Could not find like count information"+END)
                likes_aux = "Unknown"
            try:
                dislikes_string = menu_container_path.find_element_by_xpath("./div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string").get_attribute("aria-label").strip()
                dislikes_aux = int(sub(r'\D', "", dislikes_string))
            except:
                if self.speak:
                    print(WARN+"[WARNING] Could not find dislike count information"+END)
                dislikes_aux = "Unknown"
        except:
            if self.speak:
                print(WARN+"[WARNING] Could not find like and dislike count information."+END)
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
                print(WARN+"[WARNING] Could not find description information."+END)
            return "Unknown"

    #
    #
    #
    def get_comments_count(self):
        driver = self.driver
        try:
            comments_text = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string').text.strip()

            return int(sub(r"\D", "", comments_text))
        except:
            if self.speak:
                print(WARN+"[WARNING] Could not find comments count information."+END)
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
                day = int(sub(r"\D", "", date_string).replace(date_string[-4:], ""))
                return formatdate(year, month, day)
            except:
                try:
                    # Test form 2
                    #
                    #
                    return get_date_from_hour_mark(date_string[10:12])
                except:
                    if self.speak:
                        print(WARN+"[WARNING] Could not find date information."+END)
                    return "Unknown"
        except:
            if self.speak:
                print(WARN+"[WARNING] Could not find date information."+END)
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
        sleep(sleep_time)

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
                print(WARN+"[WARNING] Could not find 'Show more' button"+END)

        # Get description
        self.description = self.get_description()

        # Get category
        self.category = self.get_category()

        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Sleep, to allow for page rendering
        sleep_time_2 = 2
        if self.speak:
            print("[INFO] Sleeping for", sleep_time_2, "seconds")
        sleep(sleep_time_2)

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

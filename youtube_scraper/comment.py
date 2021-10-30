import bcolors
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .functions import suffix_number, month_string_to_number, get_date_from_hour_mark
import os
import time
import re


class Comment(object):
    likes = None
    replies_count = None
    user = None
    text = None
    path = None
    speak = True
    
    def __init__(self, path=None, speak=True):
        self.speak = speak
        self.scrape(path)
        
    #
    #
    #
    def get_user(self):
        path = self.path
        try:
            return path.find_element_by_xpath('.//*[@id="author-text"]').text.strip()
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find comment user"+bcolors.END)
            return "Unknown"

    #
    #
    #
    def get_text(self):
        path = self.path
        try:
            return path.find_element_by_xpath('.//*[@id="content-text"]').text.strip()
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find comment text"+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_likes(self):
        path = self.path
        try:
            likes_string = path.find_element_by_xpath('.//*[@id="vote-count-middle"]').text.strip()
            try:
                return int(likes_string)
            except:
                if self.speak:
                    print(bcolors.WARN+"[WARNING] Could not convert comment likes to number - trying if bigger than 1000"+bcolors.END)
                try:
                    numbers = float(re.sub(r"[A-Z].*$","",likes_string))
                    specification_letter = re.sub(r"[^A-Z]","",likes_string)
                    
                    # Youtube stores views using abbreviations
                    return suffix_number(numbers, specification_letter)
                except:
                    if self.speak:
                        print(bcolors.WARN+"[WARNING] Could not find comment likes"+bcolors.END)
                    return "Unknown"
                    
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find comment likes"+bcolors.END)
            return "Unknown"
    #
    #
    #
    def get_replies_count(self):
        path = self.path
        try:
            return path.find_element_by_xpath('./..//*[@id="replies"]//*[@id="text"]').text.strip()
            try:
                 int(re.sub(r"\D","",text_string))
            except:
                if self.speak:
                    print(bcolors.WARN+"[WARNING] Could not convert replies to number - trying if single reply"+bcolors.END)
                
                if(text_string == "View reply"):
                    return 1
                else:
                    if self.speak:
                        print(bcolors.ERR+"[ERROR] Found reply number but could not convert"+bcolors.END)
        except:
            if self.speak:
                print(bcolors.WARN+"[WARNING] Could not find comment replies"+bcolors.END)
            return "Unknown"
    #
    #
    #
    def scrape(self, path):
        self.path = path
        # Get user
        self.user = self.get_user()
        
        # Get text
        self.text = self.get_text()
            
        # Get likes
        self.likes = self.get_likes()
        
        # Get replies
        self.replies_count = self.get_replies_count()
    #
    #
    #
    def as_dict(self):
        return {
        "likes": self.likes,
        "replies count": self.replies_count,
        "user": self.user,
        "text": self.text
    }


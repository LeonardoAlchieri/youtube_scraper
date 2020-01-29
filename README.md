# Youtube Scraper

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.org/project/YoutubeScraper/)
[![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.org/project/YoutubeScraper/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pybadges.svg)](https://pypi.org/project/YoutubeScraper/)

This library provides with a class, `Scraper`, that will take most of the information present on a video page.

The project is still in alpha and will be fully updated when I will have time. I will add a documentation later.

## INSTALL

In order to install, just use `pip install YoutubeScraper`. 😄 All pre-requisites will be installed.

**WARNING** I guarantee it works only with `python 3` or above. In the future, I will try to port it to all versions, if possible.

## USAGE

In order to start, one should invoke a `Scraper` object. Here listed are the variables one can use:
1. **id**: to identify the video. Without it, the Scraper will not work. By default, it's `None`.
2. **driver**: method to give the driver to work. As for today, only *Chrome* has been tested successfully.
3. **scrape**: either `True` or `False`. If false, no scraping will be implemented after construction. By default, `True`.
4. **close_on_complete**: either `True` or `False`. If `True`, the program will quit the webpage. *If one has to implement the scraping of many pages, I suggest to put as `False`*.
5.  **comments_to_scrape**: maximum number of comments that will be scraped. If nothing is given, all visible will be scraped.

As of today, with the method `as_dict()`, results as dictionary can be obtained. Maybe I will implement more in the future.



Feel free to contact me. 😊

@ 2020, Leonardo Alchieri

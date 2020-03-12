#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""local_browser

NOTICE: Close Crawl runs its browser form submissions through Mechanize.
The module, however, is deprecated and does not support Python 3. The more
stable and maintained Mechanize and BeautifulSoup wrapper, MechanicalSoup,
will be replacing the Mechanize methods to support Python 3.

This module contains the configurations and settings for the browser used for
crawling and scraping through the pages in Close Crawl. The script contains the
implementation of the Session class which inherits attributes from the classobj
mechanize.Browser()

The script works as an internal module for Close Crawl, but can be imported
as a module for testing purposes.

TODO:
    Replace deprecated Mechanize with MechanicalSoup
    Fork Mechanize to support Python3

"""

from __future__ import absolute_import, print_function, unicode_literals
# import cookielib 
import http.cookiejar as cookielib # for Python3
import warnings
from urllib.request import urlopen
# from urllib import urlopen urllib.request

import mechanicalsoup

from .settings import HEADER, URL

warnings.filterwarnings("ignore", category=UserWarning)


class Session(object):

    def __init__(self):
        """Constructor

        Args:
            None

        Attributes:
            browser (`mechanize._mechanize.Browser`): browser object in session
        """

        self.browser = mechanicalsoup.StatefulBrowser()

        # set error and debug handlers for the browser

        # cookie jar
        self.browser.set_cookiejar(cookielib.LWPCookieJar())

        # browser options
        # self.browser.set_handle_equiv(True)
        # self.browser.set_handle_gzip(True)
        # self.browser.set_handle_redirect(True)
        # self.browser.set_handle_referer(True)
        # self.browser.set_handle_robots(False)

        # follows refresh 0 but doesn't hang on refresh > 0
        #self.browser.set_handle_refresh( _http.HTTPRefreshProcessor(), max_time=1 )

        # user-Agent
        # self.browser.addheaders = [("User-agent", HEADER)]

    def close(self):
        """Destructor for Session. Closes current browser session

        Args:
            None

        Returns:
            None
        """
        self.browser.close()

    def case_id_form(self, case):
        """Grabs the form in the case searching page, and inputs the
        case number to return the response.

        Args:
            case (`str`): case ID to be scraped

        Returns:
            response (`str`): HTML response
        """

        # iterate through the forms to find the correct one
        #for form in self.browser.forms():
        #    if form.attrs["name"] == "inquiryFormByCaseNum":
        #        self.browser.form = form
        #        break
        
        self.browser.select_form('form[action="/casesearch/inquiryByCaseNum.jis"]') 

        # submit case ID and return the response
        self.browser["caseId"] = case
        response = self.browser.submit_selected()
        response = response.text
        # if any( case_type in response.upper() for case_type in ("FORECLOSURE", "FORECLOSURE RIGHTS OF REDEMPTION", "MOTOR TORT") ): print (response.upper)

        self.browser.open("http://casesearch.courts.state.md.us/casesearch/inquiryByCaseNum.jis")
        # , "MOTOR TORT"
        return response if any(
            case_type in response.upper() for case_type in
            ("FORECLOSURE", "FORECLOSURE RIGHTS OF REDEMPTION")
        ) else False

    def disclaimer_form(self):
        """Navigates to the URL to proceed to the case searching page

        Args:
            None

        Returns:
            None
        """

        # visit the site
        print(URL)
        self.browser.open("http://casesearch.courts.state.md.us/casesearch/")

        # select the only form on the page
        self.browser.select_form('form')

        # select the checkbox
        self.browser["disclaimer"] = ['Y']

        # submit the form
        self.browser.submit_selected()

    @staticmethod
    def server_running():
        """Checks the status of the Casesearch servers

        Args:
            None

        Returns:
            `True` if server is up, `False` otherwise
        """
        return urlopen(URL).getcode() == 200

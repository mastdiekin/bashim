#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
import requests
from random import randint
import bs4

URL_BASE = 'https://bash.im'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
session = requests.session()
session.headers['User-Agent'] = USER_AGENT


def parse(obj) -> BeautifulSoup:
    return BeautifulSoup(obj, 'html.parser')


class BashRandomQuote:
    def __init__(self) -> None:
        self.pages_count = 0
        self.current_page = None
        self.rand_quote = None
        self.quote_rating = None
        self.quote_link = ''
        self.quote = ''

    def start(self,):
        self.get_pages_count()
        self.get_random_page()

    def get_pages_count(self):
        url = URL_BASE

        try:
            rs = session.get(url)
            root = parse(rs.content)
            self.pages_count = int(root.select('.pager__input')[0]['value'])

        except Exception as e:
            print(e)

    def get_random_page(self,):
        self.current_page = randint(1, self.pages_count)
        return self.current_page

    def get_random_quote_by_page(self, max_on_page):
        self.rand_quote = randint(0, max_on_page - 1)
        return self.rand_quote

    def clear_quote(self, quote):
        return self.get_plaintext(quote)

    def get_quote_rating(self, footer):
        try:
            self.quote_rating = int(footer.select('div.quote__total')[0].text)

        except Exception as e:
            print(e)

        return self.quote_rating

    def get_plaintext(self, element: Tag) -> str:
        items = []
        # try:
        #     element.find({'div', ".quote__strips"}).string = ''
        # except Exception:
        #     pass

        for elem in element.descendants:
            for child in list(elem)[1:]:
                try:
                    child.decompose()
                except AttributeError:
                    pass
            if isinstance(elem, str):
                items.append(elem.strip())
            elif elem.name in ['br', 'p']:
                items.append('\n')
        return ''.join(items).strip()

    def get_quote_link(self, header):
        h = None
        try:
            h = URL_BASE + header.select('.quote__header_permalink')[0]['href']

        except Exception as e:
            print(e)

        return h

    def get_random_quote(self, print_=True):
        url = URL_BASE
        url = urljoin(url, f'/index/{self.current_page}')
        try:
            rs = session.get(url)
            root = parse(rs.content)
            quotes = root.select('article.quote')

            len_of_page = len(quotes) - 1

            random_q = self.get_random_quote_by_page(len_of_page)

            header = quotes[random_q].select_one('.quote__header')
            body = quotes[random_q].select_one('.quote__body')
            footer = quotes[random_q].select_one('.quote__footer')

            self.quote_link = self.get_quote_link(header)
            self.quote = self.clear_quote(body)
            self.quote_rating = self.get_quote_rating(footer)

            if print_:
                self.print_cite()

            return self.quote_link, self.quote, self.quote_rating

        except Exception as e:
            print(e)

        return self.quote

    def print_cite(self,):
        print('\n', self.quote, sep='')
        print('_'*10, '\n')
        print('Rating:', self.quote_rating)
        print('Link:', self.quote_link)


def main():
    m = BashRandomQuote()
    m.start()
    m.get_random_quote(print_=True)


if __name__ == '__main__':
    main()

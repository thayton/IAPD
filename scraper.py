#!/usr/bin/env python

import re
import mechanize
from bs4 import BeautifulSoup

IAPD_URL = 'http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_Search.aspx'

class IapdScraper(object):
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape(self, q='1919 INVESTMENT COUNSEL, LLC'):
        def select_form(form):
            return form.attrs.get('id', None) == 'aspnetForm'

        self.br.open(IAPD_URL)
        self.br.select_form(predicate=select_form)
        self.br.form['ctl00$cphMainContent$ucUnifiedSearch$rdoSearchBy'] = ['rdoOrg']
        self.br.submit()

        self.br.select_form(predicate=select_form)
        self.br.form['ctl00$cphMainContent$ucUnifiedSearch$txtFirm'] = q
        self.br.submit()

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r'^ctl\d+_cphMainContent_grOrgResults$')
        t = s.find('table', id=r)

        tr = t.findAll('tr', recursive=False)
        tr = tr[2:-1] # Skip records-per-page header/footer and title header

        for row in tr:
            td = row.findAll('td')
            
            print td[0].b.text.strip()
            print td[1].text.strip()
            print td[2].text.strip()
            print td[3].text.strip()

if __name__ == '__main__':
    scraper = IapdScraper()
    scraper.scrape()

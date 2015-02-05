#!/usr/bin/env python

import os
import re
import sys
import django
import mechanize

from bs4 import BeautifulSoup
from xlrd import open_workbook

XLSX_FILE = 'Legal Names.xlsx'
IAPD_URL = 'http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_Search.aspx'

#------------------------------------------------------------------------------------------
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'scraper/scraper/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from custom_scraper.models import *
#------------------------------------------------------------------------------------------

def legal_names(file=XLSX_FILE):
    '''
    Read in legal names from the excel spreadsheet with the assumption
    that names to be searched for are in column 1. Skip row 1 header
    '''
    wb = open_workbook(file)
    s = wb.sheets()[0]

    col = 1
    for row in range(s.nrows)[1:]:
        name = s.cell(row, col).value
        if type(name) == int:
            continue

        yield name

class IapdScraper(object):
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]


    def scrape(self, q):
        '''
        Search for a Firm in the IAPD database by name
        '''
        def select_form(form):
            return form.attrs.get('id', None) == 'aspnetForm'

        try:
            firm = IapdFirm.objects.get(query_name=q)
        except ObjectDoesNotExist:
            firm = IapdFirm(query_name=q)
            firm.save()
        else:
            if firm.checked:
                return

        self.br.open(IAPD_URL)
        self.br.select_form(predicate=select_form)
        self.br.form['ctl00$cphMainContent$ucUnifiedSearch$rdoSearchBy'] = ['rdoOrg']
        self.br.submit()

        self.br.select_form(predicate=select_form)
        self.br.form['ctl00$cphMainContent$ucUnifiedSearch$txtFirm'] = q.encode('utf8')
        self.br.submit()

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r'^ctl\d+_cphMainContent_grOrgResults$')
        t = s.find('table', id=r)

        if not t: # Not found
            print 'Not Found'
            firm.checked = True
            firm.save()
            return 

        tr = t.findAll('tr', recursive=False)
        tr = tr[2:-1] # Skip records-per-page header/footer and title header

        for row in tr:
            td = row.findAll('td', recursive=False)

            firm.legal_name = td[0].b.text.strip()
            firm.other_name = td[1].text.strip()
            firm.sec_number = td[2].text.strip()
            firm.address = td[3].text.strip()
            firm.checked = True
            firm.save()

if __name__ == '__main__':
    scraper = IapdScraper()

    for name in legal_names():
        print '\nq=%s' % name
        scraper.scrape(q=name)

#!usr/bin/env python
# Heavily influenced by the R version of Seward Lee; https://github.com/sewardlee337/finreportr/blob/master/R/company_info.R
#
# Acquire basic company information
#'
#' Extracts and displays basic information relating to a given company in a data frame.
#'
#' @param symbol A character vector specifying the stock symbol of the company of interest.
#' @examples
#' CompanyInfo("GOOG")
#' CompanyInfo("TSLA")

import requests, bs4
import re
import pandas as pd

def CompanyInfo(symbol):
    
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={0}&owner=exclude&action=getcompany&Find=Search'.format(symbol)

    res = requests.get(url)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    
    # get all tag
    total = bs4.BeautifulSoup(res.text, 'lxml')
    # company info tag
    elems = total.find_all("span", class_="companyName")
    
    # Company name
    # this line is extracted from observing patterns in company names
    name = elems[0].getText().split('CIK#')[0]

    ##   Error message for function
    if (len(name) == 0):
        print("invalid company symbol")

    # CIK number
    CIK = elems[0].getText().split('CIK#')[1]
    CIK = re.findall(r'\d+',CIK)[0] # find all numbers

    ## SIC code
    elems = total.findAll("p", {"class":"identInfo"})
    
    ## Now find address
    elems = total.findAll("span", {"class":"mailerAddress"})
    ## mailing street is a standalone line
    mail_street = elems[2].getText()
    
    # all_address include state, city, zip code. Strip them one by one
    all_address = elems[3].getText().strip().rsplit(' ', 2)
    mail_city = all_address[0]
    mail_state = all_address[1]
    zip_code = all_address[2]
    
    # now phone number
    phone = elems[-1].getText()
    
    ## Now fiscal year end
    elems = total.findAll("p", {"class":"identInfo"})[0]
    fiscal_year = elems.contents[9].rsplit(' ', 2)[-1]
    
    ## Now incorporate state
    inc_state = elems.contents[8].getText() # state of incorporation
    
    # Wrap together and return a dictionary
    company_info = {}
    company_info['symbol'] = symbol
    company_info['name'] = name
    company_info['CIK'] = CIK
    company_info['SIC'] = SIC
    company_info['mail_street'] = mail_street
    company_info['mail_state'] = mail_state
    company_info['mail_city'] = mail_city
    company_info['zip_code'] = zip_code
    company_info['phone'] = phone
    company_info['fiscal_year'] = fiscal_year
    company_info['inc_state'] = inc_state
    company_info['loac_state'] = mail_state
    
    return pd.DataFrame([company_info], columns=company_info.keys())

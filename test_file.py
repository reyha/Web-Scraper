import unittest
import requests
from bs4 import BeautifulSoup as BS
from searchurl import search_url
from scraping import scrape

class Testing(unittest.TestCase):

    def test_search_url(self):
        
        # Makes sure no url is returned when match for company name is not found  
        
        company_name = "random"
        url = search_url(company_name)
        self.assertIsNone(url)

    def test_scrape(self):

        # Makes sure empty dicts are returned when neither bse nor nse is found for company. For example: SBI Magnum Express 
        
        url = 'http://www.moneycontrol.com/india/stockpricequote/finance-investments/sbimagnumexpress/SBI06'  
        company_url = requests.get(url)
        soup = BS(company_url.text, "html.parser")
        b, n = scrape(soup)
        self.assertEqual(b, {})
        self.assertEqual(n, {})

if __name__ == '__main__':
    unittest.main()

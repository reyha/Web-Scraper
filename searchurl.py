from bs4 import BeautifulSoup as BS
import requests

def search_url(cname):
    base_url = 'http://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php?search_data=&cid=&mbsearch_str=&topsearch_type=1&search_str=' + cname
    company_url = requests.get(base_url)
    soup = BS(company_url.text, "html.parser")
    search_results = soup.find('table', {"class":"srch_tbl"})
    if search_results:
        results = search_results.findAll('a',href=True)
        for r in results:
            if cname.lower() in r.text.lower():
                c_url =  r['href'].strip("http://")
                c_url = "http://" +  c_url
                return c_url  
            else:
                return        
    else:
        return
    

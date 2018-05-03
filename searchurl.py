from bs4 import BeautifulSoup as BS
import requests
import json
def search_url(cname):
    base_url = 'https://www.moneycontrol.com/mccode/common/autosuggesion.php?query=' + cname + '&type=1&format=json&callback=suggest1'
    response = requests.get(base_url)
    link = json.loads(response.text[9:-1])[0]['link_src']
    if link == "javascript:void(0)":
        return None
    else:
        return link
    

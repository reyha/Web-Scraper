from bs4 import BeautifulSoup
import re

def scrape(soup):
	
    b = {}
    n = {}

    # To check if company is listed on BSE and NSE  

    bse_content = soup.find(id="Bse_Prc_tick_div")
    nse_content = soup.find(id="Nse_Prc_tick_div")

    
    if bse_content:  

        ## BSE Contents

        # 1. Date and time
        bse_datetime = soup.find(id="bse_upd_time").string
        split_bse_datetime = bse_datetime.split(', ')
        b['bse_date'] = split_bse_datetime[0]
        b['bse_time'] = split_bse_datetime[1]
            
        # 2. Current Price
        b['bse_current_price'] = soup.find(id="Bse_Prc_tick").string

        # 3. Absolute increase/decrease in price
        bse_price = soup.find(id="b_changetext").text.strip().split(' ')
        b['bse_abs_price'] = bse_price[0]

        # 4. Percentage increase/decrease in price
        bse_per_price = bse_price[1]
        b['bse_per'] = re.findall(r'\d+\.\d+', bse_per_price)[0]

        # 5. Volume
        b['bse_volume'] = soup.find(id="bse_volume").text

        # 6. Previous Close, Open Price, Bid Price (Qty.), Offer Price (Qty.)
        b['bse_prev_close'] = soup.find(id="b_prevclose").text
        b['bse_open_price'] = soup.find(id="b_open").text
        b['bse_bid_price'] = soup.find(id="b_bidprice_qty").text
        b['bse_offer_price'] = soup.find(id="b_offerprice_qty").text

    if nse_content:

	## NSE Contents
        # 1. Date and time
        nse_datetime = soup.find(id="nse_upd_time").string
        split_nse_datetime = nse_datetime.split(', ')
        n['nse_date'] = split_nse_datetime[0]
        n['nse_time'] = split_nse_datetime[1]

        # 2. Current Price
        n['nse_current_price'] = soup.find(id="Nse_Prc_tick").string

        # 3. Absolute increase/decrease in price
        nse_price = soup.find(id="n_changetext").text.strip().split(' ')
        n['nse_abs_price'] = nse_price[0]

        # 4. Percentage increase/decrease in price
        nse_per_price = nse_price[1]
        n['nse_per'] = re.findall(r'\d+\.\d+', nse_per_price)[0]

        # 5. Volume
        n['nse_volume'] = soup.find(id="nse_volume").text

        # 6. Previous Close, Open Price, Bid Price (Qty.), Offer Price (Qty.)
        n['nse_prev_close'] = soup.find(id="n_prevclose").text
        n['nse_open_price'] = soup.find(id="n_open").text
        n['nse_bid_price'] = soup.find(id="n_bidprice_qty").text
        n['nse_offer_price'] = soup.find(id="n_offerprice_qty").text
    
    return (b, n)

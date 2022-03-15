from bs4 import BeautifulSoup
import dask, requests, time
import pandas as pd

base_url = 'https://www.lider.cl/supermercado/category/Despensa/?No={}&isNavRequest=Yes&Nrpp=40&page={}'

def scrape(id):
    page = id+1; start = 40*page
    bs = BeautifulSoup(requests.get(base_url.format(start,page)).text,'lxml')
    prods = [prod.text for prod in bs.find_all('span',attrs={'class':'product-description js-ellipsis'})]
    prods = [prod.text for prod in prods]
    brands = [b.text for b in bs.find_all('span',attrs={'class':'product-name'})]

    sdf = pd.DataFrame({'product': prods, 'brand': brands})
    return sdf

data = [dask.delayed(scrape)(id) for id in range(10)]
df = dask.delayed(pd.concat)(data)
df = df.compute()

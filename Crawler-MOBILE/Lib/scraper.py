import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://mobile.bg"
#BASE_URL = "https://m.mobile.bg/results?pubtype=1&model=120&marka=BMW&sort=3&#currency=%D0%A0%C2%BB%D0%A0%D0%86.&nup=0~1&slink=qgyawr"
#url = urljoin(BASE_URL )
html = requests.get(BASE_URL, "/results?pubtype=1&model=120&marka=BMW&sort=3&#currency=%D0%A0%C2%BB%D0%A0%D0%86.&nup=0~1&slink=qgyawr")

def scrape_links (html):
    links_id = []
    sity = []

    soup = BeautifulSoup(html.content, "html.parser")
    table = soup.find ( """ div _ngcontent-my-app-c52 class="page" """)

    rows= soup.find_all ( """div _ngcontent-my-app-c52=""                   class="ng-star-inserted" """)

    for info in rows:
        sity_info = info.find( """advertl _ngcontent-my-app-c52="" index="results" """)
        sity_info = info.get_text()
        if sity_info == str( 'София') :
            sity.append(sity_info)
            a = sity.find ( "div" "id =" )
            links_id.append(urljoin(BASE_URL, a['id'])) 

    

if __name__ == "__main__":
    scrape_links(html)
            
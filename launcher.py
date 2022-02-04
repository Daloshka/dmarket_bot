from fake_useragent import UserAgent
import requests
import json
import csv

#https://steamcommunity.com/market/priceoverview/?appid=730&country=RU&currency=5&market_hash_name=Sticker%20%7C%20Purple%20Cyclawps
# create UserAgent
ua = UserAgent()

# Price from  - to in RUB
priceFrom = 100
priceTo = 1000

def collect_data(priceFrom=priceFrom, priceTo=priceTo):
    # get html page
    response = requests.get(
        url=f'https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=best_deals&orderDir=desc&title=&priceFrom={priceFrom}&priceTo={priceTo}&treeFilters=category_1%5B%5D=not_souvenir,categoryPath%5B%5D=pistol,categoryPath%5B%5D=smg,categoryPath%5B%5D=rifle,categoryPath%5B%5D=sniper%20rifle,categoryPath%5B%5D=shotgun,categoryPath%5B%5D=machinegun&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser&isLoggedIn=true',
        #url = f'https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=best_deals&orderDir=desc&title=&priceFrom=3500&priceTo=4039&treeFilters=category_1%5B%5D=not_souvenir,categoryPath%5B%5D=pistol,categoryPath%5B%5D=rifle,categoryPath%5B%5D=sniper%20rifle/ssg%2008,categoryPath%5B%5D=sniper%20rifle/awp&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser&isLoggedIn=true',
        headers={'user-agent': f'{ua.random}'}
    )

    # make only one transition to json to make one request instead of lots
    response_json = response.json()

    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(response_json, file, indent=4, ensure_ascii=False)

    # start work with json text
    data = response_json
    objects = data.get('objects')

    # open price table
    

    # print information about items
    for i in objects:
        if i.get('extra').get('stickers') is not None:
            sTitles = ''
            sTotal = 0
            for j in i.get('extra').get('stickers'):
                with open('price_table.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for line in csv_reader:
                        if j['name'] in line:
                            sTotal = float(sTotal) + float(line[1])      
                sTitles += j['name'] + '\n'
            if sTotal >= 300:
                with open('WeaponTitles.txt', 'a', encoding="utf-8") as file:
                    file.write(f"{i.get('price').get('USD')} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}\nStickers price: {sTotal}\n\n")
                print(f"{i.get('price').get('USD')} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}\nStickers price: {sTotal}\n")

def main():
    clearWeaponTitles()
    for i,j in [300,500],[500,700],[700,800]:
        collect_data(i,j)

# function to clear saved info in Weapon Titles
def clearWeaponTitles():
    with open('WeaponTitles.txt', 'w') as file:
        file.write('')

if __name__ == "__main__":
    main()
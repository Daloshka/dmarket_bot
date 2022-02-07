from fake_useragent import UserAgent
import requests
import json
import csv
import win10toast

#https://steamcommunity.com/market/priceoverview/?appid=730&country=RU&currency=5&market_hash_name=Sticker%20%7C%20Purple%20Cyclawps

# create UserAgent
ua = UserAgent()

# Price from  - to in RUB
priceFromTo = [100,150],[150,200],[250,300],[300,350],[350,400]
min_total_sticker = 400

def notify(skin, skin_price, sTotal):
    toast = win10toast.ToastNotifier()
    notification = toast.show_toast(title=f"{skin}", msg=f"Цена скина = {skin_price}  руб.\nЦена наклеек = {sTotal} руб.", duration = 10)


def collect_data(priceFrom, priceTo):
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
        skin_price = i.get('price').get('USD')
        skin = i.get('title')
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
            if sTotal >= min_total_sticker:
                with open('WeaponTitles.txt', 'a', encoding="utf-8") as file:
                    file.write(f"{skin_price} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}\nStickers price: {sTotal}\n\n")
                print(f"{skin_price} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}\nStickers price: {sTotal}\n")
                notify(skin, skin_price, sTotal)

def main():
    clearWeaponTitles()
    for i,j in priceFromTo:
        collect_data(i,j)
    # for i,j in [2500,2600],[2600,2700],[2700,2800]:
    #     collect_data(i,j)
    # for i,j in [2000,2100],[2100,2200],[2200,2300]:
    #     collect_data(i,j)
    # for i,j in [2800,2900],[3000,3100],[3100,3200]:
    #     collect_data(i,j)
    # for i,j in [3200,3300],[3300,3400],[3400,3500]:
    #     collect_data(i,j)

# function to clear saved info in Weapon Titles
def clearWeaponTitles():
    with open('WeaponTitles.txt', 'w') as file:
        file.write('')

if __name__ == "__main__":
    main()
from fake_useragent import UserAgent
import requests
import json

# create UserAgent
ua = UserAgent()

def collect_data():
    # get html page
    response = requests.get(
        url='https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=best_deals&orderDir=desc&title=&priceFrom=300&priceTo=700&treeFilters=category_1%5B%5D=not_souvenir,categoryPath%5B%5D=pistol,categoryPath%5B%5D=smg,categoryPath%5B%5D=rifle,categoryPath%5B%5D=sniper%20rifle,categoryPath%5B%5D=shotgun,categoryPath%5B%5D=machinegun&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser&isLoggedIn=true',
        headers={'user-agent': f'{ua.random}'}
    )

    # make only one transition to json to make one request instead of lots
    response_json = response.json()

    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(response_json, file, indent=4, ensure_ascii=False)

    # start work with json text
    data = response_json
    objects = data.get('objects')

    # print information about items
    for i in objects:
        if i.get('extra').get('stickers') is not None:
            sTitles = ''
            for j in i.get('extra').get('stickers'):
                sTitles += j['name'] + '\n'
            with open('WeaponTitles.txt', 'a', encoding="utf-8") as file:
                file.write(f"{i.get('price').get('USD')} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}\n")
            print(f"{i.get('price').get('USD')} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}")

def main():
    clearWeaponTitles()
    collect_data()

# function to clear saved info in Weapon Titles
def clearWeaponTitles():
    with open('WeaponTitles.txt', 'w') as file:
        file.write('')


if __name__ == "__main__":
    main()
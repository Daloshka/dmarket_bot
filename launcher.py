from fake_useragent import UserAgent
import requests
import json
import csv
import win10toast
from tkinter import *

# create UserAgent
ua = UserAgent()



def skin_prices(priceFrom=100,priceTo=3000):
    priceFromTo = []
    changedPrice = priceFrom
    plusPriceFrom = int(round((priceTo - priceFrom)/6))
    for i in range(6):
        changedPrice += plusPriceFrom
        priceFromTo.append([priceFrom, changedPrice])
        priceFrom += plusPriceFrom
    print(priceFromTo)
    return priceFromTo

# notificatoion
def notify(skin = "Example", skin_price = "123", sTotal = "123"):
    toast = win10toast.ToastNotifier()
    notification = toast.show_toast(title=f"{skin}", msg=f"Цена скина = {skin_price}  руб.\nЦена наклеек = {sTotal} руб.", duration=4)

# main function
def collect_data(priceFrom, priceTo):
    # get html page
    response = requests.get(
        url=f'https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=best_deals&orderDir=desc&title=&priceFrom={priceFrom}&priceTo={priceTo}&treeFilters=category_1%5B%5D=not_souvenir,categoryPath%5B%5D=pistol,categoryPath%5B%5D=smg,categoryPath%5B%5D=rifle,categoryPath%5B%5D=sniper%20rifle,categoryPath%5B%5D=shotgun,categoryPath%5B%5D=machinegun&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser&isLoggedIn=true',
        headers={'user-agent': f'{ua.random}'}
    )

    # make only one transition to json to make one request instead of lots
    response_json = response.json()

    # create json with parsed info
    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(response_json, file, indent=4, ensure_ascii=False)

    # start work with json text
    data = response_json
    objects = data.get('objects')

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
                #notify(skin, skin_price, sTotal)

# function to clear saved info in Weapon Titles
def clearWeaponTitles():
    with open('WeaponTitles.txt', 'w') as file:
        file.write('')

def main():
    clearWeaponTitles()
    for i,j in getPp():
        collect_data(i,j)

def getPp():
        priceFromTo = skin_prices(int(price_from_enter.get()),int(price_to_enter.get()))
        return priceFromTo

if __name__ == "__main__":
    min_total_sticker = 400
    #creat Menu
    root = Tk()
    root.title("Dmarket Helper")
    root.geometry("1280x720")
    root.resizable(width = False, height = False)

    #Background
    root.image = PhotoImage(file='D:\\New Unity Project\\Assets\\Dmarket Bot\\img\\dmarket.png')
    root.iconbitmap('D:\\New Unity Project\\Assets\\Dmarket Bot\\img\\dmarket_logo.ico')
    bg_logo = Label(root, image=root.image)
    bg_logo.place(x=0,y=0, relheight=1, relwidth=1)

    # Enter boxes
    price_from_enter = StringVar()
    price_to_enter = StringVar()
    message_entry = Entry(textvariable=price_from_enter)
    message_entry.place(relx=.45, rely=.85, anchor="c")
    message_entry2 = Entry(textvariable=price_to_enter)
    message_entry2.place(relx=.55, rely=.85, anchor="c")

    butt = Button(root, text="Search", bg="#C9ACAE")
    butt.place(relx=0.48, rely=0.88)
    butt.config(command=main)
    butt2 = Button(root, text="Set Price", bg="#C9ACAE")
    butt2.place(relx=0.48, rely=0.86)
    butt2.config(command=getPp)

    # Input price from - to
    # Price from  - to in RUB
    
    


    root.mainloop()


    #main()
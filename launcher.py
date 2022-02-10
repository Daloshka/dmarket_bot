from fake_useragent import UserAgent
import requests
import json
import csv
import win10toast
from tkinter import *
import telebot


# create UserAgent
ua = UserAgent()

# Telebot
# bot = telebot.TeleBot('5234922052:AAGAPSSPwhrSj3oe2wS3sS151HHadX6NWZ0')
# chat_id = -1001625897184

def skin_prices(priceFrom=100,priceTo=3000):
    priceFromTo = []
    changedPrice = priceFrom
    plusPriceFrom = int(round((priceTo - priceFrom)/10))
    for i in range(10):
        changedPrice += plusPriceFrom
        priceFromTo.append([priceFrom, changedPrice])
        priceFrom += plusPriceFrom
    print(priceFromTo)
    return priceFromTo

# windows notificatoion
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
        discount = f"Discount -{i.get('discount')}%"
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
            if sTotal >= min_total_sticker.get() and i.get('discount') >= 15:
                with open('WeaponTitles.txt', 'a', encoding="utf-8") as file:
                    file.write(f"{skin_price} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}\nDiscount -{i.get('discount')}%\nStickers price: {sTotal}\n\n-----------------------------------------------------------------------------------------------------\n\n")
                print(f"{skin_price} руб   {i.get('title')}\nfloat={i.get('extra').get('floatValue')} \n{sTitles}\nDiscount -{i.get('discount')}%\nStickers price: {sTotal}\n-----------------------------------------------------------------------------------------------------\n\n")
                #notify(skin, skin_price, sTotal)
                msgs[skin] = discount, skin_price, skin, sTotal
# function to clear saved info in Weapon Titles
def clearWeaponTitles():
    with open('WeaponTitles.txt', 'w') as file:
        file.write('')

def main():
    clearWeaponTitles()
    for i,j in getPp():
        collect_data(i,j)

# 
def getPp():
        priceFromTo = skin_prices(int(price_from_enter.get()),int(price_to_enter.get()))
        return priceFromTo

# get info about skin for Telegram bot
def saveInfo(skin_price, skin, discount, sTotal):
    msgs.append(f"{skin_price} руб,\n{skin}\n-{discount}%\n{sTotal}")

#telegram msgs
msgs = {}
if __name__ == "__main__":
    
    min_total_sticker = 100

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
    # Input price from - to
    price_from_enter = IntVar()
    price_from_enter.set(100)
    price_to_enter = IntVar()
    price_to_enter.set(600)
    min_discount = IntVar()
    min_discount.set(10)
    min_total_sticker = IntVar()
    min_total_sticker.set(300)


    lbl = Label(root, text="from", font=("Hemi Head", 15), bg="#05151f", fg="#FFFFFF")
    lbl2 = Label(root, text="to", font=("Hemi Head", 15), bg="#05151f", fg="#FFFFFF")
    lbl3 = Label(root, text="discount", font=("Hemi Head", 15), bg="#05151f", fg="#FFFFFF")
    lbl4 = Label(root, text="stickers", font=("Hemi Head", 15), bg="#05151f", fg="#FFFFFF")
    
    message_entry = Entry(textvariable=price_from_enter, width=10, justify=LEFT)
    message_entry.grid(column=1, row=0, sticky=W)
    message_entry2 = Entry(textvariable=price_to_enter, width=10, justify=LEFT)
    message_entry2.grid(column=1, row=1, sticky=W)
    message_entry3 = Entry(textvariable=min_discount, width=10, justify=LEFT)
    message_entry3.grid(column=1, row=2, sticky=W)
    message_entry4 = Entry(textvariable=min_total_sticker, width=10, justify=LEFT)
    message_entry4.grid(column=1, row=3, sticky=W)
    lbl.grid(column=0, row=0)
    lbl2.grid(column=0, row=1)
    lbl3.grid(column=0, row=2)
    lbl4.grid(column=0, row=3)
    
    butt = Button(root, text="Search", bg="#05151f", fg="#FFFFFF")
    butt.grid(column=0, row=4, columnspan=2)
    butt.config(command=main)

    #bot.polling()
    root.mainloop()
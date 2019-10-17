import requests
import json
from bs4 import BeautifulSoup
import csv


def get_page(url):
    res=requests.get(url)
    # print(res.ok)
    # print(res.status_code)

    if not res.ok:
        print("server responded :",res.status_code)
    else:
        soup=BeautifulSoup(res.text,"lxml")
    return soup



def get_data(s): 
    try:
        title=s.find('h1',id="itemTitle").text.replace(u'\xa0',"").replace("Details about","").strip()
        #print(title)
    except:
        title=" "    

    try:
        price=s.find('div',id="prcIsumConv").text.replace("Approximately INR ","").replace("(including shipping)","")
        #print(price)    
    except:
        price=" "    


    try:
        try:
            sold=s.find('span',class_="vi-qtyS").find('a').text.strip().split(" ")[0]
            #print(sold) 
        except:
            sold=s.find('span',class_="convbinPrice").find('a').text.strip().split(" ")[0]

    except:
        sold=" "  

    # try:
    #     place=s.find('span',class_='s-item__location')
    #     print(place.text)
    # except Exception as e:
    #     print(e)    


    data={
        "title":title,
        "price":price,
        "sold":sold,
        #"place":place
    }


    return data



def get_links(soup):
    list=[]
    links=soup.find_all('a',class_="s-item__link")      
    for item in links:
        list.append(item.get("href"))

    #print(list)
    #print(len(list)) 
    return list


def write_to_csv(data,url):
    with open('ebaydata.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        row=[data['title'],data['price'],data['sold'],url]
        writer.writerow(row)
    csvFile.close()


def main():
    url="https://www.ebay.com/sch/i.html?_nkw=mens+watches&_pgn=1"
    #get_data(get_page(url))
    watches=get_links(get_page(url))
    for item in watches:
        data=get_data(get_page(item))
        write_to_csv(data,item)
        #print(data)


if __name__ == "__main__":
    main()




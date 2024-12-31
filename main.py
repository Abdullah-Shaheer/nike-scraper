import time
import requests
import json
import pandas as pd
import sqlite3


def scrape():
    cookies = {
        'geoloc': 'cc=PK,rc=,tp=vhigh,tz=GMT+5,la=33.70,lo=73.17',
        'mboxEdgeCluster': '41',
        'mbox': 'session#e23b2af8ccc33a862e7a7ed8f938d1e5#1735641375|PC#df034998815fe6bd7dfd612a4498ea6d.41_0#1798884316',
        'ni_d': 'D6DA759C-E966-47FC-a25A-3827C290B75D',
        'anonymousId': '8C606158A9A20713C3C154F33D28B6DF',
        'AKA_A2': 'A',
        'ak_bmsc': 'D8B8336679DA4AFA60C9170DDCC23539~000000000000000000000000000000~YAAQF2nDF8bc5reTAQAAn0EtHBpwXzFU5Bwc0OmWKIBwBaVNpxiU3E5hQjGSLi7goERPbZ6F6EiZuLytBqBb8LUXym5wXDoX8fTfgxraWNJnUeAdgD2RyR1lGZsDMuq98RajA6ekkM6hVdYA1va9gYCW/kQwYQLi2Nq1OYLmcBZ1pPWHAbBBJUo9HOZJXC8HOxG24JndUC7Jr1Jd6X/M9YK0DDpXfPZzdtehtB0lwaeBwnSJTIsD3lTQjkyOO/JZKLtjl+BVlS/z+koulDUpvSbSF1343OXxIj/bKRiM3kTPyRoaobPoETp2ZJ7TEbqtnsEriuWFU3CN+ekMt1w9GCCVf1C4b3DbiIxkv2ljOKy6HzgCVq3HfUP7Vxfj3vMYoiWXiMlrItc=',
        'KP_UIDz-ssn': '0blNbnSyLLeot8UTTsdMsJ9sZob2c7EEoskI4sVH3CZ7Bh6SJetjr6kUlOfoqm34DRuzvFn6Uysrtc49dW9qaamSJE1Y2MR1qdfwKUQicvckOnICtJnARvPa0gBq3r4j42mtFzi1Gtrr9DBGcNx4dPXIdrp6MXZNtGHI2Nz',
        'KP_UIDz': '0blNbnSyLLeot8UTTsdMsJ9sZob2c7EEoskI4sVH3CZ7Bh6SJetjr6kUlOfoqm34DRuzvFn6Uysrtc49dW9qaamSJE1Y2MR1qdfwKUQicvckOnICtJnARvPa0gBq3r4j42mtFzi1Gtrr9DBGcNx4dPXIdrp6MXZNtGHI2Nz',
        'ni_c': '1PA=1|BEAD=1|PERF=1|PERS=1',
        'sq': '3',
        'AMCV_F0935E09512D2C270A490D4D%40AdobeOrg': '1994364360%7CMCMID%7C24499658103743258856248653752155023585%7CMCAID%7CNONE%7CvVersion%7C3.4.0',
        'ni_cs': '98b1615f-f8bc-4c91-8ed0-bb6d7f2861d4',
        'NIKE_COMMERCE_COUNTRY': 'US',
        'NIKE_COMMERCE_LANG_LOCALE': 'en_US',
        'nike_locale': 'us/en_us',
        'CONSUMERCHOICE': 'us/en_us',
        'CONSUMERCHOICE_SESSION': 't',
        'ppd': 'pw|nikecom>pw>men_shoes',
        'bm_sv': '9AE8897605CBD6FAAF417F41E4BAE488~YAAQVW/ZF8bgHLSTAQAA4D8wHBofFtvZDgHEoOXAuwPIHZFGmZhmYW2FJuNddEkWRaPKd5299MBsZgK4QnVMRSKGgiYMjK6Xxnaefmj64MCK4QHovueGDpbPwKzwcod5sdGLu/9wc8UNJwqXKIDpRiu5WMGD8YaosFi9ycpEiA440jZQu/er4xHtHmIpUkq6OVWQHw53TxMz2+Rvykn0dzhRuuArcNappjE4XzF5VDj3NdznxE8KrJ3K3e1a1Is=~1',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'anonymousid': '8C606158A9A20713C3C154F33D28B6DF',
        # 'cookie': 'geoloc=cc=PK,rc=,tp=vhigh,tz=GMT+5,la=33.70,lo=73.17; mboxEdgeCluster=41; mbox=session#e23b2af8ccc33a862e7a7ed8f938d1e5#1735641375|PC#df034998815fe6bd7dfd612a4498ea6d.41_0#1798884316; ni_d=D6DA759C-E966-47FC-a25A-3827C290B75D; anonymousId=8C606158A9A20713C3C154F33D28B6DF; AKA_A2=A; ak_bmsc=D8B8336679DA4AFA60C9170DDCC23539~000000000000000000000000000000~YAAQF2nDF8bc5reTAQAAn0EtHBpwXzFU5Bwc0OmWKIBwBaVNpxiU3E5hQjGSLi7goERPbZ6F6EiZuLytBqBb8LUXym5wXDoX8fTfgxraWNJnUeAdgD2RyR1lGZsDMuq98RajA6ekkM6hVdYA1va9gYCW/kQwYQLi2Nq1OYLmcBZ1pPWHAbBBJUo9HOZJXC8HOxG24JndUC7Jr1Jd6X/M9YK0DDpXfPZzdtehtB0lwaeBwnSJTIsD3lTQjkyOO/JZKLtjl+BVlS/z+koulDUpvSbSF1343OXxIj/bKRiM3kTPyRoaobPoETp2ZJ7TEbqtnsEriuWFU3CN+ekMt1w9GCCVf1C4b3DbiIxkv2ljOKy6HzgCVq3HfUP7Vxfj3vMYoiWXiMlrItc=; KP_UIDz-ssn=0blNbnSyLLeot8UTTsdMsJ9sZob2c7EEoskI4sVH3CZ7Bh6SJetjr6kUlOfoqm34DRuzvFn6Uysrtc49dW9qaamSJE1Y2MR1qdfwKUQicvckOnICtJnARvPa0gBq3r4j42mtFzi1Gtrr9DBGcNx4dPXIdrp6MXZNtGHI2Nz; KP_UIDz=0blNbnSyLLeot8UTTsdMsJ9sZob2c7EEoskI4sVH3CZ7Bh6SJetjr6kUlOfoqm34DRuzvFn6Uysrtc49dW9qaamSJE1Y2MR1qdfwKUQicvckOnICtJnARvPa0gBq3r4j42mtFzi1Gtrr9DBGcNx4dPXIdrp6MXZNtGHI2Nz; ni_c=1PA=1|BEAD=1|PERF=1|PERS=1; sq=3; AMCV_F0935E09512D2C270A490D4D%40AdobeOrg=1994364360%7CMCMID%7C24499658103743258856248653752155023585%7CMCAID%7CNONE%7CvVersion%7C3.4.0; ni_cs=98b1615f-f8bc-4c91-8ed0-bb6d7f2861d4; NIKE_COMMERCE_COUNTRY=US; NIKE_COMMERCE_LANG_LOCALE=en_US; nike_locale=us/en_us; CONSUMERCHOICE=us/en_us; CONSUMERCHOICE_SESSION=t; ppd=pw|nikecom>pw>men_shoes; bm_sv=9AE8897605CBD6FAAF417F41E4BAE488~YAAQVW/ZF8bgHLSTAQAA4D8wHBofFtvZDgHEoOXAuwPIHZFGmZhmYW2FJuNddEkWRaPKd5299MBsZgK4QnVMRSKGgiYMjK6Xxnaefmj64MCK4QHovueGDpbPwKzwcod5sdGLu/9wc8UNJwqXKIDpRiu5WMGD8YaosFi9ycpEiA440jZQu/er4xHtHmIpUkq6OVWQHw53TxMz2+Rvykn0dzhRuuArcNappjE4XzF5VDj3NdznxE8KrJ3K3e1a1Is=~1',
        'nike-api-caller-id': 'nike:dotcom:browse:wall.client:2.0',
        'origin': 'https://www.nike.com',
        'priority': 'u=1, i',
        'referer': 'https://www.nike.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    i = 0
    page = 0
    scraped_data = []
    while True:
        try:
            print(f'Scraping data from page {page + 1}')
            response = requests.get(
                f'https://api.nike.com//discover/product_wall/v1/marketplace/US/language/en/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647?path=/w/mens-shoes-nik1zy7ok&attributeIds=16633190-45e5-4830-a068-232ac7aea82c,0f64ecc7-d624-4e91-b171-b83a03dd8550&queryType=PRODUCTS&anchor={i}&count=24',
                cookies=cookies,
                headers=headers,
            )
            i += 24
            page += 1
            data = response.json()
            product_groupings = data.get('productGroupings', [])
            for product in product_groupings:
                products = product.get('products', [])
                if not products:
                    continue

                main_product = products[0]
                scraped_data.append({
                    "title": main_product.get('copy', {}).get('title', ''),
                    "current_price": f"{main_product.get('prices', {}).get('currentPrice', '')}$",
                    "discount_percentage": f"{main_product.get('prices', {}).get('discountPercentage', '')}%",
                    "main_url": main_product.get('pdpUrl', {}).get('url', ''),
                    "image": main_product.get('colorwayImages', {}).get('portraitURL', ''),
                    "product_code": main_product.get('productCode', ''),
                    "global_product_id": main_product.get('globalProductId', ''),
                    "group_key": main_product.get('groupKey', ''),
                    "color_description": main_product.get('displayColors', {}).get('colorDescription', ''),
                    "simple_color": main_product.get('displayColors', {}).get('simpleColor', {}).get('label', ''),
                    "sub_title": main_product.get('copy', {}).get('subTitle', ''),
                    "merch_product_id": main_product.get('merchProductId', ''),
                    "internal_pid": main_product.get('internalPid', ''),
                    "consumer_channel_id": main_product.get('consumerChannelId', ''),
                })

        except Exception as e:
            print("All data has been scraped.")
            break

    return scraped_data


def info():
    print('This Nike scraper has been build by github.com/Abdullah-Shaheer')
    print('[+] Fast')
    print("[+] API Based")
    print("[+] Output in excel, json, csv and sqlite3")
    print("Going to start scraping ......")
    time.sleep(3)


def main():
    info()
    scraped_data = scrape()
    df = pd.DataFrame(scraped_data)

    df.to_csv("products.csv", index=False)
    print("Data saved to CSV file: products.csv")

    df.to_excel("products.xlsx", index=False)
    print("Data saved to Excel file: products.xlsx")

    with open("products.json", "w") as json_file:
        json.dump(scraped_data, json_file, indent=4)
    print("Data saved to JSON file: products.json")

    conn = sqlite3.connect("products.db")
    df.to_sql("products", conn, if_exists="replace", index=False)
    conn.close()
    print("Data saved to SQLite database: products.db")


if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import time
from bs4 import BeautifulSoup
import requests
import numpy as np
from numpy import genfromtxt
from PIL import Image, ImageDraw, ImageFont

with open('ICAO.txt','r') as f:
    lines = f.readlines()
    content = f.readlines()
    for line in lines:
        print(line,end="")

with open('yn.txt','r') as f:
    lines = f.readlines()
    content = f.readlines()
    for yn in lines:
        print(yn,end="")

with open('taf.txt','r') as f:
    lines = f.readlines()
    content = f.readlines()
    for tafyn in lines:
        print(yn,end="")

# Copyrights©Shepard Deng VATSIM ID 1434656 and Hunyx, not for commercial use, For
# fight simulation only, do not use for actual flight

print("Copyrights©Shepard Deng VATSIM ID 1434656 and Hunyx, not for commercial use, \n"
      "For fight simulation only, do not use for actual flight\n")


# convert csv file to image
def convert_img(data, count, is_raw):
    # find the max length of text
    length = []
    for index in range(data.shape[0]):
        length.append(len(data[index]))
    max_length = max(length)
    # print(max_length)

    # creat image for plotting
    img_length = max_length * 12
    img_width = data.shape[0] * 30
    data_found = True
    for row_1 in range(data.shape[0]):
        temp_1 = data[row_1]
        if 'Text' in temp_1 and len(temp_1) == max_length and len(temp_1) > 60:  # change img length if text is too long
            print('Long!!!!!!!')
            img_length = max_length * 14
        if is_raw and max_length > 60:  # change img length if text is too long
            print('Long!!!!!!!')
            img_length = max_length * 14
        if 'No data found' in temp_1:
            data_found = False
    if img_width < 300:
        img_width = 300
    # print No data if no data
    if not data_found:
        for row_1 in range(data.shape[0]):
            data[row_1] = 'No data found'
        print(data)

    # creat image
    img = Image.new('RGB', (img_length, img_width), color=(255, 255, 255))
    # set font
    fnt = ImageFont.truetype(font='arial.ttf', size=24)
    # plot texts on image
    d = ImageDraw.Draw(img)
    for line in range(data.shape[0]):
        d.text((20, line * 30), data[line], fill=(0, 0, 0), font=fnt)

    # rotate image to vertical
    rotate = img.transpose(Image.ROTATE_90)
    # save images
    img.save('img_' + str(count) + '.png')
    rotate.save('rotate_' + str(count) + '.png')
    print('Image ' + str(count) + ' saved')


# get the raw data
def raw_data():
    # 使用 ZUUU KIWA KLAX KPHX 作为测试航站
    # Use ZUUU KIWA KLAX KPHX for testing
    
    stationx = line
    if len(stationx) != 4:
        print('ERROR: The station code must be four digits / 航站代码必须为四位')
        return
    
    kv = {'data?ids': 'KIWA'}
    r = requests.get("https://www.aviationweather.gov/metar/data?ids=" + stationx +
                     "&format=raw&date=&hours=0&taf=on", params=kv)
    print('数据从NOAA获得''\ndata retrived from:NOAA\n')
    # web spider from aviationweather.gov
    # —————————————————————————————————————————————————————————————————————————————————————————————————————————————
    url = ("https://www.aviationweather.gov/metar/data?ids=" + stationx + "&format=raw&date=&hours=0&taf=on")
    response = requests.get(url)
    text = response.text
    enco = response.encoding
    text = text.encode(enco).decode('UTF-8')
    html = BeautifulSoup(text, 'html.parser')

    source_raw_metar = html.select('#awc_main_content_wrap > code:nth-child(3)')
    # 此项为metar数据，网页端日期下面第一行
    source_raw_taf = html.select('#awc_main_content_wrap > code:nth-child(6)')
    # 此项为taf数据，网页端日期下面第二行

    print(source_raw_metar[0].get_text())
    print(source_raw_taf[0].get_text())

    return source_raw_metar, source_raw_taf


# get the decoded data
def decode_data():
    # 使用   ZUUU KIWA KLAX KPHX 作为测试航站
    # Use    ZUUU KIWA KLAX KPHX for testing
    stationx = line
    if len(stationx) != 4:
        print('ERROR: The station code must be four digits / 航站代码必须为四位')
        error = True
    print('checking for ' + stationx)
    print('正在查询' + stationx + '航站')
    kv = {'data?ids': 'KIWA'}
    r = requests.get("https://www.aviationweather.gov/metar/data?ids=" + stationx +
                     "&format=decoded&date=&hours=0&taf=on", params=kv)
    print('数据从NOAA获得''\ndata retrived from:NOAA\n')
    # web spider from aviationweather.gov

    url = ("https://www.aviationweather.gov/metar/data?ids=" + stationx + "&format=decoded&date=&hours=0&taf=on")
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html = BeautifulSoup(response.text, 'html.parser')

    source_decode_metar = html.select('#awc_main_content_wrap > table:nth-child(3)')

    source_decode_taf = html.select('#awc_main_content_wrap > table:nth-child(5)')

    print(source_decode_metar[0].get_text())
    print("\n↑↑↑↑↑↑↑↑↑↑METAR↑↑↑↑↑↑↑↑↑↑\n\n↓↓↓↓↓↓↓↓↓↓↓TAF↓↓↓↓↓↓↓↓↓↓↓\n")
    print(source_decode_taf[0].get_text())

    return source_decode_metar, source_decode_taf


def main():
    decode_metar = decode_taf = raw_metar = raw_taf = 'No data'
    times = time.time()
    # 获取时间戳
    ztime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(times))
    # 将时间戳转换为格林威治时间（Zulu/UTC 时间）
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(times))
    # 将时间戳转换为本地时间
    zgreet = '当前UTC时间为/Current UTC time is '
    localgreet = '当前本地时间为/Current local time is '
    print(zgreet + ztime + 'Z')
    # Z在航空用于区分本地时间和世界协调时（UTC/Zulu时间）
    print(localgreet, localtime)
    print("\n\nwelcome,欢迎\n\n")
    is_raw = True

    while True:
        
        # 如需解码则使用另外的爬虫网址
        # if decoded is needed then the format needs to be changed to raw
        alpha = yn
        # 不解码
        if 'y' != alpha:
            source_raw_metar, source_raw_taf = raw_data()

            # save raw data
            raw_metar = {source_raw_metar[0].get_text()}
            with open('rawdata_metar.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for keys in list(raw_metar):
                    for key in keys.split('\n'):
                        if key:
                            writer.writerow([key])
            raw_taf = {source_raw_taf[0].get_text()}
            with open('rawdata_taf.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for keys in list(raw_taf):
                    for key in keys.split('\n'):
                        if key:
                            writer.writerow([key])

        # 解码
        else:
            is_raw = False
            source_decode_metar, source_decode_taf = decode_data()

            # save decoded data
            decode_metar = {source_decode_metar[0].get_text()}
            with open('decodedata_metar.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for keys in list(decode_metar):
                    for key in keys.split('\n'):
                        if key:
                            writer.writerow([key])
            decode_taf = {source_decode_taf[0].get_text()}
            with open('decodedata_taf.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for keys in list(decode_taf):
                    for key in keys.split('\n'):
                        if key:
                            writer.writerow([key])

        # 打印
        # print raw data
        if is_raw:
            rawdata_1 = genfromtxt('rawdata_metar.csv', dtype=str, delimiter='@')
            rawdata_2 = genfromtxt('rawdata_taf.csv', dtype=str, delimiter='@')
            rawdata = np.array([rawdata_1, rawdata_2], dtype=str)
            rawdata = np.insert(rawdata, 0, 'Current UTC time is: ' + ztime)
            rawdata = np.insert(rawdata, 0, 'Current local time is: ' + localtime)
            convert_img(rawdata, 1, is_raw)
        # print decoded data
        if not is_raw:
            metar = genfromtxt('decodedata_metar.csv', dtype=str, delimiter='@')
            taf = genfromtxt('decodedata_taf.csv', dtype=str, delimiter='@')
            metar = np.insert(metar, 0, 'Current UTC time is: ' + ztime)
            metar = np.insert(metar, 0, 'Current local time is: ' + localtime)
            convert_img(metar, 1, is_raw)
            # 打印taf
            user_check = tafyn
            if user_check.lower() == 'y' or user_check.lower() == 'yes':
                count = 0
                taf_cut = np.array([])
                for row in range(taf.shape[0]):
                    temp = taf[row]
                    if 'Text' in temp:  # only print the first Taf
                        count = count + 1
                    if count >= 2:
                        break
                    taf_cut = np.append(taf_cut, temp)
                convert_img(taf_cut, 2, is_raw)
        break    
            


if __name__ == '__main__':
    main()

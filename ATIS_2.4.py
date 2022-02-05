#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import time
from bs4 import BeautifulSoup
import requests
import numpy as np
from numpy import genfromtxt
from PIL import Image, ImageDraw, ImageFont

print('⠄⠄⠄⠄⠄⠄⢠⣿⣋⣿⣿⣉⣿⣿⣯⣧⡰⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⣿⣿⣹⣿⣿⣏⣿⣿⡗⣿⣿⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⠟⡛⣉⣭⣭⣭⠌⠛⡻⢿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⠄⠄⣤⡌⣿⣷⣯⣭⣿⡆⣈⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿⣿⣿⣿⣿⣷⢛⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⠄⠄⢻⣷⣽⣿⣿⣿⢿⠃⣼⣧⣀⠄⠄⠄⠄⠄⠄⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣛⣻⣿⠟⣀⡜⣻⢿⣿⣿⣶⣤⡀⠄⠄⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⠄⠄⢠⣤⣀⣨⣥⣾⢟⣧⣿⠸⣿⣿⣿⣿⣿⣤⡀⠄⠄⠄')
print('⠄⠄⠄⠄⠄⠄⠄⠄⢟⣫⣯⡻⣋⣵⣟⡼⣛⠴⣫⣭⣽⣿⣷⣭⡻⣦⡀⠄')
print('⠄⠄⠄⠄⠄⠄⠄⢰⣿⣿⣿⢏⣽⣿⢋⣾⡟⢺⣿⣿⣿⣿⣿⣿⣷⢹⣷⠄')
print('⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⢣⣿⣿⣿⢸⣿⡇⣾⣿⠏⠉⣿⣿⣿⡇⣿⣿⡆')
print('⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⢸⣿⣿⣿⠸⣿⡇⣿⣿⡆⣼⣿⣿⣿⡇⣿⣿⡇')
print('⠇⢀⠄⠄⠄⠄⠄⠘⣿⣿⡘⣿⣿⣷⢀⣿⣷⣿⣿⡿⠿⢿⣿⣿⡇⣩⣿⡇')
print('⣿⣿⠃⠄⠄⠄⠄⠄⠄⢻⣷⠙⠛⠋⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⡇⣿⣿⡇')

# Copyrights©Shepard Deng VATSIM ID 1434656, not for commercial use, For
# fight simulation only, do not use for actual flight

print("Copyrights©Shepard Deng VATSIM ID 1434656 and Hunter Wang, not for commercial use, \n"
      "For fight simulation only, do not use for actual flight\n")


def convert_img(data, count):
    # find the length of text
    length = []
    for index in range(data.shape[0]):
        length.append(len(data[index]))
    max_length = max(length)
    # print(max_length)

    # creat image
    if max_length > 100:
        img = Image.new('RGB', (max_length * 13, data.shape[0] * 30), color=(255, 255, 255))
    else:
        img = Image.new('RGB', (max_length * 14, data.shape[0] * 30), color=(255, 255, 255))
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

while True:
    print('decoded? 是否解码? (Y/N)')
    # 如需解码则使用另外的爬虫网址
    # if decoded is needed then the format needs to be changed to raw
    alpha = input("请输入是否解码? (Y/N)：")
    if ('y' != alpha):
        # 使用 ZUUU KIWA KLAX KPHX 作为测试航站
        # Use    ZUUU KIWA KLAX KPHX for testing
        print('输入查询的航站,type in the station you want to check')
        stationx = input("请输入输入查询的航站：")
        print('checking for ' + stationx)
        print('正在查询' + stationx + '航站')
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

        with open('rawdata.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for raw in str(source_raw_metar[0].get_text()).split('\n'):
                writer.writerow([raw])

    else:
        print('使用 ZUUU WSSS KIWA KLAX KJFK作为测试航站')
        # 使用   ZUUU KIWA KLAX KPHX 作为测试航站
        # Use    ZUUU KIWA KLAX KPHX for testing
        print('输入查询的航站,type in the station you want to check')
        stationx = input("请输入输入查询的航站：")
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

        # 此处也需要实现和86行一样的功能
        result_decode = {source_decode_metar[0].get_text()}
        with open('decodedata_metar.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for keys in list(result_decode):
                for key in keys.split('\n'):
                    if key:
                        writer.writerow([key])
        # print("result", result_decode)

        result_decode = {source_decode_taf[0].get_text()}
        with open('decodedata_taf.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for keys in list(result_decode):
                for key in keys.split('\n'):
                    if key:
                        writer.writerow([key])

    metar = genfromtxt('decodedata_metar.csv', dtype=str, delimiter='@')
    taf = genfromtxt('decodedata_taf.csv', dtype=str, delimiter='@')
    metar = np.insert(metar, 0, 'Current UTC time is: ' + ztime)
    metar = np.insert(metar, 0, 'Current local time is: ' + localtime)

    user_check = input('\ndo you want to print the data?\n \n是否要打印？\n (Y /N)')
    if user_check.lower() == 'y' or user_check.lower() == 'yes':
        convert_img(metar, 1)

        user_check = input('\ndo you want to print taf?\n \n是否要打印taf？\n (Y /N)')
        if user_check.lower() == 'y' or user_check.lower() == 'yes':
            if taf.shape[0] > 12:
                count = 0
                taf_cut = np.array([])
                for row in range(taf.shape[0]):
                    temp = taf[row]
                    if 'Text' in temp:
                        count = count + 1
                    if count >= 2:
                        break
                    taf_cut = np.append(taf_cut, temp)
                convert_img(taf_cut, 2)
            else:
                convert_img(taf, 2)

    user_check = input('\ndo you want to continue checking?\n \n继续查询？\n (Y /N)')
    if user_check.lower() == 'n' or user_check.lower() == 'no':
        print('have a good day')
        break

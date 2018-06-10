#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image, ImageDraw, ImageFont
import logging
import time

#______________________________________________________________________________________________________________________

def find_kab(map, val):
    #is_find=False
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == val:
                return [i, j]
    #return is_find
def find_way(step, arr, kab):
    curr_cell = find_kab(arr, kab)
    path = [curr_cell]
    steps = step
    for i in range(steps):
        is_find = False
        if arr[curr_cell[0] - 1][curr_cell[1]] == (step) and is_find != True:
            curr_cell = [curr_cell[0] - 1, curr_cell[1]]
            path.append(curr_cell)
            is_find = True
            step = step - 1
        if arr[curr_cell[0]][curr_cell[1] + 1] == (step) and is_find != True:
            curr_cell = [curr_cell[0], curr_cell[1] + 1]
            path.append(curr_cell)
            is_find = True
            step = step - 1
        if arr[curr_cell[0] + 1][curr_cell[1]] == (step) and is_find != True:
            curr_cell = [curr_cell[0] + 1, curr_cell[1]]
            path.append(curr_cell)
            is_find = True
            step = step - 1
        if arr[curr_cell[0]][curr_cell[1] - 1] == (step) and is_find != True:
            curr_cell = [curr_cell[0], curr_cell[1] - 1]
            path.append(curr_cell)
            is_find = True
            step = step - 1
        if arr[curr_cell[0] - 1][curr_cell[1] - 1] == (step) and is_find != True:
            curr_cell = [curr_cell[0] - 1, curr_cell[1] - 1]
            path.append(curr_cell)
            is_find = True
            step = step - 1
        if arr[curr_cell[0] + 1][curr_cell[1] - 1] == (step) and is_find != True:
            curr_cell = [curr_cell[0] + 1, curr_cell[1] - 1]
            path.append(curr_cell)
            is_find = True
            step = step - 1
        if arr[curr_cell[0] + 1][curr_cell[1] + 1] == (step) and is_find != True:
            curr_cell = [curr_cell[0] + 1, curr_cell[1] + 1]
            path.append(curr_cell)
            is_find = True
            step = step - 1
        if arr[curr_cell[0] - 1][curr_cell[1] + 1] == (step) and is_find != True:
            curr_cell = [curr_cell[0] - 1, curr_cell[1] + 1]
            path.append(curr_cell)
            is_find = True
            step = step - 1
    return path

def draw_path(path, size, width, height, floor_img):
    # im = Image.new('RGBA', (size[1] * 10, size[0] * 10), (255, 255, 255, 255))
    im = Image.open(floor_img)
    draw = ImageDraw.Draw(im)
    for i in range(1, len(path)):
        draw.line(((path[i - 1][1] + 1) * width - width/2, (path[i - 1][0] + 1) * height - height/2, (path[i][1] + 1) * width - width/2, (path[i][0] + 1) * height - height/2), fill=(0,0,0,255), width = 30)
    im.show()
    im.save("pass.png")
    time.sleep(3)
    return True

def find_ways(kab1,kab2):
    maps = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, 'K276', 0, 'K279', -1, -1, -1],
        [-1, -1, 'K219', 'K218', 'K221', 'K222', 'K223', 'K224', 'K225', 'K226', 'K228', 0, -1, 0, 'K233', 'K234',
         'K235', 'K236', 'K237', 'K238', 'K239', 'K240', 'K241', 'K242', 'K243', 'K244', 'K247', 'K246', 'K245', 0, -1,
         0, 'K280', -1, -1],
        [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1],
        [-1, -1, -1, -1, -1, 'K217', 'K216', -1, -1, 'K213', 'K211', 0, -1, 0, 'K254', -1, 'K253', -1, -1, 'K252',
         'K251', 'K250', 'K249', -1, 'K248', -1, -1, -1, 'K267', -1, -1, 'K281', -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 'K1', 0, -1, 0, 'K2', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 'K202D', 0, 0, 0, -1, 'K204D', 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 'K208D', 0, -1, 'K210D', 0, 'K212D', 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 'K214D', 0, 'K215D', 'K216D', 0, 'K213D', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1]]
    begin='K'+kab1
    point = find_kab(maps,begin)
    maps[point[0]][point[1]] = 1
    end='K'+kab2
    point = find_kab(maps, end)
    maps[point[0]][point[1]] = 'A'
    k = 2
    step = 0
    end = False
    for g in range(200):
        for i in range(1, len(maps) - 2):
            for j in range(1, len(maps[i]) - 2):
                if maps[i - 1][j - 1] == (k - 1) or maps[i - 1][j] == (k - 1) or maps[i - 1][j + 1] == (k - 1) or \
                        maps[i][j + 1] == (k - 1) or maps[i + 1][j + 1] == (k - 1) or maps[i + 1][j] == (k - 1) or \
                        maps[i + 1][j - 1] == (k - 1) or maps[i][j - 1] == (k - 1):
                    if maps[i][j] == 0:
                        maps[i][j] = k
                        if maps[i - 1][j - 1] == 'A' or maps[i - 1][j] == 'A' or maps[i - 1][j + 1] == 'A' or maps[i][j + 1] == 'A' or maps[i + 1][j + 1] == 'A' or maps[i + 1][j] == 'A' or maps[i + 1][j - 1] == 'A' or maps[i][j - 1] == 'A':
                            end = True
                # if maps[i][j] == 'A':
                #     if maps[i - 1][j - 1] != 0 or maps[i - 1][j] != 0 or maps[i - 1][j + 1] != 0 or maps[i][
                #         j + 1] != 0 or maps[i + 1][j + 1] != 0 or maps[i + 1][j] != 0 or maps[i + 1][j - 1] != 0 or \
                #             maps[i][j - 1] != 0:
                #         end = True
        if end:
            step = k
            break
        k = k + 1
    path = find_way(step, maps, 'A')
    draw_path(path, [30, 35], 100, 75, 'floor1.png')
def find_ways3(kab1,kab2):
    maps = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, 'K372', 0, 'K368', -1, -1, -1],
        [-1, -1, 'K312', 'K311', 'K314', 'K316', 'K317', 'K318', 'K319', 'K320', 'K321', 'K322', 'K324', 'K325', 0,
         'K327', 0, 'K329', 'K330', 'K331', 'K333', 'K334', 'K335', 'K336', 'K337', 'K338', 'K339', 'K342', 'K343', 0,
         -1, 0, 'K366', -1, -1],
        [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1],
        [-1, -1, -1, -1, 'K310', 'K309', -1, -1, 'K306', 'K304', -1, -1, -1, 'K1', 0, -1, 0, 'K2', -1, 'K353', 'K351',
         'K350', -1, -1, 'K346', 'K345', -1, -1, -1, -1, -1, 'K364', -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1]]
    begin='K'+kab1
    point = find_kab(maps,begin)
    maps[point[0]][point[1]] = 1
    end='K'+kab2
    point = find_kab(maps, end)
    maps[point[0]][point[1]] = 'A'
    k = 2
    step = 0
    end = False
    for g in range(200):
        for i in range(1, len(maps) - 2):
            for j in range(1, len(maps[i]) - 2):
                if maps[i - 1][j - 1] == (k - 1) or maps[i - 1][j] == (k - 1) or maps[i - 1][j + 1] == (k - 1) or \
                        maps[i][j + 1] == (k - 1) or maps[i + 1][j + 1] == (k - 1) or maps[i + 1][j] == (k - 1) or \
                        maps[i + 1][j - 1] == (k - 1) or maps[i][j - 1] == (k - 1):
                    if maps[i][j] == 0:
                        maps[i][j] = k
                        if maps[i - 1][j - 1] == 'A' or maps[i - 1][j] == 'A' or maps[i - 1][j + 1] == 'A' or maps[i][j + 1] == 'A' or maps[i + 1][j + 1] == 'A' or maps[i + 1][j] == 'A' or maps[i + 1][j - 1] == 'A' or maps[i][j - 1] == 'A':
                            end = True
                # if maps[i][j] == 'A':
                #     if maps[i - 1][j - 1] != 0 or maps[i - 1][j] != 0 or maps[i - 1][j + 1] != 0 or maps[i][
                #         j + 1] != 0 or maps[i + 1][j + 1] != 0 or maps[i + 1][j] != 0 or maps[i + 1][j - 1] != 0 or \
                #             maps[i][j - 1] != 0:
                #         end = True
        if end:
            step = k
            break
        k = k + 1
    path = find_way(step, maps, 'A')
    draw_path(path, [8, 34], 100, 75, 'floor2.png')
def find_ways4(kab1,kab2):
    # maps = [
    #     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    #      -1, -1, -1, -1, -1, -1, -1],
    #     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    #      -1, -1, -1, -1, -1, -1, -1],
    #     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    #      -1, 'K471', 0, 'K496', -1, -1, -1, -1],
    #     [-1, -1, -1, 'K415' 'K414', 'K416', 'K417', 'K419', 'K420', 'K3421', 'K422', 'K423', 'K424', 'K425', 'K426', 0,
    #      0, 0, 'K431', 'K430', 'K431', 'K432', 'K433', 'K434', 'K435', 'K437', 'K438', 'K439', 'K440', 'K441', 0, -1, 0,
    #      'K468', -1, -1],
    #     [-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1,
    #      -1],
    #     [-1, -1, -1, -1, 'K413', 'K412', -1, -1, 'K409', 'K408', 'K407', -1, 'K405', 'L4', 0, 'K427', 0, 'R3', -1,
    #      'K455', 'K454', 'K453', 'K452', 'K450', 'K449', 'K448', 'K447', -1, -1, -1, -1, 'K464', -1, -1, -1, -1],
    #     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    #      -1, -1, -1, -1, -1, -1, -1],
    #     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    #      -1, -1, -1, -1, -1, -1, -1]]
    maps = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, 'K471', 0, 'K496', -1, -1, -1],
        [-1, -1, 'K415', 'K414', 'K416', 'K417', 'K418', 'K419', 'K420', 'K421', 'K422', 'K423', 'K424', 'K425', 0,
         0, 0, 'K431', 'K430', 'K432', 'K433', 'K434', 'K435', 'K437', 'K438', 'K439', 'K440', 'K441', -1, 0,
         -1, 0, 'K468', -1, -1],
        [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'K427', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1],
        [-1, -1, -1, -1, 'K413', 'K412', -1, -1, 'K409', 'K408', 'K407', 'K406', -1, 'K1', 0, -1, 0, 'K2', -1, 'K455', 'K454',
         'K453', -1, -1, 'K448', 'K447', -1, -1, -1, -1, -1, 'K464', -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1]]
    begin='K'+kab1
    point = find_kab(maps,begin)

    maps[point[0]][point[1]] = 1
    end='K'+kab2
    point = find_kab(maps, end)
    maps[point[0]][point[1]] = 'A'
    k = 2
    step = 0
    end = False
    for g in range(200):
        for i in range(1, len(maps) - 2):
            for j in range(1, len(maps[i]) - 2):
                if maps[i - 1][j - 1] == (k - 1) or maps[i - 1][j] == (k - 1) or maps[i - 1][j + 1] == (k - 1) or \
                        maps[i][j + 1] == (k - 1) or maps[i + 1][j + 1] == (k - 1) or maps[i + 1][j] == (k - 1) or \
                        maps[i + 1][j - 1] == (k - 1) or maps[i][j - 1] == (k - 1):
                    if maps[i][j] == 0:
                        maps[i][j] = k
                        if maps[i - 1][j - 1] == 'A' or maps[i - 1][j] == 'A' or maps[i - 1][j + 1] == 'A' or maps[i][j + 1] == 'A' or maps[i + 1][j + 1] == 'A' or maps[i + 1][j] == 'A' or maps[i + 1][j - 1] == 'A' or maps[i][j - 1] == 'A':
                            end = True
                # if maps[i][j] == 'A':
                #     if maps[i - 1][j - 1] != 0 or maps[i - 1][j] != 0 or maps[i - 1][j + 1] != 0 or maps[i][
                #         j + 1] != 0 or maps[i + 1][j + 1] != 0 or maps[i + 1][j] != 0 or maps[i + 1][j - 1] != 0 or \
                #             maps[i][j - 1] != 0:
                #         end = True
        if end:
            step = k
            break
        k = k + 1
    path = find_way(step, maps, 'A')
    draw_path(path, [8, 34], 100, 75, 'floor3.png')


#______________________________________________________________________________________________________________________


# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
def help(bot, update):
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open('pass.png', 'rb'))
#def help(bot, update):
    #"""Send a message when the command /help is issued."""
    #update.message.reply_text('Type /go <start of path> <end of path>')
    #chat_id = update.message.chat_id
    #print(chat_id)
    #bot.send_photo(chat_id=chat_id, photo='pass.png')

def go(bot, update,args):
    if args[0] == args[1]:
        update.message.reply_text('you inputed the same')
    elif len(args) == 2:
        if args[0][0] == args[1][0]:
            if args[0][0] == '2':
                print('2')
                find_ways(args[0], args[1])
                time.sleep(3)
            if args[0][0] == '3':
                find_ways3(args[0], args[1])
                time.sleep(3)
            if args[0][0] == '4':
                find_ways4(args[0], args[1])
                time.sleep(3)
            chat_id = update.message.chat_id
            bot.send_photo(chat_id=chat_id, photo=open('pass.png', 'rb'))
        else:
            lest = ''
            if args[0][0] == '2':
                if int(args[0][1]) < 3:
                    lest = '1'
                    find_ways(args[0], lest)
                    time.sleep(3)
                else:
                    lest = '2'
                    find_ways(args[0], lest)
                    time.sleep(3)
                time.sleep(3)

            if args[0][0] == '3':
                if int(args[0][1]) < 3:
                    lest = '1'
                    find_ways3(args[0], lest)
                    time.sleep(3)
                else:
                    lest = '2'
                    find_ways3(args[0], lest)
                    time.sleep(3)
                time.sleep(3)

            if args[0][0] == '4':
                if int(args[0][1]) < 3:
                    lest = '1'
                    find_ways4(args[0], lest)
                    time.sleep(3)
                else:
                    lest = '2'
                    find_ways4(args[0], lest)
                    time.sleep(3)
                time.sleep(3)

            chat_id = update.message.chat_id
            bot.send_photo(chat_id=chat_id, photo=open('pass.png', 'rb'))

            if args[1][0] == '2':
                find_ways(lest, args[1])
                time.sleep(3)

            if args[1][0] == '3':
                find_ways3(lest, args[1])
                time.sleep(3)

            if args[1][0] == '4':
                find_ways4(lest, args[1])
                time.sleep(3)

            chat_id = update.message.chat_id
            bot.send_photo(chat_id=chat_id, photo=open('pass.png', 'rb'))
    else:
        update.message.reply_text('Usage: /go <start of path> <end of path>')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("540177651:AAEYGBtWOMz56m0TS_trFSG7k5RiZK_YO6g")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("go", go, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
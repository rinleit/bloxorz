#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Map"""
import simplejson as json
from model.sw import swO, swQ, swX
from model.box import Box
from model.bridge import Bridge
from model.tiles import tile
class goal:
    def __init__(self, symbol, location):
        self.symbol = symbol
        self.location = location
        
class maps:
    def __init__(self, path_to_level=None):
        self.files = None
        self.jsonObj = None
        self.maps = list()
        self.level = None
        self.size = None
        self.start = None
        self.end = None 
        self.current_box = None
        self.types_tile = None
        self.swQ = list()
        self.swX = list()
        self.swO = list()
        self.Brid = list()
        if path_to_level != None:
            self.loadLevel(path_to_level)

    def loadLevel(self, path_to_level=None):
        if path_to_level != None:
            self.files = open(path_to_level, "r")
            self.jsonObj = json.loads(self.files.read())

            # Name Level
            self.level = self.jsonObj["level"]
            # Size Map
            self.size = self.jsonObj["size"]
            # Start Location
            self.start = self.jsonObj["start"]
            # End Location
            self.end = self.jsonObj["end"]
            # Types of tiles
            self.types_tile = [self.jsonObj["tiles"]["orange"], self.jsonObj["tiles"]["rock"], self.jsonObj["tiles"]["space"]]
            # Current Box
            boxObj = self.jsonObj["box"]
            self.current_box = Box(boxObj["symbol"], boxObj["state"], boxObj["location"])
            # Load swX
            self.__loadSWX()
            # Load swQ
            self.__loadSWQ()
            # Load swO
            self.__loadSWO()
            # Load Maps
            self.__loadMap()
            # Update Maps
            self.__updateMaps("all")

        else: print("Path_to_level not None")
    
    def __loadMap(self):
        # Load tiles to Maps
        maps = self.jsonObj["maps"]
        for i in range(self.size[0]):
            line = []
            for j in range(self.size[1]):
                if maps[i][j] == self.types_tile[0]: # orange tile
                    newtile = tile(2, None, [i, j])
                    line.append(newtile)
                elif maps[i][j] == self.types_tile[1]: # rock tile
                    newtile = tile(1, None, [i, j])
                    line.append(newtile)
                elif maps[i][j] == self.types_tile[2]: # space title
                    newtile = tile(0, None, [i, j])
                    if self.end == [i, j]:
                        newtile.set_obj(goal("$", [i, j])) # End game
                    line.append(newtile)
                else:
                    newtile = tile(1, None, [i, j])
                    line.append(newtile)
            self.maps.append(line)
        # Load Start Box to Maps
        self.maps[int(self.start[0])][int(self.start[1])].set_box(self.current_box)

    def __updateMaps(self, key=None):
        # Load swO to Maps
        if len(self.swO) != 0 and key=="all":
            for one in self.swO:
                self.maps[int(one.location[0])][int(one.location[1])].set_obj(one)
        # Load swQ to Maps
        if len(self.swQ) != 0 and key=="all":
            for one in self.swQ:
                self.maps[int(one.location[0])][int(one.location[1])].set_obj(one)
        # Load swX to Maps
        if len(self.swX) != 0 and key=="all":
            for one in self.swX:
                self.maps[int(one.location[0])][int(one.location[1])].set_obj(one)

        if len(self.Brid) != 0:
            for one in self.Brid:
                if one.type == 1: # One tile
                    if one.active is True:
                        self.maps[int(one.location[0][0])][int(one.location[0][1])].type = 1
                    else: 
                        self.maps[int(one.location[0][0])][int(one.location[0][1])].type = 0
                    self.maps[int(one.location[0][0])][int(one.location[0][1])].set_obj(one)
                elif one.type == 2: # Two tile
                    if one.active is True:
                        self.maps[int(one.location[0][0])][int(one.location[0][1])].type = 1
                    else: 
                        self.maps[int(one.location[0][0])][int(one.location[0][1])].type = 0
                    self.maps[int(one.location[0][0])][int(one.location[0][1])].set_obj(one)
 
                    if one.active is True:
                        self.maps[int(one.location[1][0])][int(one.location[1][1])].type = 1
                    else: 
                        self.maps[int(one.location[1][0])][int(one.location[1][1])].type = 0
                    self.maps[int(one.location[1][0])][int(one.location[1][1])].set_obj(one)
        
        # Loads current box to Maps
        if key==3 or key=="all":
            curr_location = self.current_box.location
            stateBox = len(curr_location)
            if stateBox == 1: 
                self.maps[int(curr_location[0][0])][int(curr_location[0][1])].set_box(self.current_box)
            elif stateBox == 2: 
                self.maps[int(curr_location[0][0])][int(curr_location[0][1])].set_box(self.current_box)
                self.maps[int(curr_location[1][0])][int(curr_location[1][1])].set_box(self.current_box)

    def updateSWX(self, swXObj):
        for one in self.swX:
            if one.symbol == swXObj.symbol:
                self.swX[self.swX.index(one)].active = swXObj.active
                self.__updateBrid(swXObj.bridge)
                self.__updateMaps()
    
    def updateSWQ(self, swQObj):
        for one in self.swQ:
            if one.symbol == swQObj.symbol:
                self.swQ[self.swQ.index(one)].active = swQObj.active
                self.__updateBrid(swQObj.bridge)
                self.__updateMaps()
    
    def updateSWO(self, swOObj):
        for one in self.swO:
            if one.symbol == swOObj.symbol:
                self.swO[self.swO.index(one)] = swOObj
                self.__updateMaps()
    
    def refreshBox(self):
        self.__cleanOldBox()
        try:
            if self.__check_life(self.current_box) == False:
                return False
            self.__updateMaps(key=3)
        except:
            return False
        return True

    def check_goal(self):
        return self.current_box.is_standing() and self.current_box.is_doubleBox() and self.end == self.current_box.location[0]
     
    def __check_life(self, box):
        if len(box.location) == 1:
            y1 = box.location[0][0]
            x1 = box.location[0][1]
            return self.maps[y1][x1].check_life(box)
        elif len(box.location) == 2:
            for child in box.location:
                y1 = child[0]
                x1 = child[1]
                res = self.maps[y1][x1].check_life(box)
                if res == False: return False
            return True

    def __cleanOldBox(self):
        oldBox = self.current_box.pre_location
        stateBox = len(oldBox)
        if stateBox == 1: 
            self.maps[int(oldBox[0][0])][int(oldBox[0][1])].set_box(None)
        elif stateBox == 2:
            self.maps[int(oldBox[0][0])][int(oldBox[0][1])].set_box(None)
            self.maps[int(oldBox[1][0])][int(oldBox[1][1])].set_box(None)
        
    def __updateBrid(self, bridObj):
        for one in self.Brid:
            if one.symbol == bridObj.symbol:
                self.Brid[self.Brid.index(one)].active = bridObj.active

    def __loadSWX(self):
        swXObj = self.jsonObj["swX"]
        count = int(swXObj["count"])
        if count > 0:
            symbol = swXObj["symbol"]
            for sym in symbol:
                symObj = swXObj[sym]
                newswX = swX(sym, symObj["type"], symObj["active"], symObj["location"])
                bridObj = self.jsonObj["bridge"]
                nameBrid = symObj["bridge"]
                if int(bridObj["count"]) > 0:
                    chidBrid = bridObj[nameBrid]
                    newBrid = Bridge(nameBrid, chidBrid["active"], chidBrid["location"])
                    newswX.set_bridge(newBrid)
                    self.Brid.append(newBrid)
                self.swX.append(newswX)

    def __loadSWQ(self):
        swQObj = self.jsonObj["swQ"]
        count = int(swQObj["count"])
        if count > 0:
            symbol = swQObj["symbol"]
            for sym in symbol:
                symObj = swQObj[sym]
                newswQ = swQ(sym, symObj["type"], symObj["active"], symObj["location"])
                bridObj = self.jsonObj["bridge"]
                nameBrid = symObj["bridge"]
                if int(bridObj["count"]) > 0:
                    chidBrid = bridObj[nameBrid]
                    newBrid = Bridge(nameBrid, chidBrid["active"], chidBrid["location"])
                    newswQ.set_bridge(newBrid)
                    self.Brid.append(newBrid)
                self.swQ.append(newswQ)
    
    def __loadSWO(self):
        swOObj = self.jsonObj["swO"]
        count = int(swOObj["count"])
        if count > 0:
            symbol = swOObj["symbol"]
            for sym in symbol:
                symObj = swOObj[sym]
                newswO = swO(sym, symObj["location"], symObj["split"])
                box1 = symObj["box1"]
                box2 = symObj["box2"]
                newswO.set_box1(box1["symbol"], box1["state"], box1["location"])
                newswO.set_box2(box2["symbol"], box2["state"], box2["location"])
                self.swO.append(newswO)

    def print_current(self):
        for i in self.maps:
            print("------" * self.size[1])
            print('{0: <3}'.format("|"), end='')
            for j in i:
                if j.type == 0:
                    content = " "
                    if j.obj != None and j.box != None:
                        content = j.box.symbol
                    elif j.obj != None and j.box == None:
                        if j.obj.symbol == "$":
                            content = "$"
                elif j.type == 1 or j.type == 2:
                    if j.obj != None and j.box != None:
                        content = j.box.symbol
                    elif j.obj != None and j.box == None: 
                        content = j.obj.symbol
                    elif j.obj == None and j.box != None:
                        content = j.box.symbol
                    else: content = j.type
                print('{0: <2}'.format(content),"|", end='')
                print('{0: <2}'.format(""), end='')
            print("\n",end='')
        print("------" * self.size[1])


    
#!/usr/bin/python3
# -*- coding: utf-8 -*-
from model.box import Box
"""Tiles"""
colors = {
		'gray'	:(	 0.56862745, 0.56862745, 0.56862745, 1),
        'orange':(   0.96470588, 0.34509804, 0.05882352, 1), 
        'green' :(   0.50196078, 0.91372549, 0.09019607, 1),
        'white' :(   0.8       ,        0.8,        0.8, 1),
        'blue'  :(   0.07450980,  0.6627450, 0.89803921, 1),  #SWX
        'pink'  :(   0.49803921, 0.07450980, 0.19607843, 1),  #SWQ
        'red'   :(   0.93333333, 0.07843137, 0.11372549, 1),   #SWO
        'yellow' :   ( 1.0, 0.792156862745098, 0.0941176470588235, 0.3)
	}

class tile:
    
    def __init__(self, typ, obj, location):
        self.type = typ
        self.obj = obj
        self.location = location
        self.colors = colors['white']

        if self.type == 1:
            self.colors = colors['gray']
        elif self.type == 2:
            self.colors = colors['orange']
        
                    
    def check_material_tile(self, box):
        for child in box.location:
            if child == self.location:
                # Space
                if self.type == 0:
                    if self.obj != None:
                        if self.obj.symbol == "$":
                            return True
                        else: return False
                    else: return False
                # Orange
                elif self.type == 2:
                    if not box.is_standing():
                        return True
                    else: return False
                # Rock
                elif self.type == 1: 
                    return True

    def get_location(self):
        return self.location
    
    def set_obj(self, obj):
        self.obj = obj
        if self.obj != None:
            if 'x' in str(self.obj.symbol):
                self.colors = colors['blue']
            elif 'q' in str(self.obj.symbol):
                self.colors = colors['pink']
            elif 'o' in str(self.obj.symbol):
                self.colors = colors['red']
            elif 'c' in str(self.obj.symbol):
                self.colors = colors['green']
            elif '$' in str(self.obj.symbol):
                self.colors = colors['yellow']
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time

class Control:
    Play_handle = False
    def __init__(self, maps=None):
        if maps is None:
            print("Maps not None")
            sys.exit()

        self.start = maps.current_box.location
        self.current = maps.current_box.location
        self.pre = maps.current_box.location
        self.maps = maps

        if not self.check_box_on_maps():
            print("Start Box Error")
            sys.exit()
        
        self.stack = [self.start]
        self.visted = [self.start]
        
        self.moves = (self.move_right, self.move_down, self.move_up, self.move_left)

    def move_up(self):
        self.pre = self.current
        self.maps.current_box.move_up()
        if not self.check_box_on_maps():
            self.set_state(self.pre)
            return False
        else:
            if not self.Play_handle:
                self.__update_current_locaton()
                return self.add_stack()
            return True 
    
    def move_down(self):
        self.pre = self.current
        self.maps.current_box.move_down()
        if not self.check_box_on_maps():
            self.set_state(self.pre)
            return False
        else:
            if not self.Play_handle:
                self.__update_current_locaton()
                return self.add_stack()
            return True 
    
    def __update_current_locaton(self):
        self.current = self.maps.current_box.location
    
    def move_right(self):
        self.pre = self.current
        self.maps.current_box.move_right()
        if not self.check_box_on_maps():
            self.set_state(self.pre)
            return False
        else:
            if not self.Play_handle:
                self.__update_current_locaton()
                return self.add_stack()
            return True 
    
    def move_left(self):
        self.pre = self.current
        self.maps.current_box.move_left()
        if not self.check_box_on_maps():
            self.set_state(self.pre)
            return False
        else:
            if not self.Play_handle:
                self.__update_current_locaton()
                return self.add_stack()
            return True 

    def check_box_on_maps(self):
        return self.maps.refreshBox()
    
    def set_state(self, location):
        self.current = location
        self.maps.current_box.location = location
    
    def get_box(self):
        return self.current
    
    def add_stack(self):
        state = self.current
        if state not in self.visted:
            self.visted.append(state)
            self.stack.append(state)
            return True
        return False
    
    def check_goal(self):
        return self.maps.check_goal()

    def print_maps(self):
        self.maps.print_current()
        
def dfs(state: Control):
    while state.stack:
        current_state = state.stack.pop()
        for move in state.moves:
            state.set_state(current_state)
            # state.maps.print_current()
            # time.sleep(0.3)
            # os.system("clear")
            if move():
                # state.maps.print_current()
                if state.check_goal():
                    return
            # os.system("clear")

def dfs_recursion(state: Control):
    if state.check_goal():
        # state.maps.print_current()
        return
    current_state = state.stack.pop()
    for move in state.moves:
        state.set_state(current_state)
        if move():
            dfs_recursion(state)

def bfs(state: Control):
    while state.stack:
        current_state = state.stack.pop(0)
        for move in state.moves:
            state.set_state(current_state)
            # state.maps.print_current()
            # time.sleep(0.3)
            # os.system("cls")
            if move():
                # state.maps.print_current()
                if state.check_goal():
                    return
            # os.system("cls")

def dfs_path(state: Control):
    stack = [[state.current], ]
    while state.stack:
        current_state = state.stack.pop()
        path = stack.pop()
        for move in state.moves:
            state.set_state(current_state)
            if move():
                if state.check_goal():
                    result = path + [state.current]
                    return result
                stack.append(path + [state.current])

def bfs_path(state: Control):
    stack = [[state.current], ]
    while state.stack:
        current_state = state.stack.pop(0)
        path = stack.pop(0)
        for move in state.moves:
            state.set_state(current_state)
            if move():
                if state.check_goal():
                    result = path + [state.current]
                    return result
                stack.append(path + [state.current])
    
def hill_climbing(state: Control):
    pass

def handle(state: Control):
    state.Play_handle = True
    res = True
    while 1:
        number = input("Nhap Buoc Di:")
        if number == "5":
            res = state.move_up()
        elif number == "2":
            res = state.move_down()
        elif number == "1":
            res = state.move_left()
        elif number == "3":
            res = state.move_right()
        else: continue
        
        if res == False:
            print("GAME OVER!")
            break
        os.system('cls')
        state.print_maps()
        if  state.check_goal():
            print("WINNER!")
            break
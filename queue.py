# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:45:51 2017

@author: https://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaQueueinPython.html
"""

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
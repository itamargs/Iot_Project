#!/usr/bin/python
#-*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Data(ABC):
    def __init__(self):
        self.type = None
        self.isRelevamt = None
        self.dateAdded = None
        self.lastUpdateDate = None

    @abstractmethod
    def update(self, ):
        pass


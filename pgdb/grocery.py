import os

class product(object):
    def __init__(self, vegId, price, qty, weight, orderqty=0):
        self.vegId = vegId
        self.price = price
        self.qty = qty
        self.weight = weight
        self.orderqty = orderqty

    def add_veg

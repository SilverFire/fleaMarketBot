#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from item import Item
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, or_


class database(object):
    '''database class for store items, objest should be created before use item'''
    def __init__(self):
        engine = create_engine(config.db, echo=True)
        metadata = MetaData()
        items_table = Table('items', metadata,
            Column('id', Integer, primary_key=True),
            Column('itemName', String),
            Column('itemDescription', String),
            Column('itemPhoto', String),
            Column('userID',String),
            Column('ts', Integer)
        )
        metadata.create_all(engine)
        mapper(Item, items_table)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def save_to_db(self, item):
        '''save item to database'''
        self.session.add(item)
        self.session.commit()

    def get_by_user(self, user):
        '''get all items by userID'''
        return self.session.query(Item).filter(Item.userID == user).all()

    def get_from_date(self, ts):
        '''get all items from ts date'''
        return self.session.query(Item).filter(Item.ts >= ts).all()

    def find(self, str):
        '''find item by sting it name or description'''
        return self.session.query(Item).filter(or_(Item.itemName.like('%'+str+'%'), Item.itemDescription.like('%'+str+'%'))).all()
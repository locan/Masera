# -*- coding:utf-8 -*-
import json

from ansible.inventory import Inventory
class Inventory(object):
    def __init__(self):
        self.inventory = {}

    # Example inventory for testing.
    def _inventory(self):
        '''此处完成动态获取inventory
        '''
        group = {}
        _meta = {}
        result = {}
        return result

    def get_inventory(self):
        self._inventory()
        return json.dumps(self.example_inventory())

    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

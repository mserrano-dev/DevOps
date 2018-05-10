#!/usr/bin/python
import awscli
from infrastructure.interface import Platform

# ---------------------------------------------------------------------------- #
# Infrastructure via Amazon Web Services
# ---------------------------------------------------------------------------- #
class Infrastructure(Platform):
    def create_server(self):
        return
    
    def remove_server(self, KEY):
        print KEY
        return
#!/usr/bin/python
import awscli
from infrastructure.interface import Infrastructure

# ============================================================================ #
# Infrastructure via Amazon Web Services
# ============================================================================ #
class Platform(Infrastructure):
    def create_server(self):
        return
    
    def remove_server(self, KEY):
        print KEY
        return
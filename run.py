#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:31:29 2024

@author: cardotcm
"""
import os, secrets

from ThronExpress import app
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = secrets.token_hex()

    app.run(debug = True)

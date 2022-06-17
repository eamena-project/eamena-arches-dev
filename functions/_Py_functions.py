# -*- coding: utf-8 -*-
"""
Created on ...

@description: ...
"""

import psycopg2
        
conn = psycopg2.connect(
    host="ec2-54-155-109-226.eu-west-1.compute.amazonaws.com",
    database="24test",
    user="postgres",
    password="postgis")

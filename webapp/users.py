#!/usr/bin/python3
# -*- coding: utf-8 -*-
# users.py



from datetime import datetime



class User():
 
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
               "JaneDoe": ("JaneDoe", "Jane")}
 
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return 'admin'
 
    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

        
    def __repr__(self):
        return '<User %r>' % (self.username)  
  
  
  
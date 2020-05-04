from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
import click
import functools
from setuptools import setup
import sqlite3
import os
from App.Config.db import *
    
    
def get(db, table, id=None, arg2=None): #arg2 = name if users or title if articles
    if id is None and arg2 is None:
        
        if table == "users":
            return db.execute('SELECT * FROM users ').fetchall()
        if table == "articles":
            return db.execute('SELECT * FROM articles ').fetchall()
        
    elif arg2 is None:
        if table == "users":
            return db.execute('SELECT * FROM users WHERE id = ?', ( id,)).fetchone()
        if table == "articles":
            return db.execute('SELECT * FROM articles WHERE id = ?', ( id,)).fetchone()
        
    elif id is None:
        if table == "users":
            return db.execute('SELECT * FROM users WHERE username = ?', ( arg2,)).fetchone()
        if table == "articles":
            return db.execute('SELECT * FROM articles WHERE title = ?', ( arg2,)).fetchone()
        

def delete(db, table, id): 
    if table == "users":
        db.execute('DELETE FROM users WHERE id = ?', (id,))
    if table == "articles":
        db.execute('DELETE FROM articles WHERE id = ?', (id,))
    db.commit()

def put(db , table, arg1, arg2, arg3=None):
    """     if users: arg1,2,3:name,email, password      if articles: arg1,2,3:title,body,userId   """
    
    if table == "users":
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',(arg1, arg2, arg3))
    elif table=="articles":
        db.execute('INSERT INTO articles (title, body, userId) VALUES (?, ?,? )',(arg1, arg2,arg3))
    db.commit() 
    
def update(db, table, id, arg1, arg2, arg3=None):
    """     if users: arg1,2,3:name,email, password      if articles: arg1,2,3:title,body,userId   """
    
    if table == "users":
        db.execute('UPDATE users SET username = ?, email= ?, password = ? WHERE id =?',(arg1, arg2, arg3, id))
    elif table=="articles":
        db.execute('UPDATE articles SET title = ?, body= ?, userId= ? WHERE id =?',(arg1, arg2, arg3, id))
    db.commit()
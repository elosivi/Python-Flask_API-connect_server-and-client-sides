from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
import click
import functools
from setuptools import setup

from App.Models import model 
from App.Config import db


class ArticlesController:
    
    def getAll(self):

        datab = db.get_db() 
        articles = model.get(datab,'articles')
        print(articles)
        return jsonify(articles) 
    
    def returnArt(self,id=""):#added d2 ex2
        datab = db.get_db()
        return model.get(datab,'articles',id)
    
    def crud(self,request,id=""):
        datab = db.get_db() 
        
        if request.method == 'GET': 
            articles = model.get(datab,'articles',id)
            return jsonify(articles)
            
        elif request.method == 'PUT':
            title= request.form['title']
            body= request.form['body']
            userId= session['userId'] 
            model.put(datab,'articles',title,body,userId)
            response = 'your article is added, thanks!'
            return response
            
        elif request.method =='DELETE':
            model.delete(datab,'articles', id)
            response = 'The User #'+str(id)+'is deleted now'
            return response
        
        elif request.method == 'POST':
            new_title= request.form['title']
            new_body= request.form['body']
            new_userId=session['userId'] 
            actual = model.get(datab, 'articles', id)


            if new_title == "":
                new_title = actual[1]
            if new_body == "":
                new_body= actual[2]
            if new_userId == "":
                new_userId = actual[4]
            
            model.update(datab,'articles',id, new_title, new_body, new_userId)
            response = 'The article #'+str(id)+'is updated'
            return response
    
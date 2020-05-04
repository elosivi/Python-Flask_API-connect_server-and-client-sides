from flask import Flask, Response, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint, session, json
import click
import functools
from setuptools import setup

from App.Config.db import *
from App.Controllers.usersController import UsersController
from App.Controllers.articlesController import ArticlesController


""" under blueprint creation """


bp = Blueprint('templates', __name__, url_prefix='/templates')
actualUser = UsersController()
actualArticle=ArticlesController()

# ##################################    i n d e x    ##################################
    
@app.route('/') 
def index() : 
    if 'logged_in' in session:
        username = session['username']
        userId = session['userId']
        return "Welcome "+username+"("+str(userId)+") !"
    else:
        return "please log you : ../login (or register you : ./register) -> on Postman !"
    
# ##################################    l o g i n     /    r e g i s t e r   ##################################

@app.route("/login",methods=["POST","GET"])
def login():
    response = actualUser.login(request)
    
    if response == "login":
        username = session['username']
        message = "loginOk"
        return jsonify(message)
    else:
        return jsonify(response)
        
    
@app.route("/register",methods=["POST","GET"])
def register():
    response = actualUser.register(request)
    print('mess=', response)
    if response == 'ok':
        users = actualUser.getAll()
        return jsonify(response)
          
    else:
        return jsonify(response)
    
@app.route('/logout')
def logout():
    message = actualUser.logout()
    return message

# ##################################    u s e r s     m a n a g e m e n t   ##################################

@app.route('/users', methods=["GET","PUT"])
def getAll():
    if request.method == "GET": 
        users = actualUser.getAll()
        return users
    elif request.method == 'PUT': 
        actual = actualUser.crud(request, id)
        users = actualUser.getAll()
        return users
    
@app.route('/users/<id>', methods=["GET", "DELETE", "POST"])
def userCrud(id=None):
    if request.method == 'GET':
        actual = actualUser.crud(request, id)
        return actual
    
    elif request.method == 'DELETE':
        response = actualUser.crud(request, id)
        flash(response)
        return response
    
    elif request.method == 'POST':
        response=actualUser.crud(request,id)
        flash(response)
        users = actualUser.getAll()
        return users
        

        
# ##################################    a r t i c l e s     m a n a g e m e n t   ##################################    
     
@app.route('/articles', methods=["GET","PUT"]) 
def getAllArt():
    """
    1/ verify if user is identified(login)
    2/ if yes he can post a new article
    if not he can only get/read all articles
    """
    if request.method == "GET": 
        articles = actualArticle.getAll()
        return articles
        
    elif request.method == 'PUT': 
        if 'logged_in' in session:
            response = actualArticle.crud(request, id)
            articles = actualArticle.getAll()
            return articles
        else:
            message="To add a new article you have to log/register you thanks"
            return message
    
    
@app.route('/articles/<id>', methods=["GET", "DELETE", "POST"])
def artCrud(id=None):
    """
    1/ verify if user connected is the owner. if yes, set 'owner' at true
    2/ if owner is true he can delete ou post his article
    if not he can only get
    """
    #added d02 ex02 : owner and logged notion
    owner = False
    
    if 'logged_in' in session:
        userConnectedId = session['userId'] 
        actual = actualArticle.returnArt(id)
        userIdArticle = actual[4]

        if userConnectedId == userIdArticle:
            owner = True
        
        if request.method == 'GET':
            actual = actualArticle.crud(request, id)
            return actual
        
        elif request.method == 'DELETE':

            if owner == True:
                response = actualArticle.crud(request, id)
            else:
                response = "You are not the owner of this article, you can't delete it"
                return response
            flash(response)
            articles = actualArticle.getAll()
            return articles
        
        elif request.method == 'POST':

            if owner == True:
                response=actualArticle.crud(request,id)
            else:
                response = "You are not the owner of this article, you can't modify it"    
                return response
            flash(response)
            articles = actualArticle.getAll()
            return articles
        
    else:
        message="To access a specific article, you have to log/register you thanks"
        return message
  
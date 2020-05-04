from flask import Flask, Response, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint, session, json
from setuptools import setup
import requests

import http.client
import mimetypes

import socket

from Client.Controllers.usersController import UsersController
from Client.Controllers.articlesController import ArticlesController


   
client=Flask( __name__ ) 
client.secret_key = "super_secret_key"

bp = Blueprint('templates', __name__, url_prefix='/templates')
actualUser = UsersController()
article=ArticlesController()


########################## i n d e x  ############################
 
 
@client.route('/')  #ok works
def index():
    if 'logged_in' in session:
        username=session['username']
        return render_template("index.html",  username=session['username'])
    else:
        return redirect(url_for('login'))
    
    
########################## l o g / s e s s i o n s  ############################
    
    
@client.route("/login",methods=["POST","GET"]) #ok works
def login():
    newlog = actualUser.login(request)
    if newlog == "index":
        return redirect(url_for('index'))
    else:
        if newlog is None:
            return render_template('login.html')
        else:
            error=newlog
            flash(error)
            return render_template('login.html',error=error)
        
    
@client.route("/register",methods=["POST","GET"]) #ok works
def register():
    newRegister = actualUser.register(request)
    print('newReg=', newRegister)
    
    if newRegister == "ok":
        return render_template('login.html')
    else:    
        error = newRegister
        if error is None:
            return render_template('register.html')
        else:
            flash(error)
            return render_template('register.html',error=error)

    
@client.route('/logout') #ok works
def logout():
    newLogout = actualUser.logout()
    return redirect(url_for('index'))    
    
    
########################## u s e r s  ############################


@client.route('/users') #ok works
def users():
    if 'logged_in' in session:
        r= actualUser.get()
        return render_template('users.html', users=json.loads(r.text))
    else:
        return redirect(url_for('login'))
    
@client.route('/users/<id>')#ok works 
def user(id=None):
    if 'logged_in' in session:
        r = actualUser.get(id)
        user=json.loads(r.text)
        return render_template('user.html', user=user)
    else:
        return redirect(url_for('login'))
    
    
@client.route('/users/delete/<id>')#ok works
def delete(id=None):
    if 'logged_in' in session:
        r = actualUser.delete(id)
        message="user #"+id+" is now deleted"
        flash(message)
        return render_template('users.html',error=message)
    else:
        return redirect(url_for('login'))
    
    
########################## a r t i c l e s ############################


@client.route('/articles') #ok works 
def articles():
    if 'logged_in' in session:
        r=article.get()
        return render_template('articles.html', articles=json.loads(r.text))
    else:
        return redirect(url_for('login'))
    
@client.route('/articles/<id>')
def oneArticle(id=None):
    if 'logged_in' in session:
        r=article.get(id)
        oneArticle = json.loads(r.text)
        return render_template('article.html', article=oneArticle)
    else:
        return redirect(url_for('login'))    
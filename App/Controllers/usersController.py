from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
import click
import functools
from setuptools import setup

from App.Models import model 
from App.Config import db

class UsersController:
    
    def login(self, request): 
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            datab = db.get_db() 
            error = None
            user = model.get(datab,'users',None,username)

            if user is None:
                error = 'Incorrect username.'
                
            elif not check_password_hash(user[3], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['logged_in'] = True
                session['userId'] = user[0]
                session['username'] = username
                session['email'] = user[2]

                return "login"
            
            flash(error)
        
        return error


    def register(self, request):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            datab = db.get_db() 
            error = None
            userExist = model.get(datab, 'users',None, username)
            
            if not username:
                error = 'Username is required.'
            elif not email:
                error = 'Email is required.'               
            elif not password:
                error = 'Password is required.'
            elif password != confirm_password:
                error= 'password confirmation is different'
            elif userExist is not None:
                error = 'User {} is already registered.'.format(username)
            
            if error is None:
                hashed_Password=generate_password_hash(password)
                model.put(datab,'users',username,email, hashed_Password)
                return "ok"

            flash(error)
            
        return error
    
    
    def logout(self):
        session.clear()
        message="bye bye ! Seen you soon again (Hope!)"
        return message
    
    def getAll(self):
        datab = db.get_db() 
        users = model.get(datab,'users')
        return jsonify(users) 
    
    def crud(self,request,id=""):
        datab = db.get_db() 
        # name= request.form['username']
        # email= request.form['email']
        # password=request.form['password']     
        
        if request.method == 'GET': 
            user = model.get(datab,'users',id)
            return jsonify(user)
            
        elif request.method == 'PUT':
            name= request.form['username']
            email= request.form['email']
            password=request.form['password']

            model.put(datab,'users',name,email,password)
            response = 'The User #'+str(id)+'is added'
            return response
            
        elif request.method =='DELETE':
            model.delete(datab,'users', id)
            response = 'The User #'+str(id)+'is deleted now'
            print("********************")
            print(response)
            return response
        
        elif request.method == 'POST':
            new_name= request.form['username']
            new_email= request.form['email']
            new_password=request.form['password'] 
            actual = model.get(datab, 'users', id)

            if new_name == "":
                new_name = actual[1]
            if new_email == "":
                new_email= actual[2]
            if new_password == "":
                new_password = actual[3]
            
            model.update(datab,'users',id, new_name, new_email, new_password)
            response = 'The User #'+str(id)+'is updated'
            return response
            
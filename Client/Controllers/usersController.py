from flask import Flask,jsonify, json, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
import click
import requests
import functools
from setuptools import setup

from App.Models import model 
from App.Config import db

class UsersController:
    
    def login(self, request): #ok works

        if request.method == 'POST':
           
            username = request.form['username']
            password = request.form['password']
              
            r = requests.post(url='http://localhost:5000/login',data={'username': username, 'password': password})
            log = r.json()

            if log == "loginOk":
                session.clear()
                session['logged_in'] = True
                #  session['userId'] = user[0]
                session['username'] = username
                #  session['email'] = user[2]
                return "index"
            else:
                if log is None:
                    return ""
                else:
                    return log


    def register(self, request): #ok works
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            r = requests.post(url='http://localhost:5000/register',data={'username': username, 'email':email, 'password':password, 'confirm_password':confirm_password})
            log = r.json()   
            return log
        
    
    def logout(self): #ok works
        session.clear()
        message="bye bye ! Seen you soon again (Hope!)"
        return message
    

    
    def get(self,id=None):
        print(">>>>>>>>>>>>>> get()---------------")
        if id is None:
    
            r = requests.get('http://localhost:5000/users') 
        else:
            print("---------------get(id)---------------")
            print(id)
            request='http://localhost:5000/users/'+id
            print(request)
            r = requests.get('http://localhost:5000/users/'+id)
        return r
    
    def delete(self, id):
        r = requests.delete('http://localhost:5000/users/'+id)
        print("---------------delete return----------------")
        print(r)
        return r       
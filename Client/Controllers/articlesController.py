from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
import click
import requests
import functools
from setuptools import setup

from App.Models import model 
from App.Config import db


class ArticlesController:
    
    def get(self,id=None):
        if id is None:
            r = requests.get('http://localhost:5000/articles') 
        else:
            r = requests.get('http://localhost:5000/articles/'+id)
        return r
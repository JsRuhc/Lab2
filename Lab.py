# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:42:51 2019

@author: Administrator
"""

from flask import Flask, request,Blueprint
from UseSqlite import InsertQuery
from datetime import datetime
from upload_bp import upload_bp
from show_bp import show_bp
from search_bp import search_bp
from api_bp import api_bp

app=Flask(__name__)

app.register_blueprint(upload_bp)
app.register_blueprint(show_bp)
app.register_blueprint(search_bp)
app.register_blueprint(api_bp)


@app.route('/')
def main():
        page='''
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css" />
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js" />
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css" />
<!DOCTYPE  html>
<html lang="en">
  <body> 
    <div class="container">
        <center>
       <h1>Welcome To Use PhotoString</h1>
      <a href='/upload'><button type="button" class="btn btn-prinary btn-lg" >upload</button></a>
      <a href='/show'><button type="button" class="btn btn-prinary btn-lg">show</button></a>
      <a href='/search'><button type="button" class="btn btn-prinary btn-lg">search</button></a>
      <a href='/api'><button type="button" class="btn btn-prinary btn-lg" >api</button></a>
      </center>
      </div>

    </body>
  </html>'''
        return page
    
if __name__=='__main__':
    print(app.url_map)
    app.run(debug=True)
    
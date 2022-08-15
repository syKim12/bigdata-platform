from django.shortcuts import render
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import pymysql.cursors
from django.conf import settings
#import requests

#Create mysql connection



# Create your views here.
def main(request):
    return render(request, 'main.html')

def index(request):
    sql = """SELECT * FROM passenger_str"""
    mysql_connection = pymysql.connect(host=getattr(settings, "DB_HOST"), port=3306, user=getattr(settings, "DB_USER"),password=getattr(settings, "DB_PW"),db=getattr(settings, "DB_NAME"),cursorclass=pymysql.cursors.DictCursor)
    #get table from sql
    with mysql_connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()

    df = pd.DataFrame(row)
    rs = df.groupby("line_num")["ride_pasgr_num"].agg("sum")
    categories = list(rs.index)
    values = list(rs.values)
	

    temp = df.to_html(index=None)
    table_content = temp.replace("<thead>","<thead class='thead-dark'>")
    table_content = table_content.replace('class="dataframe"',"class='table table-striped'")
    table_content = table_content.replace('border="1"',"")
	
    context = {'categories': categories, 'values': values, 'table_data': table_content}
    return render(request, 'index.html', context= context)

def datepicker(request):
    date = request.POST.get('date')
    cleaned_date = date.replace('-', '')
    sql = """SELECT * FROM passenger_str WHERE use_dt = """ + cleaned_date
    mysql_connection = pymysql.connect(host=getattr(settings, "DB_HOST"), port=3306, user=getattr(settings, "DB_USER"),password=getattr(settings, "DB_PW"),db=getattr(settings, "DB_NAME"),cursorclass=pymysql.cursors.DictCursor)
    #get table from sql
    with mysql_connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()

    df = pd.DataFrame(row)
    rs = df.groupby("line_num")["ride_pasgr_num"].agg("sum")
    categories = list(rs.index)
    values = list(rs.values)
	

    temp = df.to_html(index=None)
    table_content = temp.replace("<thead>","<thead class='thead-dark'>")
    table_content = table_content.replace('class="dataframe"',"class='table table-striped'")
    table_content = table_content.replace('border="1"',"")
	
    context = {'categories': categories, 'values': values, 'table_data': table_content}
    return render(request, 'index-date.html', context= context)
    
  
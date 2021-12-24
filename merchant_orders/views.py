from django.shortcuts import render
import datetime
import pymysql
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.db import connection
import json
from SQL_connection.sqlhelper import SqlHelper
# Create your views here.

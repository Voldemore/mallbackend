from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.response import Response
from django.db import connection
import json
import pymysql
from SQL_connection.sqlhelper import SqlHelper


class MerQuery(APIView):
    []

class GoodsQuery(APIView):
    []
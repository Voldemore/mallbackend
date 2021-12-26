
# Create your views here.

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
import json
from SQL_connection.sqlhelper import SqlHelper

#管理员登录
class Login(APIView):
    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            print("received POST request at api/admin/login/")
            data = json.loads(request.body)
            admin_id = data.get('admin_email')
            password = data.get('password')
            sql_select = "select * from mall.administrator where admin_id = %s and password = %s"
            obj = SqlHelper()
            result0 = obj.get_one(sql_select, [admin_id, password, ])
            if result0 is not None:
                result = {}
                result['admin_name'] = result0['admin_name']
                obj.close()
                resp = {
                    'id': 0,
                    'msg': "Success",
                    'payload': result
                }
                return Response(resp)

            else:
                resp = {
                    'id': -1,
                    'msg': "User not found"
                }
                return Response(resp)


class GoodsSearchKeywords(APIView):
    def get(self,request, *args, **kwargs):
        if request.method == 'GET':
            print("received the GET request at api/admin/goods_search/")
            data = request.GET
            variety = data.get('keywords')
            print("keywords")
            obj = SqlHelper()
            sql_select = 'select goods_id,des,maker,image,price,sales,stock ' \
                         'from mall.view_admin_goods_search_keywords ' \
                         'where variety = %s'
            result1 = obj.get_list(sql_select, [variety, ])
            result2 = obj.get_one(sql_select, [variety, ])
            print(result2)
            if result2 is not None:
                obj.close()
                resp = {
                    'id': 0,
                    'msg': 'Success',
                    'payload': result1
                }

            else:
                resp = {
                    'id': -1,
                    'msg': 'Goods can not found',
                    'payload': []
                }
            return Response(resp)


#搜索所有的商家
class all_merchants(APIView):
    def get(self,request, *args, **kwargs):
        if request.method == 'GET':
            print("received the GET request at api/admin/allmer_search")
            sql_select = "select mer_id,mer_name,goods_num,goods_typenum,income " \
                         "from mall.view_mer_goods_num_type_sales"
            obj = SqlHelper()
            result = obj.get_list(sql_select,[])
            obj.close()
            resp={
                'id':0,
                'msg': 'success',
                'payload':result
            }
            return Response(resp)


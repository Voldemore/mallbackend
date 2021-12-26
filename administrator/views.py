
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
            sql_select = "select name from mall.administrator where admin_id = %s and password = %s"
            obj = SqlHelper()
            result0 = obj.get_one(sql_select, [admin_id, password, ])
            print(result0)
            if result0 is not None:
                result = {}
                result['admin_name'] = result0['name']
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


# 按照商品种类搜索商品
class GoodsSearchKeywords(APIView):
    def get(self,request, *args, **kwargs):
        if request.method == 'GET':
            print("received the GET request at api/admin/goods_search/")
            data = request.GET
            variety = data.get('keywords')
            print(variety)
            obj = SqlHelper()
            sql_select = 'select goods_id,des,maker,image,price,sales,stock,comments ' \
                         'from mall.view_admin_goods_search_keywords ' \
                         'where variety = %s'
            result1 = obj.get_list(sql_select, [variety, ])
            result2 = obj.get_one(sql_select, [variety, ])
            print(result2)
            obj.close()
            if result2 is not None:
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


# 按照商家名称搜索商家
class MerchantSearchKeywords(APIView):
    def get(self,request, *args, **kwargs):
        if request.method == 'GET':
            print("received the GET request at api/admin/mer_search/")
            data = request.GET
            mer_id = data.get('keywords')
            print("keywords")
            obj = SqlHelper()
            sql_select = 'select mer_id, mer_name, goods_id, goods_name, goods_type, ' \
                         'goods_price, goods_sales, goods_stock, goods_income ' \
                         'from mall.view_admin_merchant ' \
                         'where mer_id = %s'
            result1 = obj.get_list(sql_select, [mer_id, ])
            result2 = obj.get_one(sql_select, [mer_id, ])
            print(result2)
            obj.close()
            if result2 is not None:

                resp = {
                    'id': 0,
                    'msg': 'Success',
                    'payload': result1
                }

            else:
                resp = {
                    'id': -1,
                    'msg': 'Goods cannot found',
                    'payload': []
                }
            return Response(resp)


# 搜索用户订单
class UserOrderSearch(APIView):
    def get(self,request, *args, **kwargs):
        if request.method == 'GET':
            print("received the GET request at api/admin/user_order_search/")
            data = request.GET
            user_id = data.get('keywords')
            print(user_id)
            obj = SqlHelper()
            sql_select = 'select user_id, user_name, order_num, sum_cost, max_cost, min_cost ' \
                         'from mall.view_admin_user_order ' \
                         'where user_id = %s'
            result1 = obj.get_list(sql_select, [user_id, ])
            result2 = obj.get_one(sql_select, [user_id, ])
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
                    'msg': 'Goods cannot found',
                    'payload': []
                }
            return Response(resp)


# 搜索用户商品
class UserGoodsSearch(APIView):
    def get(self,request, *args, **kwargs):
        if request.method == 'GET':
            print("received the GET request at api/admin/user_goods_search/")
            data = request.GET
            user_id = data.get('keywords')
            print(user_id)
            obj = SqlHelper()
            sql_select = 'select user_id, goods_id, goods_name, goods_price, goods_num, goods_cost ' \
                         'from mall.view_admin_user_goods ' \
                         'where user_id = %s'
            result1 = obj.get_list(sql_select, [user_id, ])
            result2 = obj.get_one(sql_select, [user_id, ])
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
                    'msg': 'Goods cannot found',
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

class user_province_search(APIView):
    def get(self,request,*args,**kwargs):
        if request.method == "GET":
            data = request.GET
            sql_select = "select province,user_num,order_num,avg_cost,max_cost,min_cost from mall.view_user_order_province"
            obj = SqlHelper()
            result = obj.get_list(sql_select,[ ])
            resp = {
                'id':0,
                'msg':'success',
                'payload':result
            }
            return Response(resp)



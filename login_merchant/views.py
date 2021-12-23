from django.shortcuts import render

# Create your views here.
# Create your views here.
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
# 在内置的User中username,定义为email

# 商家注册
class Register(APIView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            print("receive POST request at /merchant/register")
            # handle the request
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            username = data.get('name')
            mobile = data.get('mobile')
            province = data.get('province')
            city = data.get('city')
            county = data.get('county')
            address = data.get('address')

            if User.objects.filter(username=email).exists():
                resp = {
                    'id': -1,
                    'msg': 'Username already exists',
                }
            else:
                user = User.objects.create_user(username=email, password=password, is_staff=1)
                obj = SqlHelper()
                operation_insert = 'insert into mall.merchant(mer_id,name,mobile,province,city,county,address) values(%s,%s,%s,%s,%s,%s,%s)'

                obj.modify(operation_insert, [email, username, mobile, province, city, county, address, ])
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
                obj.close()

        return Response(resp)


# 商家登录
class Login(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /merchant/login")
            data = json.loads(request.body)
            print(data)
            email = data.get('mername')  # actually email
            password = data.get('password')
            print(email)
            print(password)
            #   内置验证
            n = authenticate(username=email, password=password)
            print(n)
            if n is not None:
                # 登陆成功即可获取当前登录用户，返回主页
                auth.login(request, user=n)
                user = User.objects.get(username=email)
                staff_state = user.is_staff
                if staff_state == 1:
                    operation_select = "select name,mobile,province,city,county,address from mall.view_merchant_users where mer_id = %s"
                    obj = SqlHelper()
                    result = obj.get_one(operation_select, [email, ])
                    obj.close()
                    result['time'] = datetime.datetime.now()

                    # return
                    resp = {
                        'id': 0,
                        'msg': 'Success',
                        'payload': result
                    }
                else:
                    resp = {
                        "id": -1,
                        "msg": "username doesn't exist",
                    }

                return Response(resp)
            # 失败重定向到登录页
            # test----------------------------------------------
            else:
                user = User.objects.filter(username=email)

                if len(user) != 0:
                    user = User.objects.get(username=email)
                    pwd = user.password
                    staff_state = user.is_staff

                    if (check_password(password, pwd) is False) and (staff_state == 1):
                        resp = {
                            "id": -2,
                            "msg": "password incorrect"
                        }
                    else:
                        resp = {
                            "id": -1,
                            "msg": "username doesn't exist",
                        }

                else:

                    resp = {
                        "id": -1,
                        "msg": "username doesn't exist--len(user)==0",
                    }

                return Response(resp)


# 获取商家信息
class Merchant_Info(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /merchant_info")
            data = request.GET  # 处理请求
            mer_id = int(data.get('mername'))
            print(mer_id)
            user = User.objects.filter(username=mer_id)
            if user is not None:
                user = User.objects.get(username=mer_id)
                if user.is_staff == 1:
                    obj = SqlHelper()
                    sql_select = 'select mer_id,name,mobile,province,city,county,address ' \
                                 'from mall.view_merchant_users ' \
                                 'where mer_id = %s'
                    result = obj.get_one(sql_select, [mer_id, ])
                    result['time'] = datetime.datetime.now()
                    obj.close()
                    resp = {
                        'id': 0,
                        'msg': 'success',
                        'payload': result
                    }
                else:
                    resp = {
                        'id': -1,
                        'msg': "the merchant id doesn't exist"
                    }
            else:
                resp = {
                    'id': -1,
                    'msg': "the merchant id doesn't exist"
                }
            return Response(resp)


# 该商家的所有商品
class Home(APIView):
    def get(self, request, *args, **kargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /home")
            data = request.GET  # 处理请求
            mer_id = data.get('mer_id')
            print(mer_id)
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            obj = SqlHelper()
            sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                          'from mall.view_goods_search ' \
                          'where mer_id = %s ' \
                          'order by price'
            result1 = obj.get_list(sql_select1, [mer_id, ])
            result2 = obj.get_one(sql_select1, [mer_id, ])
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


# 删除商品
# class Delete(APIView):
#     def get(self, request, *args, **kargs):
#         if request.method == 'GET':  # 要求使用GET请求方式
#             print("receive GET request at /delete")
#             data = request.GET  # 处理请求
#             mer_id = data.get('mer_id')
#             print(mer_id)
#             goods_id = data.get('goods_id')
#             print(goods_id)


class Add(APIView):
    def post(self, request, *args, **kargs):
        if request.method == 'POST':  # 要求使用POST请求方式
            print("receive POST request at /bill_of_goods")
            data = json.loads(request.body)
            mer_id = data.get('mer_id')
            goods_id = data.get('goods_id')
            price = data.get('price')
            sales = data.get('sales')
            stock = data.get('stock')
            print(mer_id)
            print(goods_id)
            print(price)
            print(sales)
            print(stock)
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            obj = SqlHelper()
            sql_check1 = 'select name ' \
                         'from mall.merchant ' \
                         'where mer_id = %s '
            check1 = obj.get_one(sql_check1, [mer_id,])
            print(check1)

            if check1 is not None:
                sql_addgoods = 'insert into mall.mergoods(mer_id, goods_id, price, stock, sales) ' \
                               'values(%s, %s, %s, %s, %s)'
                obj.modify(sql_addgoods, [mer_id, goods_id, price, stock, sales])
                obj.close()
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
            else:
                resp = {
                    'id': -1,
                    'msg': 'Fail'
                }
            return Response(resp)











# ####################################以下存疑#######################################


# 该商家的所有订单
class Goods_Bill(APIView):
    def get(self, request, *args, **kargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /bill_of_goods")
            data = request.GET  # 处理请求
            mer_id = data.get('mer_id')
            print(mer_id)
            user = User.objects.filter(username=mer_id)
            if user is not None:
                user = User.objects.get(username=mer_id)
                if user.is_staff == 1:
                    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
                    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                    sql_select0 = "select goods_id,price,sales,stock " \
                                      "from mergoods " \
                                      "where mer_id = %s"
                    cursor.execute(sql_select0, [mer_id, ])
                    sql_select = "select goods.goods_id,goods.goods_name,goods.image,mergoods.price,mergoods.sales,mergoods.stock " \
                                 "from goods,mergoods " \
                                 "where goods.goods_id = mergoods.goods_id"
                    cursor.execute(sql_select)
                    result_list = cursor.fetchall()
                    conn.close()
                    resp = {
                        'id': 0,
                        'msg': 'success',
                        'payload': result_list
                    }
                else:
                    resp = {
                        'id': -1,
                        'msg': "the merchant id doesn't exist"
                    }
            else:
                resp = {
                    'id': -1,
                    'msg': "the merchant id doesn't exist"
                }
            return Response(resp)

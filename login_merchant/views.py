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

# 商家注册，更新shopname
class Register(APIView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            print("receive POST request at /merchant/register")
            # handle the request
            data = json.loads(request.body)
            email = data.get('email')
            name = data.get('mername')
            shopname = data.get('shopname')
            password = data.get('password')
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
                operation_insert = 'insert into mall.merchant(mer_id,name,mobile,province,city,county,address,shopname) ' \
                                   'values(%s,%s,%s,%s,%s,%s,%s,%s)'

                obj.modify(operation_insert, [email, name, mobile, province, city, county, address, shopname, ])
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
                obj.close()

        return Response(resp)


# 商家登录，更新shopname
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
                    operation_select = "select name,shopname,mobile,province,city,county,address from mall.merchant where mer_id = %s"
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

# 暂时没有用
class Merchant_Info(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /merchant_info")
            data = request.GET  # 处理请求
            mer_id = data.get('email')
            print(mer_id)
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            user = User.objects.filter(username=mer_id)
            if user is not None:
                user = User.objects.get(username=mer_id)
                if user.is_staff == 1:
                    obj = SqlHelper()
                    sql_select = 'select mer_id,shopname,name,mobile,province,city,county,address ' \
                                 'from mall.merchant ' \
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

# ##############################Info_Mod未经测试

class Info_Mod(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /merchant/merinfo/modification/")
            data = json.loads(request.body)
            mer_id = data.get('mer_id')
            password = data.get('password')
            name = data.get('mername')
            mobile = data.get('mobile')
            province = data.get('province')
            city = data.get('city')
            county = data.get('county')
            address = data.get('address')
            shopname = data.get('shopname')
            # print(shopname)

            # 修改密码
            u = User.objects.get(username=mer_id)
            u.set_password(password)
            u.save()

            # 其他部分
            obj = SqlHelper()
            info_update = 'update mall.merchant ' \
                          'set name = %s, mobile = %s, province = %s, city = %s, county = %s, address = %s, shopname = %s ' \
                          'where mer_id = %s'
            obj.modify(info_update, [name, mobile, province, city, county, address, shopname, mer_id, ])
            sql_select = 'select mer_id,shopname,name,mobile,province,city,county,address  ' \
                         'from mall.merchant ' \
                         'where mer_id = %s'
            result = obj.get_one(sql_select, [mer_id, ])
            print(result)

            resp = {
                'id': 0,
                'msg': 'Success',
                'payload': result
            }
            obj.close()

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
            sql_select1 = 'select goods_id,goods_name,image,price,sales,stock,state ' \
                          'from mall.view_goods_search2 ' \
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



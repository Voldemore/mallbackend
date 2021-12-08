# Create your views here.
import datetime

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.db import connection
import json



# Create your views here.
# 用户注册
# 在内置的User中username,定义为email

class Register(APIView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            print("receive POST request at /register")

            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            username = data.get('name')
            mobile = data.get('mobile')
            province = data.get('province')
            city = data.get('city')
            address = data.get('address')

            if User.objects.filter(username=email).exists():
                resp = {
                    'id': -1,
                    'msg': 'Username already exists',
                }
            else:
                user = User.objects.create_user(username=email, password=password)
                operation_insert = 'insert into mall1.users(user_id,username,mobile,province,city,address) values(%s,%s,%s,%s,%s,%s)'
                cursor = connection.cursor()
                cursor.execute(operation_insert, [email, username, mobile, province, city, address])
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
                cursor.close()

        return Response(resp)


# 用户登录
class Login(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /login")
            data = json.loads(request.body)
            print(data)
            email = data.get('username')#actually email
            password = data.get('password')
            print(email)
            print(password)
            #   内置验证
            #   username = auth.authenticate(username = username, password = password)

            n = authenticate(username=email, password=password)
            print(n)
            if n is not None:
                # 登陆成功即可获取当前登录用户，返回主页
                auth.login(request, user=n)
                operation_select = 'select username,mobile,province,city,address from mall1.users where user_id = %s'
                cursor = connection.cursor()
                cursor.execute(operation_select,[email])
                result = cursor.fetchone()

                dict_res = {'time': datetime.datetime.now(), 'username': result[0], 'mobile': result[1], 'province': result[2], 'city': result[3],
                            'address': result[4], }
                # return
                resp = {
                    'id': 0,
                    'msg': 'Success',
                    'payload': dict_res
                    #     {
                    #     "username": "A",
                    #     "mobile": "10.46.233.207",
                    #     "province": "D",
                    #     "city": "1",
                    #     "address": "1"
                    # }
                }
                return Response(resp)
            # 失败重定向到登录页
            # test----------------------------------------------
            else:
                user = User.objects.filter(username=email)

                print(user)

                if len(user) != 0:
                    user = User.objects.get(username=email)
                    pwd = user.password
                    if check_password(password, pwd) is False:
                        resp = {
                            "id": -2,
                            "msg": "password incorrect"
                        }

                else:

                    resp = {
                        "id": -1,
                        "msg": "username doesn't exist",
                    }

                return Response(resp)


class Test(APIView):
    def get(self, request, *args, **kwargs):
        return Response("hello world")

# sql_insert = 'insert into mall.users(user_id,name,password,email,mobile,province,city) values(%s,%s,%s,%s,%s,%s,%s)'
# cursor = connection.cursor()
# # cursor.execute(sql_insert, ['000000000000002', 'sy', '12345', '200001@ruc.edu.cn', '13767595949', 'jiangxi', 'gaoan'])
# sql_select = 'select * from mall.users'
# cursor.execute(sql_select)
# rows = cursor.fetchall()
# for row in rows:
#   print(row[0])
# #cursor.execute()
# # cursor.close()

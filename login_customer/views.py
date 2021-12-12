# Create your views here.
import datetime

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
import json
from SQL_connection.sqlhelper import SqlHelper


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
            county = data.get('county')
            address = data.get('address')
            print(data)

            if User.objects.filter(username=email).exists():
                resp = {
                    'id': -1,
                    'msg': 'Username already exists',
                }
            else:
                user = User.objects.create_user(username=email, password=password, is_staff=0)
                obj = SqlHelper()

                operation_insert = 'insert into mall.users(user_id,username,mobile,province,city,county,address) values(%s,%s,%s,%s,%s,%s,%s)'
                obj.modify(operation_insert, [email, username, mobile, province, city, county, address, ])
                obj.close()
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }

        return Response(resp)


# 用户登录
class Login(APIView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /customer/login")
            data = json.loads(request.body)
            print(data)
            email = data.get('username')  # actually email
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
                if staff_state == 0:
                    operation_select = 'select username,mobile,province,city,county,address from mall.view_customer_users where user_id = %s'
                    obj = SqlHelper()
                    result = obj.get_one(operation_select, [email, ])
                    result['time'] = datetime.datetime.now()
                    obj.close()
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

                print(user)

                if len(user) != 0:
                    user = User.objects.get(username=email)
                    pwd = user.password
                    staff_state = user.is_staff
                    if (check_password(password, pwd) is False) and (staff_state == 0):
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
                        "msg": "username doesn't exist",
                    }

                return Response(resp)

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
                print("1")
                print(email)
                operation_insert1 = 'insert into mall.users(user_id,username,mobile,province,city,county,address) values(%s,%s,%s,%s,%s,%s,%s)'
                obj.modify(operation_insert1, [email, username, mobile, province, city, county, address, ])
                operation_insert2 = "insert into mall.address(user_id, name, mobile, province, city, county, address) values (%s,%s,%s,%s,%s,%s,%s)"
                obj.modify(operation_insert2,[email, username, mobile, province, city, county, address,])
                operation_select = "select username, mobile, province, city, county, address from mall.users where user_id=%s"
                result = obj.get_one(operation_select, [email, ])
                print(result)
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
                    operation_select = 'select username,mobile,province,city,county,address ' \
                                       'from mall.view_customer_users ' \
                                       'where user_id = %s'
                    obj = SqlHelper()
                    result = obj.get_one(operation_select, [email, ])
                    # result['time'] = datetime.datetime.now()
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
                        "msg": "username doesn't exist--len(user)=0",
                    }

                return Response(resp)


# 获取用户收货地址
class Receive_Address(APIView):
    def get(self, request, *args, **kargs):
        if request.method == 'GET':  # 要求使用GET请求方式
            print("receive GET request at /customer_adddress")
            data = request.GET  # 处理请求
            user_id = data.get('user_id')
            print(user_id)
            user = User.objects.filter(username=user_id)
            if user is not None:
                sql_select = "select addr_id,name,mobile,province,city,county,address " \
                             "from mall.address where user_id = %s"
                obj = SqlHelper()
                result = obj.get_list(sql_select, [user_id, ])
                obj.close()
                resp = {
                    'id': '0',
                    'msg': 'Success',
                    'payload': result,
                }
                return Response(resp)
            else:
                resp = {
                    'id': '-1',
                    'msg': 'user not found'
                }
                return Response(resp)

# 添加用户收货地址
class Add_Receive_address(APIView):
    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            print("receive the post request at api/customer/add_address/")
            data = json.loads(request.body)
            print(data)
            user_id = data.get("user_id")
            name = data.get("name")
            mobile = data.get("mobile")
            province = data.get("province")
            city = data.get('city')
            county = data.get('county')
            address = data.get('address')
            if User.objects.filter(username=user_id).exists():
                obj = SqlHelper()
                sql_insert = "insert into mall.address(user_id, name, mobile, province, city, county, address) " \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s)"
                obj.modify(sql_insert, [user_id, name, mobile, province, city, county, address, ])
                resp = {
                    'id': 0,
                    'msg': 'Success',
                }
            else:
                resp = {
                    "id": -1,
                    "msg": "user not found"
                }
            return Response(resp)


# 修改用户信息
class Info_Mod(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /customer/info/modification/")
            data = json.loads(request.body)
            user_id = data.get('user_id')
            password = data.get('password')
            username = data.get('username')
            mobile = data.get('mobile')
            province = data.get('province')
            city = data.get('city')
            county = data.get('county')
            address = data.get('address')

            # 修改密码

            u = User.objects.get(username=user_id)
            u.set_password(password)
            u.save()

            # 其他部分
            obj = SqlHelper()
            info_update = 'update mall.users ' \
                          'set username=%s, mobile=%s, province=%s, city=%s, county=%s, address=%s ' \
                          'where user_id = %s'
            obj.modify(info_update, [username, mobile, province, city, county, address, user_id, ])
            sql_select = "select username, mobile, province, city, county, address from mall.users where user_id = %s"
            result = obj.get_one(sql_select, [user_id, ])
            print(result)
            resp = {
                'id': 0,
                'msg': 'Success',
                'payload': result,
            }
            obj.close()
            print(resp)

        return Response(resp)

from django.shortcuts import render

# Create your views here.
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import APIView, AuthTokenSerializer
from rest_framework.response import Response
from django.db import connection
import json
import pymysql
from SQL_connection.sqlhelper import SqlHelper
from datetime import datetime


class GoodsSearch(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive GET request at /goods_search/goods_search")
            data = request.GET
            variety = data.get('keywords')
            order = data.get('order')
            direction = data.get('direction')  # 默认升序
            print(variety)
            print(order)
            print(direction)

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            if order == "价格":

                if direction == "升序":
                    obj = SqlHelper()
                    sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                                  'from mall.view_goods_search ' \
                                  'where variety = %s ' \
                                  'order by price'
                    result1 = obj.get_list(sql_select1, [variety, ])
                    result2 = obj.get_one(sql_select1, [variety, ])
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

                elif direction == "降序":
                    obj = SqlHelper()
                    sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                                  'from mall.view_goods_search ' \
                                  'where variety = %s ' \
                                  'order by price desc'
                    result1 = obj.get_list(sql_select1, [variety, ])
                    result2 = obj.get_one(sql_select1, [variety, ])
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

                else:
                    obj = SqlHelper()
                    sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                                  'from mall.view_goods_search ' \
                                  'where variety = %s '
                    result1 = obj.get_list(sql_select1, [variety, ])
                    result2 = obj.get_one(sql_select1, [variety, ])
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


# =========================================================================================================================================
# =========================================================================================================================================
# =========================================================================================================================================

class MerchantSearch(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive GET request at /goods_search/merchant_search")
            data = request.GET
            mer_id = data.get('seller')
            order = data.get('order')
            direction = data.get('direction')  # 默认升序
            print(mer_id)
            print(order)
            print(direction)

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2021mall', db='mall')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            if order == "价格":

                if direction == "升序":
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
                            'msg': 'Goods can not found',
                            'payload': []
                        }
                    return Response(resp)

                elif direction == "降序":
                    obj = SqlHelper()
                    sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                                  'from mall.view_goods_search ' \
                                  'where mer_id = %s ' \
                                  'order by price desc'
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
                        return Response(resp)
                    else:
                        resp = {
                            'id': -1,
                            'msg': 'Goods can not found',
                            'payload': []
                        }
                    return Response(resp)

                else:
                    obj = SqlHelper()
                    sql_select1 = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
                                  'from mall.view_goods_search ' \
                                  'where mer_id = %s '
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
                        return Response(resp)
                    else:
                        resp = {
                            'id': -1,
                            'msg': 'Goods can not found',
                            'payload': []
                        }
                    return Response(resp)


# class GoodsSearch(APIView):
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             print("receive GET request at /goods_search/goods_search")
#             data = json.loads(request.body)
#             variety = data.get('variety')
#
#             print(variety)
#
#             operation_select = 'select goods_id,goods_name,des,maker,variety,image,price,stock ' \
#                                'from mall.view_goods_search ' \
#                                'where type = %s '
#             cursor = connection.cursor()
#             cursor.execute(operation_select, [variety])
#             result = cursor.fetchall()
#
#             dict_res = {
#                 'time': datetime.datetime.now(),
#                 'goods_id': result[0],
#                 'maker': result[1],
#                 'image': result[2],
#                 'goods_name': result[3]
#             }
#
#             resp = {
#                 'id': 0,
#                 'msg': 'Success',
#                 'payload': dict_res
#             }
#
#             return Response(resp)

class Test(APIView):
    def get(self, request, *args, **kwargs):
        return Response("困！")


# =========================================================================================================================================
# =========================================================================================================================================
# =========================================================================================================================================
# 查询商品的详情
class Goods_detail(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive GET request at /order_details")
            data = request.GET  # 处理请求
            good_id = int(data.get('goods_id'))
            mer_id = data.get('mer_id')

            sql_select = "select goods_name,mer_name,image,des,price,sales,stock " \
                         "from mall.view_goods_detail " \
                         "where goods_id = %s and mer_id = %s"
            obj = SqlHelper()
            result = obj.get_one(sql_select, [good_id, mer_id, ])
            if result:
                resp = {
                    'id': '0',
                    'msg': 'success',
                    'payload': result
                }

            else:
                resp = {
                    'id': "-1",
                    'msg': 'goods not found'
                }
            obj.close()
            return Response(resp)


# 查找一个商品所有的评论
class Goods_comments(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive GET request at /order_details")
            data = request.GET  # 处理请求
            good_id = int(data.get('goods_id'))
            mer_id = data.get('mer_id')
            sql_select = 'select username,comments ' \
                         'from mall.view_users_comments ' \
                         'where goods_id = %s and mer_id = %s'
            obj = SqlHelper()
            result = obj.get_list(sql_select, [good_id, mer_id, ])
            print(result)
            if result:
                resp = {
                    'id': '0',
                    'msg': 'Success',
                    'payload': result
                }
            else:
                resp = {
                    'id': '-1',
                    'msg': 'goods not found'
                }
            obj.close()
            return Response(resp)


# 商品添加购物车 此时需要判断商品是否在购物车中只需要增加数量
class add_to_cart(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("receive POST request at /goods_detail/addtocart/")
            data = json.loads(request.body)
            user_id = data.get('user_id')
            goods_id = data.get('goods_id')
            mer_id = data.get('mer_id')
            num = data.get('num')
            add_time = datetime.now()
            obj = SqlHelper()

            sql_select = "select stock from mall.mergoods where mer_id = %s and goods_id= %s"

            result = obj.get_one(sql_select, [mer_id, goods_id, ])
            stock = result['stock']
            if stock > 0:
                sql_select1 = "select goods_id, mer_id, user_id, num, add_time " \
                              "from mall.cart " \
                              "where goods_id = %s and mer_id = %s and user_id = %s"
                result1 = obj.get_one(sql_select1, [goods_id, mer_id, user_id, ])
                if result1 is not None:
                    add_time = datetime.now()
                    sql_update = "update mall.cart set num = %s,add_time = %s where goods_id = %s and mer_id = %s and user_id = %s"
                    result2 = obj.create(sql_update, [num, add_time, goods_id, mer_id, user_id, ])
                else:
                    sql_insert = "insert into mall.cart(goods_id, mer_id, user_id, num, add_time) " \
                                    "values (%s,%s,%s,%s,%s)"
                    obj.modify(sql_insert, [goods_id, mer_id, user_id, num, add_time, ])
                obj.close()
                resp = {
                    "id": 0,
                    "msg": "Success",
                }
                return Response(resp)
            else:
                resp = {
                    'id': -1,
                    'msg': 'Goods not found'
                }
                return Response(resp)

class customer_home(APIView):
    def get(self,request, *args,**kwargs):
        if request.method == 'GET':
            print("receive GET request at api/goods_search/inquiry/")
            data = request.GET
            number = int(data.get('number'))
            sql_select = "select mer_id,shopname,goods_id,goods_name,des,maker,variety,image,price,stock from mall.view_customer_home"
            obj = SqlHelper()
            result = obj.get_many(sql_select, [], number)
            obj.close()
            if result is not None:
                resp = {
                    'id': 0,
                    'msg': "success",
                    'payload': result
                }
                return Response(resp)
            else:
                resp={
                    'id': -1,
                    'msg':"goods not found"
                }
                return Response(resp)
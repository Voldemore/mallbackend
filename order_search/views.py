from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from django.db import connection
import json
from rest_framework.authtoken.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response


class order_inquiry(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            print("receive GET request at /order_inquiry")

            data = request.GET
            user_id = data.get('user_id')
            print(user_id)
            if User.objects.filter(username=user_id).exists():
                print("1")
                #inquiry_sql = 'select order_id,mer_id,goods_id,city,address from mall1.orderitem where user_id = %s'
                resp = {
                        'id': 0,
                        'msg': 'Success',
                        'payload': [{
                            "order_id": "订单号",
                            "mer_name": "店铺名",
                            "goods_name": "商品名",
                            "image": "",
                            "num": "购买数量",
                            "amount": "金额"
                        }]
                    }

                return Response(resp)
            #else:
                #inquiry_sql = 'select'


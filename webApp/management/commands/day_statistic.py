import json
from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone
from django.db.models import Sum
from webApp.models import Order, Hotel


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.date = timezone.now().date() - timedelta(days=1)
        self.count_hotel_consumption()

    def count_hotel_consumption(self):
        """统计每个酒店昨天的消费情况"""

        hotels = Hotel.objects.all()
        for hotel in hotels:
            # 获取酒店昨天的所有订单
            orders = Order.objects.filter(
                branch__hotel=hotel, dinner_date=self.date, status=2)
            # 总订单数
            order_number = orders.count()
            # 总人数
            qs = orders.values('dinner_date').annotate(
                sum=Sum('guest_number')).order_by('-sum')
            if qs:
                guest_number = qs[0]['sum']
            else:
                guest_number = 0
            # 总消费
            qs = orders.values('dinner_date').annotate(
                sum=Sum('consumption')).order_by('-sum')
            if qs:
                consumption = qs[0]['sum']
            else:
                consumption = 0
            # 总桌数
            desk_number = 0
            # 人均消费
            guest_consumption = 0.0
            # 桌均消费
            desk_consumption = 0.0
            for order in orders:
                if order.desks:
                    desk_list = json.loads(order.desks)
                    desk_number += len(desk_list)
            if guest_number > 0:
                guest_consumption = '%.2f' % (float(consumption) /
                                              guest_number)
            if desk_number > 0:
                desk_consumption = '%.2f' % (float(consumption) /
                                             desk_number)
            daily_consumption = hotel.day_consumptions.get_or_create(
                date=self.date)[0]

            daily_consumption.order_number = order_number
            daily_consumption.guest_number = guest_number
            daily_consumption.consumption = consumption
            daily_consumption.desk_number = desk_number
            daily_consumption.guest_consumption = guest_consumption
            daily_consumption.desk_consumption = desk_consumption
            daily_consumption.save()

    """
    def count_guest_consumption(self):
        #统计酒店每个顾客的消费情况

        hotels = Hotel.objects.all()
        for hotel in hotels:
            # 获取酒店昨天的所有订单
            orders = Order.objects.filter(
                branch__hotel=hotel, dinner_date=self.date, status=2)
    """

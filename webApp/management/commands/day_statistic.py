import json
import time
from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone
from django.db import connection
from django.db.models import Sum
from webApp.models import Order, Hotel


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.date = timezone.now().date() - timedelta(days=1)
        self.count_hotel_consumption()
        self.count_hotel_guest_consumption()

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
                sum=Sum('guest_number')).order_by('dinner_date')
            if qs:
                guest_number = qs[0]['sum']
            else:
                guest_number = 0
            # 总消费
            qs = orders.values('dinner_date').annotate(
                sum=Sum('consumption')).order_by('dinner_date')
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
                # 结果保留2位小数
                guest_consumption = '%.2f' % (float(consumption) /
                                              guest_number)
            if desk_number > 0:
                # 结果保留2位小数
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

    def count_hotel_guest_consumption(self):
        """统计每个酒店的所有顾客的消费情况"""

        hotels = Hotel.objects.all()
        for hotel in hotels:
            # 获取酒店所有的顾客
            guests = hotel.guests.all()
            for g in guests:
                # 预定桌数(直接写sql查询语句统计)
                sql = '''SELECT SUM(length(replace(desks, "%s", "%s"))
                -length(desks)+1) as sum FROM webApp_order WHERE status = 2 and
                contact = "%s"''' % (",", ",,", g.phone)
                cursor = connection.cursor()
                cursor.execute(sql)
                desk_number = cursor.fetchone()[0]
                if desk_number:
                    desk_number = int(desk_number)
                    g.desk_number = desk_number

                # 人均消费
                qs = Order.objects.filter(
                    contact=g.phone, branch__hotel=hotel, status=2). \
                    values('contact').annotate(sum=Sum('consumption')). \
                    order_by('contact')
                if qs:
                    consumption = qs[0]['sum']
                    g.consumption = consumption
                    # 桌均消费
                    if desk_number:
                        desk_consumption = float(consumption) / desk_number
                        g.desk_consumption = desk_consumption
                    ps = Order.objects.filter(
                        contact=g.phone, branch__hotel=hotel, status=2). \
                        values('contact').annotate(sum=Sum('guest_number')). \
                        order_by('contact')
                    if ps:
                        guest_number = ps[0]['sum']
                        person_consumption = float(consumption) / guest_number
                        g.person_consumption = person_consumption

                # 消费频度(单/月)
                orders = Order.objects.filter(
                    contact=g.phone, branch__hotel=hotel, status=2). \
                    order_by('dinner_date')
                if orders:
                    count = orders.count()
                    first_date = orders[0].dinner_date
                    last_date = orders[count-1].dinner_date
                    # 计算第一次消费到今天的时间间隔
                    date_interval = 12 * (self.date.year - first_date.year) + \
                        self.date.month - first_date.month + 1
                    # 结果保留2位小数
                    order_per_month = '%.2f' % (float(count) / date_interval)
                    g.order_per_month = order_per_month

                    # 最后消费时间戳
                    last_consumption = int(time.mktime(last_date.timetuple()))
                    g.last_consumption = last_consumption

                g.save()

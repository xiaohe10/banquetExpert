import json
from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone
from webApp.models import Order, Hotel


class Command(BaseCommand):

    def handle(self, *args, **options):
        date = timezone.now().date()
        # 上个月的天数
        day = (date - timedelta(days=1)).day

        # 获得上个月的日期(年-月)
        self.month = (date - timedelta(days=1)).strftime('%Y-%m')
        # 月初
        self.first_date = date - timedelta(days=day)
        # 月末
        self.last_date = date - timedelta(days=1)
        self.count_hotel_consumption()

    def count_hotel_consumption(self):
        """统计每个酒店上个月的消费情况"""

        hotels = Hotel.objects.all()
        for hotel in hotels:
            # 获取酒店上个月的所有订单
            orders = Order.objects.filter(branch__hotel=hotel,
                                          dinner_date__gte=self.first_date,
                                          dinner_date__lte=self.last_date,
                                          status=2)
            # 总订单数
            order_number = orders.count()
            # 总人数
            guest_number = 0
            # 总消费
            consumption = 0
            # 总桌数
            desk_number = 0
            # 人均消费
            guest_consumption = 0.00
            # 桌均消费
            desk_consumption = 0.00
            for order in orders:
                guest_number += order.guest_number
                consumption += order.consumption

                if order.desks:
                    desk_list = json.loads(order.desks)
                    desk_number += len(desk_list)
            if guest_number > 0:
                guest_consumption = '%.2f' % (float(consumption) /
                                              guest_number)
            if desk_number > 0:
                desk_consumption = '%.2f' % (float(consumption) /
                                             desk_number)
            daily_consumption = hotel.month_consumptions.get_or_create(
                month=self.month)[0]

            daily_consumption.order_number = order_number
            daily_consumption.guest_number = guest_number
            daily_consumption.consumption = consumption
            daily_consumption.desk_number = desk_number
            daily_consumption.guest_consumption = guest_consumption
            daily_consumption.desk_consumption = desk_consumption
            daily_consumption.save()

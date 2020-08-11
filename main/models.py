from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.


class Table(models.Model):
    TABLE_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=TABLE_CATEGORIES)
    capacity = models.IntegerField()

    def __str__(self):
        return f'Table Number: {self.number} || Category: {dict(self.TABLE_CATEGORIES)[self.category]} || Capacity: {self.capacity}'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username} booked table number {self.table.number} from  {self.check_in.strftime("%d-%b-%Y %H:%M")} to  {self.check_out.strftime("%d-%b-%Y %H:%M")}'

    def get_table_category(self):
        table_categories = dict(self.table.TABLE_CATEGORIES)
        table_category = table_categories.get(self.table.category)
        return table_category

    def get_cancel_booking_url(self):
        return reverse_lazy('main:CancelBookingView', args=[self.pk, ])
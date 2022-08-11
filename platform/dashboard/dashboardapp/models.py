from django.db import models

# Create your models here.
"""
class PassengerStr(models.Model):
    use_dt = models.CharField(max_length=10, blank=True, null=True)
    line_num = models.CharField(max_length=20, blank=True, null=True)
    sub_sta_nm = models.CharField(max_length=50, blank=True, null=True)
    ride_pasgr_num = models.IntegerField(blank=True, null=True)
    alight_pasgr_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passenger_str'
"""
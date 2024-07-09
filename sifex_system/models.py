from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.dispatch import receiver

COURIER_STATUS_CHOICES = (
    ("ACCEPTED", "accepted"),
    ("LOADED", "loaded"),
    ("MANIFATED", "manifested"),
    ("RCS - recieved from shipper", "RCS recieved from shipper"),
    ("OFFLOADED", "offloaded"),
    ("DEPARTED", "departed"),
    ("ON TRANSIT", "on transit"),
    ("ARRIVED", "arrived"),
    ("UNDER CLEARANCE", "under clearance"),
    ("DELIVERED", "derivered"),
)

TYPE_CHOICES = (
    ("normal awb", "Normal awb"),
    ("express awb", "Express awb"),
    ("shengzen awb", "Shengzen awb"),
)

STATION_CHOICES = (
    ('CAN - Guanzhou', 'CAN - Guanzhou'),
    ('HKG - HongKong', 'HKG - HongKong'),
    ('DAR - Dar es salaam', 'DAR - Dar es salaam'),
    ('DXB - Dubai', 'DXB - Dubai'),
    ('NBO - Nairobi', 'NBO - Nairobi'),
    ('SHJ - Sharjah', 'SHJ - Sharjah'),
    ('JNB - Johanesburg', 'JNB - Johanesburg'),
    ('MCT - Muscat', 'MCT - Muscat'),
    ('BOM - Mumbai', 'BOM - Mumbai'),
    ('ADD - Addis Ababa', 'ADD - Addis Ababa'),
)

class Masterawb(models.Model):
    PAYMENT_MODE = (
        ('PP', 'pp'),
        ('cc', 'cc'),
    )
    awb = models.CharField(max_length=255, blank=True)
    order_number = models.CharField(max_length=255, null=True, blank=True)
    sender_name = models.CharField(max_length=255, blank=True)
    sender_address = models.CharField(max_length=255, blank=True)
    sender_tel = models.CharField(max_length=255, blank=True)
    sender_city = models.CharField(max_length=255, blank=True)
    sender_country = models.CharField(max_length=255, blank=True)
    receiver_name = models.CharField(max_length=255, blank=True)
    receiver_address = models.CharField(max_length=255, blank=True)
    receiver_tel = models.CharField(max_length=255, blank=True)
    receiver_city = models.CharField(max_length=255, blank=True)
    receiver_country = models.CharField(max_length=255, blank=True)
    desc = models.CharField(max_length=255, blank=True)
    freight = models.CharField(max_length=255, blank=True)
    insurance = models.CharField(max_length=255, blank=True)
    awb_pcs = models.CharField(max_length=255, blank=True)
    awb_kg = models.FloatField(max_length=255, blank=True)
    arr_pcs = models.CharField(max_length=255, null=True, blank=True)
    number_of_parcel = models.CharField(max_length=255, null=True, blank=True)
    parcel_kg = models.FloatField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    arr_kg = models.FloatField(max_length=255, null=True, blank=True)
    chargable_weight = models.CharField(max_length=255, null=True, blank=True)
    terms = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, blank=True)
    expected_arrival_date = models.DateTimeField(null=True, blank=True)
    date_received = models.DateTimeField(null=True, blank=True)
    custom_value = models.CharField(max_length=255, blank=True)
    payment_mode = models.CharField(max_length=255, choices=PAYMENT_MODE, blank=True)
    awb_type = models.CharField(max_length=255, choices=TYPE_CHOICES, null=True)
    dlv_pcs = models.CharField(max_length=255, null=True, blank=True)
    dlv_kg = models.FloatField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    height = models.CharField(max_length=255, null=True, blank=True)
    width = models.CharField(max_length=255, null=True, blank=True)
    length = models.CharField(max_length=255, null=True, blank=True)
    accepted = models.BooleanField(max_length=255, default=True)
    loaded = models.BooleanField(max_length=255, default=False)
    manifested = models.BooleanField(max_length=255, default=False)
    departed = models.BooleanField(max_length=255, default=False)
    arrived = models.BooleanField(max_length=255, default=False)
    under_clearance = models.BooleanField(max_length=255, default=False)
    delivered = models.BooleanField(max_length=255, default=False)
    released = models.BooleanField(max_length=255, default=False)
    POD = models.BooleanField(max_length=255, default=False)
    

    def __str__(self):
        return f'{self.receiver_name} {self.awb}'




class Slaveawb(models.Model):
    PAYMENT_MODE = (
        ('PP', 'pp'),
        ('cc', 'cc'),
    )
    master = models.ForeignKey(Masterawb, on_delete=models.CASCADE, null=True, blank=True, related_name="slave_master")
    master_awb = models.CharField(max_length=255, null=True)
    awb = models.CharField(max_length=255, null=True)
    order_number = models.CharField(max_length=255, null=True)
    desc = models.CharField(max_length=255, null=True,)
    freight = models.CharField(max_length=255, null=True,)
    insurance = models.CharField(max_length=255, null=True,)
    awb_pcs = models.CharField(max_length=255, null=True,)
    awb_kg = models.FloatField(max_length=255, null=True,)
    arr_pcs = models.CharField(max_length=255, null=True, blank=True)
    arr_kg = models.FloatField(max_length=255, null=True, blank=True)
    chargable_weight = models.CharField(max_length=255, null=True, blank=True)
    terms = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True,)
    expected_arrival_date = models.DateField(null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    date_received = models.DateTimeField(null=True, blank=True)
    custom_value = models.CharField(max_length=255, null=True,)
    payment_mode = models.CharField(max_length=255, null=True, choices=PAYMENT_MODE)
    awb_type = models.CharField(max_length=255, choices=TYPE_CHOICES, null=True)
    dlv_pcs = models.CharField(max_length=255, null=True, blank=True)
    dlv_kg = models.FloatField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    height = models.CharField(max_length=255, null=True, blank=True)
    width = models.CharField(max_length=255, null=True, blank=True)
    length = models.CharField(max_length=255, null=True, blank=True)
    accepted = models.BooleanField(max_length=255, default=True)
    loaded = models.BooleanField(max_length=255, default=False)
    manifested = models.BooleanField(max_length=255, default=False)
    departed = models.BooleanField(max_length=255, default=False)
    arrived = models.BooleanField(max_length=255, default=False)
    under_clearance = models.BooleanField(max_length=255, default=False)
    delivered = models.BooleanField(max_length=255, default=False)
    released = models.BooleanField(max_length=255, default=False)
    POD = models.BooleanField(max_length=255, default=False)

    def __str__(self):
        return self.desc




class Invoice(models.Model):
    customer = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    # message = models.TextField(default= "this is a default message.")
    total_amount_tzs = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_amount_usd = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.customer)
    
    def get_status(self):
        return self.status



class LineItem(models.Model):
    customer = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.TextField(null=True)
    description = models.TextField()
    quantity = models.IntegerField()
    chargable_weight = models.FloatField(null=True)
    awb_kg = models.FloatField(null=True)
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount_tz = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    amount_usd = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def __str__(self):
        return str(self.customer)











class SlaveStatus(models.Model):
    sub_awb = models.ForeignKey(Slaveawb, on_delete=models.CASCADE, null=True, related_name="slave_status")
    status = models.CharField(verbose_name="status", null=True, max_length=50)
    date = models.DateField(_("Date"), auto_now_add=True, null=True, blank=True)
    time = models.TimeField(_("Time"),auto_now=True, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    terminal = models.CharField(max_length=100, null=True, choices=STATION_CHOICES)

class MasterStatus(models.Model):
    master = models.ForeignKey(Masterawb, on_delete=models.CASCADE, null=True, related_name="master_status")
    status = models.CharField(verbose_name="status", null=True, max_length=50)
    delivered_to = models.CharField(verbose_name="delivered to", null=True, blank=True, max_length=50)
    date = models.DateField(_("Date"), auto_now_add=True, null=True, blank=True)
    time = models.TimeField(_("Time"),auto_now=True, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    terminal = models.CharField(max_length=100, null=True, choices=STATION_CHOICES)

    def __str__(self):
        return f'{self.master.sender_name} status: {self.status}'






class Quote(models.Model):
    SERVICE_CHOICES = (
    ("air transport", "air transport"),
    ("transport", "transport service"),
    ("warehouse", "Warehouse service"),
   
    )
    name = models.CharField(_("name"), max_length=50)
    email = models.EmailField(_("email"), max_length=254)
    phone = models.CharField(_("phone"), max_length=254)
    service = models.CharField(verbose_name="choose service", choices=SERVICE_CHOICES, max_length=50)
    massage = models.TextField(verbose_name="your quote massage", null=True)


    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quote_detail", kwargs={"pk": self.pk})




class SystemPreference(models.Model):
    rate = models.FloatField(null=True)
    currency = models.CharField(max_length=120, null=True)
    exchange_rate = models.FloatField(null=True)

    def __str__(self):
        return f'{self.rate}'



class Customer(models.Model):
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)



class Staff(models.Model):
    name = models.CharField(max_length=255, null=True)
    code_number = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.name}'


class Attendance(models.Model):
    in_time = models.TimeField(auto_now=True)
    out_time = models.TimeField(null=True)
    date = models.DateField(auto_now=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.staff.name}'
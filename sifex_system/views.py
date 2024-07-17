import logging
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.views import PasswordChangeView
from django.template.loader import get_template
from django.views import View
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from accounts.decorators import *
from sifex_system.forms import PasswordChangingForm
from sifex_system.models import *
from sifex_system.forms import *
from django.db.models import Sum
import datetime
from django.utils.timezone import now as timezone_now
from core.models import *
from .models import Invoice, LineItem, Customer, Attendance, Staff
import pdfkit


# for printing
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from io import BytesIO

# another approch

from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Image as PlatypusImage, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet



# Set up logging
logger = logging.getLogger(__name__)

@login_required
def register_customer(request):
    context = {}
    return render(request, 'system/customer/register.html', context)

@login_required
def display_customer(request):
    context = {}
    return render(request, 'system/customer/list.html', context)

@login_required
def console(request):
    today = datetime.date.today()
    week = today - datetime.timedelta(7)
    total_deliverd_awb = 0
    delivered_this_week = Masterawb.objects.filter(POD=True, date_received__gte=week, date_received__lte=today).order_by('-date_received')
    master_sum = delivered_this_week.aggregate(Sum('awb_kg'))
    slave_delivered_this_week = delivered_this_week.filter(POD=True, date_received__gte=week, date_received__lte=today)
    pcs = Masterawb.objects.all().order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/console/index.html', context)

@login_required
def accept_console(request):
    pcs = Masterawb.objects.filter(accepted=True)
    slave_pcs = Slaveawb.objects.filter(accepted=True).order_by('-date_received')
    context = {
        'pcs': pcs,
        'slave_pcs': slave_pcs,
    }
    return render(request, 'system/parcels/accept_parcel/index.html', context)

@login_required
def accept_loaded_console(request):
    pcs = Masterawb.objects.filter(loaded=True).order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/accept_parcel/loaded.html', context)

@login_required
def accept_manifested_console(request):
    pcs = Masterawb.objects.filter(manifested=True).order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/accept_parcel/manifested.html', context)

@login_required
def accept_arrived_console(request):
    pcs = Masterawb.objects.filter(arrived=True).order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/importer/arrived.html', context)

@login_required
def accept_underclearance_console(request):
    pcs = Masterawb.objects.filter(under_clearance=True).order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/importer/underclearance.html', context)

@login_required
def accept_release_console(request):
    pcs = Masterawb.objects.filter(released=True).order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/importer/released.html', context)

@login_required
def accept_delivered_console(request):
    pcs = Masterawb.objects.filter(invoice_paid=True).order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/importer/delivered.html', context)

@login_required
def accept_pod_console(request):
    pcs = Masterawb.objects.filter(delivered=True)
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/importer/pod.html', context)

@login_required
def parcel_update_view(request):
    # master_parcel = Masterawb.objects.get(id=pk)
    form = MasterForm()
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = MasterForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            return JsonResponse({'awb': parcel.awb, 'sender_name': parcel.sender_name, 'order_number': parcel.order_number, 'id': parcel.id})
    return render(request, 'system/parcels/accept_parcel/parcel_update.html', {
        'form': form,
    })

@login_required
def accept_parcel(request):
    form = MasterCreateForm(request.POST)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        awb = request.POST.get('awb')
        order_number = request.POST.get('order_number')
        sender_name = request.POST.get('sender_name')
        sender_address = request.POST.get('sender_address')
        sender_city = request.POST.get('sender_city')
        sender_company = request.POST.get('sender_company')
        sender_tel = request.POST.get('sender_tel')
        sender_country = request.POST.get('sender_country')
        receiver_name = request.POST.get('receiver_name')
        receiver_address = request.POST.get('receiver_address')
        receiver_company = request.POST.get('receiver_company')
        receiver_tel = request.POST.get('receiver_tel')
        receiver_city = request.POST.get('receiver_city')
        receiver_country = request.POST.get('receiver_country')
        desc = request.POST.get('desc')
        freight = request.POST.get('freight')
        insurance = request.POST.get('insurance')
        awb_pcs = request.POST.get('awb_pcs')
        awb_kg = request.POST.get('awb_kg')
        chargable_weight = request.POST.get('chargable_weight')
        terms = request.POST.get('terms')
        volume = request.POST.get('volume')
        height = request.POST.get('height')
        width = request.POST.get('width')
        length = request.POST.get('length')
        currency = request.POST.get('currency')
        date_received = request.POST.get('date_received')
        expected_arrival_date = request.POST.get('expected_arrival_date')
        custom_value = request.POST.get('custom_value')
        payment_mode = request.POST.get('payment_mode')
        awb_type = request.POST.get('awb_type')

        parcel = Masterawb.objects.create(
            awb=awb, 
            order_number=order_number,
            sender_name=sender_name,
            sender_tel=sender_tel,
            awb_type=awb_type,
            sender_address=sender_address,
            sender_city=sender_city,
            sender_company=sender_company,
            sender_country=sender_country,
            receiver_name=receiver_name,
            receiver_tel=receiver_tel,
            receiver_address=receiver_address,
            receiver_city=receiver_city,
            receiver_company=receiver_company,
            receiver_country=receiver_country,
            desc=desc,
            freight=freight,
            insurance=insurance,
            awb_pcs=awb_pcs,
            awb_kg=awb_kg,
            chargable_weight=chargable_weight,
            terms=terms,
            volume=volume,
            height=height,
            width=width,
            length=length,
            user=request.user,
            currency=currency,
            date_received=date_received,
            expected_arrival_date=expected_arrival_date,
            custom_value=custom_value,
            payment_mode=payment_mode,
            accepted=True,
        )
        awb_status = MasterStatus.objects.create(master=parcel, user=request.user, status='accepted', date=datetime.datetime.now().date(), time=datetime.datetime.now().time(), terminal='CAN - Guanzhou')
        return JsonResponse({
            'id': parcel.id,
            'awb': parcel.awb,
            'order_number': parcel.order_number,
            'sender_name': parcel.sender_name,
            'sender_tel': parcel.sender_tel,
            'sender_address': parcel.sender_address,
            'sender_city': parcel.sender_city,
            'sender_company': parcel.sender_company,
            'sender_country': parcel.sender_country,
            'receiver_name': parcel.receiver_name,
            'receiver_address': parcel.receiver_address,
            'receiver_tel': parcel.receiver_tel,
            'receiver_city': parcel.receiver_city,
            'receiver_company': parcel.receiver_company,
            'receiver_country': parcel.receiver_country,
            'desc': parcel.desc,
            'freight': parcel.freight,
            'insurance': parcel.insurance,
            'awb_pcs': parcel.awb_pcs,
            'awb_type': parcel.awb_type,
            'awb_kg': parcel.awb_kg,
            'chargable_weight': parcel.chargable_weight,
            'terms': parcel.terms,
            'volume': parcel.volume,
            'width': parcel.width,
            'height': parcel.height,
            'length': parcel.length,
            'currency': parcel.currency,
            'date_received': parcel.date_received,
            'expected_arrival_date': parcel.expected_arrival_date,
            'custom_value': parcel.custom_value,
            'payment_mode': parcel.payment_mode,
        })

@login_required
def accept_form_view(request):
    form = MasterCreateForm()
    context = {'form': form}
    return render(request, 'system/parcels/accept_parcel/accept.html', context)

@login_required
def add_parcel(request):
    if request.method == "POST":
        id = request.POST.get('id')
        parcel_id = Masterawb.objects.get(id=id)
        desc = request.POST.get('desc')
        awb = request.POST.get('awb')
        order_number = request.POST.get('order_number')
        freight = request.POST.get('freight')
        insurance = request.POST.get('insurance')
        awb_pcs = request.POST.get('awb_pcs')
        awb_kg = request.POST.get('awb_kg')
        chargable_weight = request.POST.get('chargable_weight')
        terms = request.POST.get('terms')
        awb_type = request.POST.get('awb_type')
        volume = request.POST.get('volume')
        height = request.POST.get('height')
        width = request.POST.get('width')
        length = request.POST.get('length')
        currency = request.POST.get('currency')
        date_received = request.POST.get('date_received')
        expected_arrival_date = request.POST.get('expected_arrival_date')
        custom_value = request.POST.get('custom_value')
        payment_mode = request.POST.get('payment_mode')

        parcel = Slaveawb.objects.create(
            master=parcel_id,
            desc=desc,
            awb_type=awb_type,
            awb=awb,
            order_number=order_number,
            freight=freight,
            insurance=insurance,
            awb_pcs=awb_pcs,
            awb_kg=awb_kg,
            chargable_weight=chargable_weight,
            terms=terms,
            volume=volume,
            user=request.user,
            height=height,
            width=width,
            length=length,
            currency=currency,
            date_received=date_received,
            expected_arrival_date=expected_arrival_date,
            custom_value=custom_value,
            payment_mode=payment_mode,
        )

        sub_parcels = Slaveawb.objects.filter(master=id, user=request.user, date_received=date_received)
        awb_status = SlaveStatus.objects.create(sub_awb=parcel, user=request.user, status='accepted', date=datetime.datetime.now().date(), time=datetime.datetime.now().time(), terminal='CAN - Guanzhou')
        return JsonResponse({
            'id': parcel.id,
            'desc': parcel.desc,
            'awb': parcel.awb,
            'order_number': parcel.order_number,
            'freight': parcel.freight,
            'insurance': parcel.insurance,
            'awb_pcs': parcel.awb_pcs,
            'awb_kg': parcel.awb_kg,
            'chargable_weight': parcel.chargable_weight,
            'terms': parcel.terms,
            'volume': parcel.volume,
            'width': parcel.width,
            'height': parcel.height,
            'length': parcel.length,
            'currency': parcel.currency,
            'date_received': parcel.date_received,
            'expected_arrival_date': parcel.expected_arrival_date,
            'custom_value': parcel.custom_value,
            'payment_mode': parcel.payment_mode,
        })

@login_required
def parcel_view(request, pk):
    pc = Masterawb.objects.get(id=pk)
    master_status = pc.master_status.all()
    slave_pcs = pc.slave_master.filter(accepted=True)
    form = MasterForm(instance=pc)
    context = {
        'form': form,
        'master_awb': pc,
        'master_status': master_status,
        'slave_pcs': slave_pcs,
    }
    return render(request, 'system/parcels/importer/view.html', context)

@login_required
def parcel_import(request):
    pcs = Masterawb.objects.filter(departed=True).order_by('-date_received')
    context = {
        'pcs': pcs,
    }
    return render(request, 'system/parcels/importer/import.html', context)

@login_required
def new_staff(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        accountance = request.POST.get('accountance')
        acceptance = request.POST.get('acceptance')
        delivery_man = request.POST.get('delivery_man')
        management = request.POST.get('management')
        importer = request.POST.get('importer')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.success(request, 'username exist')
            return redirect('new_staff')
            return render(request, 'system/users/new_staff.html')

        if acceptance == "on":
            acceptance = True
        else:  
            acceptance = False

        if accountance == "on":
            accountance = True
        else:  
            accountance = False
            
        if importer == "on":
            importer = True
        else:  
            importer = False

        if delivery_man == "on":
            delivery_man = True
        else:  
            delivery_man = False

        if management == "on":
            management = True
        else:  
            management = False
        
        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                acceptance=acceptance,
                accountance=accountance,
                importer=importer,
                delivery_man=delivery_man,
                management=management,
                password=password1,
            )
            messages.success(request, f'{user.username} account created successfully')
            return redirect('new_staff')
            return render(request, 'system/users/new_staff.html')
        else:
            messages.success(request, f'enter the same password as before')
            return redirect('new_staff')
            return render(request, 'system/users/new_staff.html')
    form = UserRoleForm()
    return render(request, 'system/users/new_staff.html', {'form': form})

class PasswordChange(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('success_password')
    template_name="system/users/password_change.html"

@login_required
def changepassword(request):
    return render(request, '')

@login_required
def password_success(request):
    return render(request, 'partials/messages/password_success.html')

@login_required
def add_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id)
            awb.accepted = False 
            awb.loaded = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')

@login_required
def add_sub_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')

        for id in awb_list:
            awb = Masterawb.objects.get(pk=id)
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status='accepted')
        return redirect('accept_console')

@login_required
def manifested_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.loaded = False 
            awb.manifested = True
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')

@login_required
def departed_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.manifested = False 
            awb.departed = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')

@login_required
def arrived_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.departed = False
            awb.arrived = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')

@login_required
def underclearance_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.arrived = False
            awb.under_clearance = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')

@login_required
def released_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.under_clearance = False
            awb.released = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')



@login_required
def payment_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.released = False
            awb.account = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')



@login_required
def pod_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        delivered_to = request.POST.get('delivered_to')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.delivered = False
            awb.POD = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, delivered_to=delivered_to, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')



@login_required
def delivered_master_status(request):
    if request.method == 'POST':
        awb_list = request.POST.getlist('id[]')
        status = request.POST.get('status')
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        terminal = request.POST.get('terminal')
        for id in awb_list:
            awb = Masterawb.objects.get(pk=id) 
            awb.invoice_paid = False
            awb.delivered = True 
            awb.save()
            awb_status = MasterStatus.objects.create(master=awb, user=request.user, status=status, date=date, time=time, note=note, terminal=terminal)
            messages.success(request, f'{awb_status.master.sender_name} status updated successfully')
        return redirect('accept_console')

@login_required
def total_master_awb_kg(request):
    today = datetime.date.today()
    month = today - datetime.timedelta(7)
    master_awbs = Masterawb.objects.filter(date_received__gte=month, date_received__lte=today, accepted=True)
   
    finalrep = {}

    def get_awb_type(master_awb):
        return master_awb.awb_type
    awb_type_list = list(set(map(get_awb_type, master_awbs)))

    def get_awb_kg(awb_type):
        awb_kg = 0
        filter_by_awb_type = master_awbs.filter(awb_type=awb_type)
        for item in filter_by_awb_type:
            awb_kg += item.awb_kg
            return awb_kg
    for x in master_awbs:
        for y in awb_type_list:
            finalrep[y] = get_awb_kg(y)
    return JsonResponse({'awb_type_data': finalrep}, safe=False)

@login_required
def total_month_master_awb_kg(request):
    today = datetime.date.today()
    month = today - datetime.timedelta(30)
    master_awbs = Masterawb.objects.filter(date_received__gte=month, date_received__lte=today, POD=True)
    finalrep = {}

    def get_awb_type(master_awb):
        return master_awb.awb_type
    awb_type_list = list(set(map(get_awb_type, master_awbs)))

    def get_awb_kg(awb_type):
        awb_kg = 0
        filter_by_awb_type = master_awbs.filter(awb_type=awb_type)
        for item in filter_by_awb_type:
            awb_kg += item.awb_kg
            return awb_kg
    for x in master_awbs:
        for y in awb_type_list:
            finalrep[y] = get_awb_kg(y)
    return JsonResponse({'awb_type_data': finalrep}, safe=False)

@login_required
def update_slave_arr(request, id):
    if request.method == 'POST':
        slave_awb = Slaveawb.objects.get(pk=id)
        arr_pcs = request.POST.get('arr_pcs')
        arr_kg = request.POST.get('arr_kg')

        slave_awb.arr_pcs = arr_pcs
        slave_awb.arr_kg = arr_kg
        slave_awb.save()
        return redirect('parcel_view', slave_awb.master.id)

@login_required
def update_master_arr(request, id):
    if request.method == 'POST':
        master_awb = Masterawb.objects.get(pk=id)
        arr_pcs = request.POST.get('arr_pcs')
        arr_kg = request.POST.get('arr_kg')

        master_awb.arr_pcs = arr_pcs
        master_awb.arr_kg = arr_kg
        master_awb.save()
        return redirect('parcel_view', master_awb.id)

@login_required
def update_slave_dlv(request, id):
    if request.method == 'POST':
        slave_awb = Slaveawb.objects.get(pk=id)
        arr_pcs = request.POST.get('arr_pcs')
        arr_kg = request.POST.get('arr_kg')

        slave_awb.arr_pcs = arr_pcs
        slave_awb.arr_kg = arr_kg
        slave_awb.save()
        return redirect('parcel_view', slave_awb.master.id)

@login_required
def update_master_dlv(request, id):
    if request.method == 'POST':
        master_awb = Masterawb.objects.get(pk=id)
        dlv_pcs = request.POST.get('dlv_pcs')
        dlv_kg = request.POST.get('dlv_kg')

        master_awb.dlv_pcs = dlv_pcs
        master_awb.dlv_kg = dlv_kg
        master_awb.save()
        return redirect('parcel_view', master_awb.id)

@login_required
def blog_create_view(request):
    context = {}
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        photo = request.FILES['photo']
        if not title:
            messages.error(request, f'title is required')
            return redirect('blog_create')
        if not body:
            messages.error(request, f'body is required')
            return redirect('blog_create')
        blog = Post.objects.create(user=request.user, title=title, body=body, photo=photo)
        messages.success(request, f'{blog.title} created successfully!')
        return redirect('blogs')
    return render(request, 'system/blog/create.html', context)

@login_required
def blog_view(request):
    blogs = Post.objects.all()
    context = {
        'blogs': blogs,
    }
    return render(request, 'system/blog/index.html', context)

@login_required
def quotes_view(request):
    quotes = Quote.objects.all()
    context = {
        'quotes': quotes,
    }
    return render(request, 'system/quotes/index.html', context)

@login_required
def users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'system/users/index.html', context)

@login_required
def delete_user(request, id):
    user = User.objects.get(pk=id)
    user.delete()
    messages.success(request, f'{user.username} deleted successfully')
    return redirect('users')

def upload_quote_bg(request):
    if request.method == "POST":
        quote_bg = request.POST.get('quote_bg')
    context = {}
    return render(request, '_.html', context)

def upload_service_bg(request):
    if request.method == "POST":
        service_bg = request.POST.get('service_bg')
    context = {}
    return render(request, '_.html', context)

def upload_about_bg(request):
    if request.method == "POST":
        about_bg = request.POST.get('about_bg')
    context = {}
    return render(request, '_.html', context)

@login_required
def on_edit_add_parcel(request):
    if request.method == "POST":
        id = request.POST.get('id')
        master_awb = Masterawb.objects.get(id=id)
        desc = request.POST.get('desc')
        awb = request.POST.get('awb')
        order_number = request.POST.get('order_number')
        freight = request.POST.get('freight')
        insurance = request.POST.get('insurance')
        awb_pcs = request.POST.get('awb_pcs')
        awb_kg = request.POST.get('awb_kg')
        chargable_weight = request.POST.get('chargable_weight')
        terms = request.POST.get('terms')
        awb_type = request.POST.get('awb_type')
        volume = request.POST.get('volume')
        height = request.POST.get('height')
        width = request.POST.get('width')
        length = request.POST.get('length')
        currency = request.POST.get('currency')
        date_received = request.POST.get('date_received')
        expected_arrival_date = request.POST.get('expected_arrival_date')
        custom_value = request.POST.get('custom_value')
        payment_mode = request.POST.get('payment_mode')

        parcel = Slaveawb.objects.create(
            master=master_awb,
            master_awb=master_awb.awb,
            desc=desc,
            awb_type=awb_type,
            awb=awb,
            order_number=order_number,
            freight=freight,
            insurance=insurance,
            awb_pcs=awb_pcs,
            awb_kg=awb_kg,
            chargable_weight=chargable_weight,
            terms=terms,
            volume=volume,
            height=height,
            width=width,
            length=length,
            currency=currency,
            date_received=date_received,
            expected_arrival_date=expected_arrival_date,
            custom_value=custom_value,
            payment_mode=payment_mode,
        )

        sub_parcels = Slaveawb.objects.filter(master=id, date_received=date_received)
        awb_status = SlaveStatus.objects.create(sub_awb=parcel, status='accepted', date=datetime.datetime.now().date(), time=datetime.datetime.now().time(), terminal='CAN - Guanzhou')
        return redirect('parcel_view', master_awb.id)

@login_required
def export_masterawb_pdf_label(request, pk):
    awb = Masterawb.objects.get(id=pk)
    context = {'awb': awb}
    return render(request, 'system/pdf/export.html', context)

def on_edit_add_parcel_view(request, pk):
    form = SlaveCreateForm()
    awb_id = Masterawb.objects.get(id=pk)
    ctx = {'master_awb_id': awb_id, 'form': form}
    return render(request, 'system/parcels/importer/add.html', ctx)

class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices": invoices,
        }
        return render(self.request, 'invoice/invoice-list.html', context)
    
    def post(self, request):
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)

        for invoice in invoices:
            awb = invoice.awb
            if update_status_for_invoices == 0:
                invoice.status = False
            else:
                invoice.status = True
                awb.account = False
                awb.invoice_paid = True
                awb.save()
                MasterStatus.objects.create(
                    master=awb, 
                    user=request.user, 
                    status='invoice paid', 
                    date=timezone_now().date(), 
                    time=timezone_now().time(), 
                    terminal='DAR - Dar es salaam',  # Replace this with actual terminal information if needed
                    note='Invoice marked as paid'
                )
            invoice.save()

        return redirect('invoice-list')

@login_required
def createInvoice(request, pk):
    """
    Invoice Generator page. It will have functionality to create new invoices.
    This view is protected; only admin has the authority to read and make changes here.
    """
    awb = Masterawb.objects.get(id=pk)
    heading_message = 'Formset Demo'
    if request.method == 'POST':
        customer = request.POST.get('customer')
        customer_phone = request.POST.get('customer_phone')
        origin = request.POST.get('origin')
        billing_address = request.POST.get('billing_address')
        date = request.POST.get('date')
        due_date = request.POST.get('due_date')
        invoice = Invoice.objects.create(
            customer=customer,
            awb=awb,
            origin=origin,
            customer_phone=customer_phone,
            billing_address=billing_address,
            date=date,
            due_date=due_date,
            user=request.user
        )

        total_tz = 0
        total_usd = 0

        user_preferences = SystemPreference.objects.all()[:1]
        exchange_rates = 0
        for exch in user_preferences:
            exchange_rates = exch.exchange_rate

        service = request.POST.get('service')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        chargable_weight = request.POST.get('chargable_weight')
        rate = request.POST.get('rate')
        if service and description and quantity and rate and chargable_weight:
            amount_tz = float(rate) * float(chargable_weight) * float(exchange_rates)
            total_tz += amount_tz
            amount_usd = float(rate) * float(chargable_weight)
            total_usd += amount_usd
            LineItem.objects.create(
                customer=invoice,
                service=service,
                description=description,
                tracking_key=awb.awb,  # Assuming tracking_key is a field in Masterawb
                quantity=quantity,
                chargable_weight=chargable_weight,
                rate=rate,
                amount_tz=amount_tz,
                amount_usd=amount_usd
            )
            invoice.total_amount_tzs = total_tz
            invoice.total_amount_usd = total_usd
            invoice.save()

        try:
            generate_PDF(request, id=invoice.id)
        except Exception as e:
            print(f"********{e}********")

        return redirect('invoice-list')
    
    context = {
        "title": "Sifex Invoice Generator",
        "awb": awb,
    }
    return render(request, 'invoice/invoice-create.html', context)

def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "SIFEX COURIER COMPANY LIMITED",
            "address": """Dar es salaam, Ilala, 
            Kipawa street-Plot No 236 Zakhem Plaza
            1st Floor
            """,
            "phone": "(+255) 688 930 963",
            "TIN": "142-996-014",
        },
        "invoice_id": invoice.id,
        "invoice_origin": invoice.origin,
        "invoice_total_usd": invoice.total_amount_usd,
        "invoice_total_tzs": invoice.total_amount_tzs,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "lineitem": lineitem,

    }
    return render(request, 'invoice/pdf_template.html', context)

def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice-detail', args=[id])), False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response

def change_status(request):
    return redirect('invoice-list')

def view_404(request, *args, **kwargs):
    return redirect('invoice-list')

@login_required
def delete_awb(request, id):
    awb = Masterawb.objects.get(pk=id)
    awb.delete()
    messages.success(request, f'{awb.receiver_name} awb deleted successfully')
    return redirect('accept_console')

@login_required
# @allowed_user
def delete_invoice(request, id):
    invoice = Invoice.objects.get(pk=id)
    invoice.delete()
    messages.success(request, f'invoice {invoice.customer} deleted successfully')
    return redirect('invoice-list')

def awb_edit(request, pk):
    if request.method == 'POST':
        master_awb = Masterawb.objects.get(id=pk)
        awb = request.POST.get('awb')
        order_number = request.POST.get('order_number')
        sender_name = request.POST.get('sender_name')
        sender_address = request.POST.get('sender_address')
        sender_city = request.POST.get('sender_city')
        sender_tel = request.POST.get('sender_tel')
        sender_country = request.POST.get('sender_country')
        receiver_name = request.POST.get('receiver_name')
        receiver_address = request.POST.get('receiver_address')
        receiver_tel = request.POST.get('receiver_tel')
        receiver_city = request.POST.get('receiver_city')
        receiver_country = request.POST.get('receiver_country')
        desc = request.POST.get('desc')
        freight = request.POST.get('freight')
        insurance = request.POST.get('insurance')
        awb_pcs = request.POST.get('awb_pcs')
        awb_kg = request.POST.get('awb_kg')
        chargable_weight = request.POST.get('chargable_weight')
        terms = request.POST.get('terms')
        volume = request.POST.get('volume')
        height = request.POST.get('height')
        width = request.POST.get('width')
        length = request.POST.get('length')
        currency = request.POST.get('currency')
        date_received = request.POST.get('date_received')
        expected_arrival_date = request.POST.get('expected_arrival_date')
        custom_value = request.POST.get('custom_value')
        payment_mode = request.POST.get('payment_mode')
        awb_type = request.POST.get('awb_type')

        master_awb.awb = awb
        master_awb.awb_type = awb_type
        master_awb.order_number = order_number
        master_awb.sender_name = sender_name
        master_awb.sender_address = sender_address
        master_awb.sender_tel = sender_tel
        master_awb.sender_country = sender_country
        master_awb.sender_city = sender_city
        master_awb.receiver_name = receiver_name
        master_awb.receiver_country = receiver_country
        master_awb.receiver_city = receiver_city
        master_awb.receiver_tel = receiver_tel
        master_awb.currency = currency
        master_awb.date_received = date_received
        master_awb.expected_arrival_date = expected_arrival_date
        master_awb.desc = desc
        master_awb.freight = freight
        master_awb.insurance = insurance
        master_awb.awb_kg = awb_kg
        master_awb.awb_pcs = awb_pcs
        master_awb.chargable_weight = chargable_weight
        master_awb.terms = terms
        master_awb.height = height
        master_awb.width = width
        master_awb.length = length
        master_awb.volume = volume
        master_awb.payment_mode = payment_mode
        master_awb.save()
        return redirect('parcel_view', master_awb.id)

def invoice_generation(request):
    pcs = Masterawb.objects.filter(account=True)
    exchange_rate = SystemPreference.objects.first()
    ctx = {
        'pcs': pcs,
        'exchange_rate': exchange_rate,
    }
    return render(request, 'invoice/generate_invoice.html', ctx)

def list_of_delivered_awb(request):
    return render(request, 'system/reports/delivered-goods.html', {})

def list_of_undelivered_awb(request):
    return render(request, 'system/reports/undelivered-goods.html', {})

def list_of_paid_awb(request):
    return render(request, 'system/reports/paid-goods.html', {})

def list_of_unpaid_awb(request):
    return render(request, 'system/reports/unpaid-goods.html', {})

@login_required
def add_customer(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        if not name:
            messages.error(request, 'Name field is required')
            return render(request, 'system/customer/create.html', context)
        if not phone:
            messages.error(request, 'Phone number field is required')
            return render(request, 'system/customer/create.html', context)
        customer = Customer.objects.create(name=name, user=request.user, phone=phone, address=address, city=city, country=country)
        messages.success(request, f'Customer {customer.name} added successfully')
        return redirect('customers-list')
    return render(request, 'system/customer/create.html', context)

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'system/customer/index.html', {'customers': customers})

def delivered_report(request):
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        pcs = Masterawb.objects.filter(date_received__gte=date_from, date_received__lte=date_to, POD=True)
    context = {'pcs': pcs}
    return render(request, 'system/reports/dlv-reports.html', context)

def undelivered_report(request):
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        pcs = Masterawb.objects.filter(date_received__gte=date_from, date_received__lte=date_to, delivered=True)
    context = {'pcs': pcs}
    return render(request, 'system/reports/undlv-reports.html', context)

def paid_report(request):
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        pcs = Masterawb.objects.filter(date_received__gte=date_from, date_received__lte=date_to, delivered=True)
    context = {'pcs': pcs}
    return render(request, 'system/reports/paid-reports.html', context)

def unpaid_report(request):
    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        pcs = Masterawb.objects.filter(date_received__gte=date_from, date_received__lte=date_to, delivered=True)
    context = {'pcs': pcs}
    return render(request, 'system/reports/unpaid-reports.html', context)

def check_staff(request):
    return render(request, 'system/attendance/check_staff.html')

def check_staff_by_code(request):
    return render(request, 'system/attendance/check_staff_by_code.html')

def check_staff_id(request):
    if request.method == 'POST':
        staffcode = request.POST.get('staffcode')
        result = None
        if Staff.objects.filter(code_number=staffcode).exists():
            staff = Staff.objects.get(code_number=staffcode)
            item = {
                'pk': staff.pk,
                'code_number': staff.code_number,
                'name': staff.name,
            }
            data = item
            result = data
        else:
            result = 'not found'
        return JsonResponse({'data': result})
    return JsonResponse({})

from django.utils import timezone

now = timezone.now()
date = now.date()

def mark_attendance_in(request):
    if request.method == "POST":
        staffcode = request.POST.get('staffcode')
        staff = Staff.objects.get(code_number=staffcode)
        result = None 
        print(staffcode)
        # CHECK IF MEMBER EXISTS AND MARK OUT MEMBER ELSE MARK OUT
        if Attendance.objects.filter(date=date, staff=staff).exists():
            attendances = Attendance.objects.filter(staff=staff)
            for attendance in attendances:
                if attendance.out_time:
                    result = f'Sorry already marked out'
                    return JsonResponse({'data': result})
                else:
                    attendance.out_time = now.time()
                    attendance.present = True
                    attendance.save()
                    result = 'signed out successfully'
                    return JsonResponse({'data': result})
        else:
            attendance = Attendance.objects.create(staff=staff, in_time=now.time())
            item = {
                'pk': attendance.pk,
                'in_time': attendance.in_time,
                'date': attendance.date,
                'staff': staff.name,
            }
            data = item
            result = data
            return JsonResponse({'data': result})
    return JsonResponse({})

def mark_attendance_out(request):
    return render(request, 'system/attendance/take_attendance.html', {})

def filter_attendance(request):
    return render(request, 'system/attendance/filter.html', {})

def list_attendance(request):
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    attendances = Attendance.objects.filter(date__gte=date_from, date__lte=date_to)
    return render(request, 'system/attendance/index.html', {'attendances': attendances})

def register_staff(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        company = request.POST.get('company')
        if not name:
            messages.error(request, 'Name field is required')
            return render(request, 'system/staff/create.html', context)
        if not phone:
            messages.error(request, 'Phone number field is required')
            return render(request, 'system/staff/create.html', context)
        staff = Staff.objects.create(name=name, phone=phone, address=address, city=city, country=country, designation=designation, department=department, company=company)
        messages.success(request, f'Customer {customer.name} added successfully')
        return redirect('customers-list')
    return render(request, 'system/staff/create.html', {})




@login_required
def print_label(request, pk):
    awb = get_object_or_404(Masterawb, pk=pk)

    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=(4 * inch, 6 * inch))  # Size for Zebra and thermal printers

    # Draw the content of the label
    p.setFont("Helvetica", 10)
    
    # Set line width for borders
    p.setLineWidth(1)
    
    # Draw border around the label
    p.rect(10, 10, 4 * inch - 20, 6 * inch - 20)  # Draw border with margins
    
    # Add the logo image
    logo_path = os.path.join(settings.STATIC_ROOT, 'assets/img/sifex/logo.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 20, 330, width=0.8 * inch, height=0.5 * inch, mask='auto')
    else:
        p.drawString(20, 330, "Logo not found")
    
    # Add the barcode
    barcode_value = awb.awb
    barcode = code128.Code128(barcode_value, barHeight=10*mm, barWidth=0.5*mm)
    barcode.drawOn(p, 20, 390)
    p.drawString(100, 380, barcode_value)

    # Add horizontal lines for separation
    # y_positions = [450, 430, 410, 390, 370, 350, 330, 310, 290, 270, 250, 230, 210, 190, 170, 150]
    # for y in y_positions:
    #     p.line(20, y, 4 * inch - 20, y)
    
    # Add sender and receiver information
    info = [
        ("Sender Name:", awb.sender_name or ''),
        ("Sender Address:", awb.sender_address or ''),
        ("Sender Company:", awb.sender_company or ''),
        ("Sender Phone:", awb.sender_tel or ''),
        ("Receiver Name:", awb.receiver_name or ''),
        ("Receiver Address:", awb.receiver_address or ''),
        ("Receiver Company:", awb.receiver_company or ''),
        ("Receiver Phone:", awb.receiver_tel or ''),
        ("Payment type:", awb.payment_mode or ''),
        ("Number of pieces:", str(awb.awb_pcs) or ''),
        ("Chargeable weight:", f"{awb.awb_kg} kg" if awb.awb_kg else ''),
        ("Volume:", awb.volume or ''),
        ("Desc:", awb.desc or ''),
        ("", ''),
        ("RECEIVER'S SIGNATURE:",  '')
    ]

    y = 300
    for label, value in info:
        p.drawString(20, y, label)
        p.drawString(130, y, value)
        y -= 20

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="label_{awb.awb}.pdf"'

    return response




@login_required
def search_parcel(request):
    query = request.GET.get('query')
    if query:
        parcels = Masterawb.objects.filter(
            Q(awb__icontains=query) | Q(order_number__icontains=query)
        )
        if parcels.exists():
            return redirect('search_found', pk=parcels.first().id)
        else:
            logger.info(f"No parcel found for query: {query}")
            return render(request, 'system/parcels/search/search_results.html', {'error': 'No parcel found.'})
    else:
        logger.info("No query provided.")
        return render(request, 'system/parcels/search/search_results.html', {'error': 'Please enter a search term.'})



@login_required
def search_found(request, pk):
    pc = Masterawb.objects.get(id=pk)
    master_status = pc.master_status.all()
    slave_pcs = pc.slave_master.filter(accepted=True)
    form = MasterForm(instance=pc)
    context = {
        'form': form,
        'master_awb': pc,
        'master_status': master_status,
        'slave_pcs': slave_pcs,
    }
    return render(request, 'system/parcels/search/search_found.html', context)
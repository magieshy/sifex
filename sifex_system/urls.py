from django.urls import path
from .views import *
from accounts.views import *


urlpatterns = [
    path('', console, name="console"),

    # printing
    path('print_label/<int:pk>/', print_label, name='print_label'),

    path('accept_console/', accept_console, name="accept_console"),
    path('accept_loaded_console/', accept_loaded_console, name="accept_loaded_console"),
    path('accept_manifested_console/', accept_manifested_console, name="accept_manifested_console"),
    path('parcel_import/', parcel_import, name="parcel_import"),
    path('accept_arrived_console/', accept_arrived_console, name="accept_arrived_console"),
    path('accept_release_console/', accept_release_console, name="accept_release_console"),
    path('accept_pod_console/', accept_pod_console, name="accept_pod_console"),
    path('accept_underclearance_console/', accept_underclearance_console, name="accept_underclearance_console"),
    path('accept_delivered_console/', accept_delivered_console, name="accept_delivered_console"),
    path('accept/', accept_parcel, name="accept_parcel"),
    path('accept/<str:pk>/', parcel_view, name="parcel_view"),
    path('save_parcel/', add_parcel, name="save_parcel"),
    path('accept_form/', accept_form_view, name="accept_form_view"),
    path('new_staff/', new_staff, name="new_staff"),
    path('password_success/', password_success, name="password_success"),
    path('password_change/', PasswordChange.as_view(), name="password_change"),
    path('loaded/', add_master_status, name="load_master_status"),
    path('manifested/', manifested_master_status, name="manifested_master_status"),
    path('departed/', departed_master_status, name="departed_master_status"),
    path('arrived/', arrived_master_status, name="arrived_master_status"),
    path('underclearance/', underclearance_master_status, name="underclearance_master_status"),
    path('delivered/', delivered_master_status, name="delivered_master_status"),
    path('released/', released_master_status, name="released_master_status"),
    path('pod/', pod_master_status, name="pod_master_status"),
    path('loaded/sub/', add_sub_status, name="load_sub_status"),
    path('manifested/sub/', add_sub_status, name="load_sub_status"),

    path('total_master_awb_kg/', total_master_awb_kg, name="total_master_awb_kg"),
    path('total_month_master_awb_kg/', total_month_master_awb_kg, name="total_month_master_awb_kg"),

    path('update_master_arr/<int:id>/', update_master_arr, name="update_slave_arr"),
    path('update_master_dlv/<int:id>/', update_master_dlv, name="update_master_dlv"),

    path('blog_create/', blog_create_view, name="blog_create"),
    path('blogs/', blog_view, name="blogs"),
    path('quotes/', quotes_view, name="quotes"),
    path('users/', users, name="users"),
    path('delete_user/<int:id>/', delete_user, name="delete-user"),

    path('awb_edit/<int:pk>/', awb_edit, name="awb-edit"),


    path('add_awb/<int:pk>/', on_edit_add_parcel_view, name="on_edit_add_awb_view"),
    path('save_awb/', on_edit_add_parcel, name="on_edit_save_awb"),
    path('export/pdf/<int:pk>/', export_masterawb_pdf_label, name="export-master-awb-pdf-label"),
    path('delete_awb/<int:id>/', delete_awb, name="delete-awb"),
    path('delete_invoice/<int:id>/', delete_invoice, name="delete-invoice"),


    # INVOICE APP

    path('invoices/', InvoiceListView.as_view(), name="invoice-list"),
    path('create/<int:pk>/', createInvoice, name="invoice-create"),
    path('invoice-detail/<id>', view_PDF, name='invoice-detail'),
    path('invoice-download/<id>', generate_PDF, name='invoice-download'),
    path('generate-invoice/', invoice_generation, name="generate-invoice"),

    #CUSTOMER APP
    path('add-customer/', add_customer, name="add-customer"),
    path('customers', customer_list, name="customers-list"),

    # REPORT APP
    path('deliverd-goods/', list_of_delivered_awb, name="delivered-goods"),
    path('undeliverd-goods/', list_of_undelivered_awb, name="undelivered-goods"),
    path('paid-goods/', list_of_paid_awb, name="paid-goods"),
    path('unpaid-goods/', list_of_unpaid_awb, name="unpaid-goods"),

    path('delivered_report', delivered_report, name="delivered_report"),
    path('undelivered_report', undelivered_report, name="undelivered_report"),
    path('paid_report', paid_report, name="paid_report"),
    path('unpaid_report', unpaid_report, name="unpaid_report"),


    # ATTENDANCE APP
    path('check-staff', check_staff, name="check-staff"),
    path('check-staff-by-code', check_staff_by_code, name="check-staff-by-code"),
    path('check-staff-id/', check_staff_id, name="check-staff-id"),
    path('mark-attendance-in/', mark_attendance_in, name="mark-attendance-in"),
    path('mark-attendance-out/', mark_attendance_out, name="mark-attendance-out"),
    path('filter-attendance', filter_attendance, name="filter-attendance"),
    path('attendance', list_attendance, name="attendance"),

]
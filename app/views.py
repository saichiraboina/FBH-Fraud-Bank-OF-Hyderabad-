from django.shortcuts import render,redirect,HttpResponse
from . models import Account
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random

# Create your views here.
def index(request):
    return render(request,'index.html')
def create(request):
    if request.method == 'POST':
        name = request.POST['name']
        dob = request.POST['dob']
        aadhar = request.POST['aadhar']
        pan = request.POST['pan']
        mobile = request.POST['mobile']
        address = request.POST['address']
        email =request.POST['email']
        print(name,dob,aadhar,pan,mobile,address)
        Account.objects.create(Name = name ,DOB = dob ,Aadhar = aadhar, Pan = pan, Mobile = mobile ,Address = address, email = email)
        print("Succefully account Created...")
        send_mail(f"hello {name} ,Thank you for Creating Account in Our Bank",#subject 
        "FBH Fraud Bank Of Hyderabad,\n Welcome to Family Of Our Bank,\n We Are Happy For It \n, Regards \n Manager(DJD-E1)\n Thank You ****!" #body
        ,settings.EMAIL_HOST_USER,[email],fail_silently=False)
        messages.success(request,"Account is  Successfully Created.... 💐💐")
        print("Sent Successfully...")
    return render(request,'create.html')

def pin_gen(request):
    if request.method=='POST':
        otp = random.randint(100000,999999)
        acc = request.POST.get('acc')
        data = Account.objects.get( Account_no = acc )
        email =data.email
        send_mail(f"Hello {data.Name}",
        f"FBH Bank of hyd \n the OTP is {otp} \n Please Share OTP Only My Employees Not With The Other Scammers,It is Kind Request \n Regards \n Manager(DJD-E1)\n Thank You ****!" #body
        ,settings.EMAIL_HOST_USER,[email],fail_silently=False
        )
        print("Sent Successfully...")
        data.OTP = otp
        data.save()
        return redirect("OTP")

    return render(request,'pin.html')

def valid_otp(request):
    if request.method == 'POST':
        acc = request.POST['acc']
        otp = int(request.POST['otp'])
        pin1 = int(request.POST['pin1'])
        pin2 = int(request.POST['pin2'])
        try:
            data = Account.objects.get( Account_no = acc )
        except:
            return HttpResponse("Invalid Account Number...")
        if pin1 == pin2:
            if data.OTP == otp:
                data.Pin = pin2
                data.save()
                send_mail(f"Hello {data.Name} PIN GENERATION ",
                    f"FBH fraud bank of hyd .\n We are happy to scam You \n You Successfully Generated Pin,we are happy to inform that we know Your otp and pin as well ,so we are happy to use Your Money `(your Money is our money & Our Money is Our Money)`\n,Regards \n Manager(DJD-E1)\n Thank You ****! We Scam Because We Care " #body
                    ,settings.EMAIL_HOST_USER,[data.email],fail_silently = False)
                print("Sent Succefully...")
            else:
                    return HttpResponse("OTP Missmatched.....")
        else:
            return HttpResponse("****** is not Valid Pin You *******")
    return render(request,'valid_otp.html')


def wallet(request):
    data = None
    bal = 0
    msg = ""
    f = False
    if request.method == "POST":
        acc = int(request.POST['acc'])
        pin = int(request.POST['pin'])
        try:
            data = Account.objects.get( Account_no = acc )
        except:
            pass
        if data is not None:
            if data.Pin == pin:
                bal = data.Balance
                f =True
            else:
                msg = "pls enter the valid Pin"
        else:
            msg = "pls enter the Valid account number.."
    
    context = {
        'bal' : bal,
        'var' : f,
        'msg' : msg
    }
    return render(request,'wallet.html' , context)

def withdraw(request):
    msg = ""
    if request.method == "POST":
        acc = int(request.POST['acc'])
        pin = int(request.POST['pin'])
        amount = int(request.POST['amount'])
        try:
            details = Account.objects.get( Account_no = acc )
        except:
            return HttpResponse("Invalid Account Number...")
        if details.Pin == pin:
            if details.Balance>=amount and amount>0:
                total_amount = details.Balance-amount
                details.Balance = total_amount
                details.save()
                send_mail(f"Dear Customer {details.Name} ",
                        f"FBH fraud bank of hyd .{amount}rs debited in Your account.\n and your current Balance is: {details.Balance},Regards \n Manager(DJD-E1)\n Thank You ****! We Scam Because We Care " #body
                        ,settings.EMAIL_HOST_USER,[details.email],fail_silently = False)
                messages.success(request,f"{amount}RS Successfully Debited...😒😒")
                # return redirect("index")
            else:
                return HttpResponse("insufficient Balance ...") 
        else:
            return HttpResponse("Invalid Pin...")
    return render(request,'withdraw.html')

def deposite(request):
    if request.method == "POST":
        acc = request.POST.get('acc')
        amount = int(request.POST.get('deposite'))
        try:
            data = Account.objects.get( Account_no = acc )
        except:
            return HttpResponse("Invalid Account Number...")
            # messages.success(request,"Invalid Account Number..")
        if amount >0 and amount<=20000:
            total_amount = data.Balance+amount
            data.Balance = total_amount
            data.save()
            send_mail(f"Hello {data.Name} MONEY DEPOSITE..",
                    f"FBH fraud bank of hyd .\n {amount}rs Credited in Your account..\n and Your Current balance is {data.Balance},Regards \n Manager(DJD-E1)\n Thank You ****! We Scam Because We Care " #body
                    ,settings.EMAIL_HOST_USER,[data.email],fail_silently = False)
            print("Sent Succefully...")
            messages.success(request,f"{amount}RS Successfully Credited...💐💐💐")
        else:
            return HttpResponse("Amount is must be greater than 0 and lessthan or equal 20000..")

    return render(request, 'deposite.html')

def transaction(request):
    msg=""
    s_data=0
    r_data=0
    if request.method == "POST":
        sender_acc=int(request.POST['s_acc'])
        receiver_acc = int(request.POST['r_acc'])
        s_pin = int(request.POST['pin'])
        amount = int(request.POST['amount'])
        try:
            s_data = Account.objects.get( Account_no = sender_acc)
        except:
            msg ="Invalid sender account number.."
        try:
            r_data = Account.objects.get( Account_no = receiver_acc )
        except:
            msg = "Invalid reciever account number.."
            
        if amount>=100 and amount<=20000:
            if s_data.Pin==s_pin:
                if s_data.Balance>=amount:
                    s_data.Balance-=amount
                    s_data.save()
                    send_mail(f"Dear Customer {s_data.Name} ",
                        f"FBH fraud bank of hyd .{amount}rs debited in Your account.\n and your current Balance is: {s_data.Balance},Regards \n Manager(DJD-E1)\n Thank You ****! We Scam Because We Care " #body
                        ,settings.EMAIL_HOST_USER,[s_data.email],fail_silently = False)
                    r_data.Balance+=amount
                    r_data.save()
                    send_mail(f"Hello {r_data.Name} MONEY DEPOSITE..",
                    f"FBH fraud bank of hyd .\n {amount}rs Credited in Your account..\n from {s_data.Account_no} and Your Current balance is {r_data.Balance},Regards \n Manager(DJD-E1)\n Thank You ****! We Scam Because We Care " #body
                    ,settings.EMAIL_HOST_USER,[r_data.email],fail_silently = False)
                    print("Sent Succefully...")
                    messages.success(request,f"{amount}RS Successfully Debited from {s_data.Account_no} Credited to {r_data.Account_no}...💐💐💐")
                else:
                    msg ="Insufficient Balance in Senders Bank"
            else:
                msg = "Invalid PIN"
        else:
            msg = "Amount must be greater than or equal 100 and lessthan or equal 20000 "

    return render(request, 'transaction.html',{'msg' : msg})
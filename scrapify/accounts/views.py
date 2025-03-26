# accounts/views.py
from datetime import datetime
from django.shortcuts import render, redirect
from .decorators import firebase_login_required
from django.contrib.auth import logout
import pyrebase
import re
import smtplib
from django.http import JsonResponse
from firebase_admin import auth

config = {
    configure according to user database
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()
authe = firebase.auth()


def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username-up")
        email = request.POST.get("email")
        password = request.POST.get("password_up")
        conpass = request.POST.get("conpass_up")
        if password == conpass:
            try:
                user = authe.create_user_with_email_and_password(email, password)
                uid = user["localId"]
                data = {
                    "Name": username,
                    "verified": False
                }
                database.child("Users").child(uid).child("details").set(data)
                return render(request, 'accounts/home.html')
            except Exception as e:
                print(str(e))
                pattern = r'"message":\s*"([^"]+)"'
                match = re.search(pattern, str(e))
                if match:
                    error_message = match.group(1)
                    print("Extracted Message:", error_message)
                    return render(request, "accounts/dual.html", {"messg": error_message, "show_up": True})

        else:
            error_register = "password do not match"
            return render(request, 'accounts/dual.html', {'messg': error_register, "show_up": True})
    return render(request, 'accounts/dual.html')


# jb else wla error aa rha to render krne pr login dikh rha usko register krna h

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("username")
        password = request.POST.get("password")
        try:
            next_url = request.session.pop('next_url', '/scraper/')
            user = authe.sign_in_with_email_and_password(email, password)
            request.session['uid'] = str(user['localId'])
            request.session['username'] = database.child("Users").child(request.session['uid']).child("details").child(
                "Name").get().val()
            return redirect(next_url)
        except Exception as e:
            print(str(e))
            messg = "user not found or incorrect credentials"
            return render(request, 'accounts/dual.html', {"messg": messg})
    return render(request, 'accounts/dual.html')


@firebase_login_required
def log_out(request):
    logout(request)
    return render(request, 'accounts/dual.html')


def send_password_reset_email(email, subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'scrapify.shopBuddy@gmail.com'
    sender_password = 'uzzd hafu xley wgne'

    if smtp_server and smtp_port and sender_email and sender_password and email:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        msg = f"Subject: {subject}\n\n{message}"

        server.sendmail(sender_email, email, msg)
        print('Email has been sent')
        server.quit()
    else:
        print('Email credentials are not properly set.')


def forgot_pass_view(request):
    return render(request, 'accounts/forgot_password.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        try:
            user = auth.get_user_by_email(email)
            reset_link = auth.generate_password_reset_link(email)
            subject = "Reset your password"
            message = f"Please click the link below to reset your password:\n\n{reset_link}\n\nIf it was not you please ignore this mail."
            send_password_reset_email(email, subject, message)
            return JsonResponse({'message': 'Password reset email sent!\nCheck your mail Id'}, status=200)

        except auth.UserNotFoundError:
            return JsonResponse({'error': 'No user found with this email address'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'accounts/dual.html')


def home(request):
    return render(request, 'accounts/home.html')


def dual(request):
    return render(request, "accounts/dual.html")


@firebase_login_required
def profile_view(request):
    p = database.child("Users").child(request.session['uid']).child("details").get().val()
    d = database.child("Users").child(request.session['uid']).child("Product Details").get().val()
    p["count"] = len(d.keys())
    print(p.keys())
    return render(request, 'accounts/profile.html', {"dataset": d, "profile": p})


@firebase_login_required
def edit_profile_view(request):
    return render(request, 'accounts/edit_profile.html')

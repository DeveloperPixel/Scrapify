import requests
import pyrebase
from datetime import datetime
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from .decorators import firebase_login_required
import smtplib
import re

config = {
 congire according to your database
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()


def send_email(url, title, price, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'scrapify.shopBuddy@gmail.com'
    sender_password = 'sender password'
    recipient_email = "recipient mail"

    if smtp_server and smtp_port and sender_email and sender_password and recipient_email:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        subject = "Hey! Price has dropped.!"
        body = f"{message}\nCheck out for {title}\n"
        msg = f"Subject: {subject}\n\n{body} {url} \n Price:{price}"

        server.sendmail(sender_email, recipient_email, msg)
        print('Email has been sent')
        server.quit()
    else:
        print('Email credentials are not properly set.')


@firebase_login_required
def home(request):
    # Render the home page with optional context
    return render(request, "scraper/home.html")


@firebase_login_required
def compare_price(request):
    proID = request.POST.get("product")
    d = database.child("Users").child(request.session['uid']).child("Product Details").child(proID).get().val()

    if request.method == 'POST':
        try:
            threshold = int(d["Threshold"])

            title = request.session.get('product_title')
            url = request.session.get('url')

            integer_value = d["Price"][:-1].replace(",", "")
            price = int(integer_value.replace(",", ""))

            if price <= threshold:
                message = f"The product price ({price}) is lower than the threshold ({threshold})."

                send_email(url, title, price, message)
                return HttpResponse(
                    f"The product price ({price}) is lower than the threshold ({threshold}).<br> Email Sent")
            else:
                return HttpResponse(f"The product price ({price}) is higher than the threshold ({threshold}).")
        except Exception as e:
            # return render(request, "home.html", {"error": f"An error occurred: {str(e)}"})
            return HttpResponse("exception", str(e))


def submit(request):
    proID = request.POST.get("product")
    d = database.child("Users").child(request.session['uid']).child("Product Details").child(proID).get().val()
    print("normal", type(d["Price"]))
    print(d["Threshold"])
    return None


import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]


@firebase_login_required
def scrape_amazon(request):
    if request.method == 'POST':
        Raw_url = request.POST.get('url')
        f_url = requests.get(Raw_url)
        url = f_url.url
        request.session['url'] = url

        if not url or not urlparse(url).netloc:
            return render(request, "scraper/home.html", {"error": "Invalid URL"})

        headers = {"User-Agent": random.choice(USER_AGENTS),
                   "Accept-Language": "en-US,en;q=0.9",
                   "Referer": "https://www.amazon.in/"}

        try:
            with httpx.Client(timeout=15) as client:
                response = client.get(url, headers=headers)

                if "captcha" in response.text.lower():
                    print("CAPTCHA encountered. Try again later.")
                    return None

                if not response:
                    return render(request, "scraper/home.html", {"error": "Failed to fetch the webpage"})

                soup = BeautifulSoup(response.text, 'html.parser')

                # title
                try:
                    product_title = soup.find('span', id='productTitle')
                    product_title = product_title.text.strip() if product_title else "Title Not Found"
                except Exception:
                    product_title = "Title Parsing Error"

                # price
                try:
                    product_price = soup.find('span', class_='a-price-whole')
                    product_price = product_price.text.strip() if product_price else "Price Not Found"
                except Exception:
                    product_price = "Price Parsing Error"

                #  STAR RATING
                try:
                    product_star = soup.find('span', class_='a-icon-alt')
                    star_text = product_star.get_text(strip=True) if product_star else "Star Rating not found"
                except Exception:
                    star_text = "Star Rating Parsing Error"

                # Customer Rating
                try:
                    product_rating = soup.find('span', id='acrCustomerReviewText').get_text() if soup.find('span',
                                                                                                           id='acrCustomerReviewText') else "Rating Not Found"
                except Exception:
                    product_rating = "Rating Parsing Error"

                # OLD MRP
                try:
                    old_mrp = soup.find('span', class_='a-text-price')
                    old_mrp_text = old_mrp.find('span', class_='a-offscreen').get_text(
                        strip=True) if old_mrp else "Old MRP not found"
                except Exception:
                    old_mrp_text = "MRP Parsing Error"

                # IMG Link
                try:
                    image = soup.find('img', id='landingImage')
                    image_link = image['src'] if image else "Image not found"
                except Exception:
                    image_link = "Image Parsing Error"

            request.session['product_price'] = product_price
            request.session['product_title'] = product_title
            request.session['star_text'] = star_text
            request.session['product_rating'] = product_rating
            request.session['old_mrp_text'] = old_mrp_text
            request.session['image_link'] = image_link

            per = round(int(product_price[:-1].replace(",", "")) / int(old_mrp_text[1:].replace(",", "")) * 100)
            request.session['per'] = per

            current_datetime = datetime.now()
            add_time = current_datetime.strftime("%Y%m%d%H%M%S")
            data = {
                "time": add_time,
                "title": product_title,
                "price": product_price,
                "star": star_text,
                "rating": product_rating,
                "old_MRP": old_mrp_text,
                "image": image_link,
                "url": url,
                "per": per
            }
            return render(request, "scraper/detail_page.html", data)
        except Exception as e:
            return render(request, "scraper/home.html", {"error": f"An error occurred: {str(e)}"})

    return render(request, "scraper/home.html")


@firebase_login_required
def product(request):
    return render(request, "scraper/detail_page.html")


@firebase_login_required
def push_product(request):
    threshold = int(request.POST.get('threshold').replace("e", ""))
    request.session['threshold'] = threshold
    current_datetime = datetime.now()
    add_time = current_datetime.strftime("%d %b,%Y %H:%M:%S")
    print("Formatted Date and Time:", add_time)
    data = {
        "Time": add_time,
        "Title": request.session['product_title'],
        "Price": request.session['product_price'],
        "Star": request.session['star_text'],
        "Rating": request.session['product_rating'],
        "Old_MRP": request.session['old_mrp_text'],
        "Image": request.session['image_link'],
        "Url": request.session['url'],
        "per": request.session['per'],
        "Threshold": threshold
    }
    url = request.session['url']
    pattern = r"/dp/([^/?&]+)"
    match = re.search(pattern, url)
    if match:
        new_product_id = match.group(1)
        d = database.child("Users").child(request.session['uid']).child("Product Details").get().val()
        p = database.child("Users").child(request.session['uid']).child("details").get().val()
        if d is None:
            database.child("Users").child(request.session['uid']).child("Product Details").child(new_product_id).set(
                data)
            d = database.child("Users").child(request.session['uid']).child("Product Details").get().val()
            message = "Product Added Successfully in your List"
            return render(request, 'accounts/profile.html', {'message': message, "dataset": d, "profile": p})

        product_id_list = list(d.keys())

        if new_product_id in product_id_list:
            message = "Product Already Exists in your List"
            p["count"] = len(d.keys())
            return render(request, "accounts/profile.html", {'message': message, "dataset": d, "profile": p})

        database.child("Users").child(request.session['uid']).child("Product Details").child(new_product_id).set(data)
        time.sleep(5)
        n = database.child("Users").child(request.session['uid']).child("Product Details").get().val()
        p["count"] = len(d.keys())
        message = "Product Added Successfully in your List"
        return render(request, "accounts/profile.html", {'message': message, "dataset": n, "profile": p})
    else:
        message = "Unable to Add product"
        return render(request, "scraper/home.html", {'message': message})

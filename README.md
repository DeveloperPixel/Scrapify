<div align="center">

# 🕸️ Scrapify

![Scrapify Logo](https://via.placeholder.com/150x150.png?text=Scrapify)

**Smart Price Tracking & Notification Bot**  
[![Live](https://img.shields.io/badge/Live-Scrapify.pythonanywhere.com-brightgreen?style=for-the-badge&logo=pythonanywhere)](https://Scrapify.pythonanywhere.com)  

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)](https://www.python.org/)  
[![Django](https://img.shields.io/badge/Django-4.0-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)  
[![Firebase](https://img.shields.io/badge/Firebase-Cloud-yellow?style=for-the-badge&logo=firebase)](https://firebase.google.com/)  
[![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen?style=for-the-badge&logo=selenium)](https://www.selenium.dev/)  
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Overview
**Scrapify** is a web-based application that scrapes product details (title, price, ratings, etc.) from major e-commerce platforms like **Amazon** and **Flipkart**.  
It also notifies users via **Email** and **Firebase Push Notifications** when product prices drop.  

This project is designed to **save users time and money** by automatically monitoring product prices without manual searching.  

---

## ✨ Features
- 🔍 **Product Scraping**: Extracts title, price, rating, and availability.  
- 📊 **Multi-Website Support**: Works with Amazon & Flipkart (expandable).  
- 📩 **Notifications**: Sends Email alerts via Gmail SMTP.  
- 🔔 **Push Alerts**: Integrated with Firebase for real-time notifications.  
- ⏳ **Scheduled Scraping**: Runs periodically via GitHub Actions.  
- 🛡️ **CAPTCHA Handling**: Supports ScraperAPI to bypass detection.  

---

## 🛠️ Tech Stack
- **Backend:** Python, Django  
- **Scraping:** Selenium + ScraperAPI  
- **Database:** Firebase Firestore  
- **Notifications:** Firebase Cloud Messaging, Gmail SMTP  
- **Deployment:** PythonAnywhere  

---

## 🚀 Live Demo
👉 [Scrapify Live Website](https://Scrapify.pythonanywhere.com)  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/scrapify.git
cd scrapify
```
## 📂 Project Structure

```
scrapify/
│── scrapify/                # Django project folder
│── static/                  # Static files (CSS, JS, Images)
│── templates/               # HTML templates
│── scrape_amazon.py         # Amazon scraper script
│── scrape_flipkart.py       # Flipkart scraper script
│── requirements.txt         # Dependencies
│── README.md                # Project documentation
```

---

## ⚡ Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/scrapify.git
   cd scrapify
   ```

2. Create a virtual environment & install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   pip install -r requirements.txt
   ```

3. Run Django server:

   ```bash
   python manage.py runserver
   ```

4. Access locally at:

   ```
   http://127.0.0.1:8000/
   ```

---

## 📌 Roadmap

* ✅ Amazon & Flipkart support
* ✅ Email + Push notifications
* 🔄 Add more e-commerce sites (Myntra, Meesho, etc.)
* 📊 Price history & visualization
* 📱 Mobile app integration

---

## 👨‍💻 Author

**Keshav Prajapati**
7th Semester, BTech CSE, Sage University Bhopal
📧 Contact: *keshavprajapati357@gmail.com*

---



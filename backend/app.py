import psycopg2
import csv
from flask import Flask, jsonify, request, send_file, render_template, make_response
from models import *
from flask_cors import CORS
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from reportlab.lib.pagesizes import letter, A4, A3, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from io import BytesIO
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd
from werkzeug.security import generate_password_hash
import jwt
from sqlalchemy import func
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import base64
from weasyprint import HTML
from sqlalchemy import func
import time

load_dotenv()

app = Flask(__name__)

CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)


# smtplib.SMTP.debuglevel = 1


def create_database():
    connection = psycopg2.connect(
        user="postgres", password="qwerty", host="127.0.0.1", port="5432")
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE my_database")
        print("Database created successfully")
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists")
    finally:
        cursor.close()
        connection.close()


def insert_dummy_data():
    colleagues_data = [
        # {"name": "Neha Mishra", "email": "neha@accorppartners.com",
        #     "department": "HR", "designation": "Consultant"},
        # {"name": "Ishaan", "email": "ishan@accorppartners.com",
        #     "department": "HR", "designation": "Consultant"},
        # {"name": "Alice Johnson", "email": "22dp1000105@ds.study.iitm.ac.in",
        #     "department": "IT", "designation": "Analyst"},
        # {"name": "Anurag Kumar", "email": "akanuragkumar75@gmail.com",
        #     "department": "Developer", "designation": "Developer"},
        # {"name": "Sethi", "email": "tech@kvqaindia.com",
        #     "department": "Developer", "designation": "Developer"},
        # {"name": "Ritika", "email": "training@kvqaindia.com",
        #     "department": "Leadership", "designation": "CTO"},
        # {"name": "Lav Kaushik", "email": "lav@kvqaindia.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun", "email": "2345varun@gmail.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG", "email": "trg@kvqaindia.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales", "email": "sales1@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO", "email": "noidaiso22@gmail.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby", "email": "ruby@kvqaindia.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli", "email": "babli12@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha", "email": "shikha12@kvqaindia.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan", "email": "kanchan@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info", "email": "info@kvqaindia.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali", "email": "vaishali@kvqaindia.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha", "email": "neha12@kvqaindia.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR", "email": "dhr@kvqaindia.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi", "email": "delhi@kvqaindia.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun", "email": "arun.kvqa@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS", "email": "ops@kvqaindia.com",
        #     "department": "OPS", "designation": "OPS"},

{'name': 'Aarsh Pardeshi', 'email': 'aarsh.pardeshi@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Aarshabh Gupta', 'email': 'aarshabh.gupta@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Abhijith Sinikumary', 'email': 'abhijith.sinikumary@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Abhishek Agrawal', 'email': 'abhishek.agrawal1@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Abhishek Sarfare', 'email': 'sarfare.abhishek@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Achal Mani', 'email': 'mani.achal@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Aditi Anand', 'email': 'aditi.anand@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Aditya Dewadwal', 'email': 'aditya.dewadwal@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Aditya Jha', 'email': 'aditya.jha@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Aditya Raval', 'email': 'aditya.raval@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Aditya Vyas', 'email': 'aditya.vyas@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Adnan Khan', 'email': 'adnan.k@icicibank.com', 'department': '/CANTRESRY/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Akanksha Manku', 'email': 'akanksha.manku@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Akshay Jaggi', 'email': 'akshay.jaggi1@icicibank.com', 'department': '/CANRETAIL/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Alexandrina S.A.', 'email': 'alexandrina.sa@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Alisha Mishra', 'email': 'alisha.mishra@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Aman Sehgal', 'email': 'aman.sehgal1@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Amanjeet Gumber', 'email': 'amanjeet.gumber@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Amardeep Singh', 'email': 'amardeep.singh1@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ambuj Kumar', 'email': 'ambuj.kumar4@icicibank.com', 'department': '/CANRETAIL/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Amit Ahuja', 'email': 'amit.ahuja@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Amit Chugh', 'email': 'amit.chugh@icicibank.com', 'department': '/CANTRESRY/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Anita Sequeira', 'email': 'anita.seq@icicibank.com', 'department': '/CANADM/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Anjali A', 'email': 'anjali.a@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Anjali Deswal', 'email': 'anjali.deswal@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ankit Juneja', 'email': 'ankit.juneja1@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Ankit Manchanda', 'email': 'ankit.manchanda@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ankita Vadodariya', 'email': 'ankita.vadodariya@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Ankur Dadhich', 'email': 'ankur.dadhich@icicibank.com', 'department': '/CANAUDIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ankur Srivastava', 'email': 'ankur.shr@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Anthony Coulthard', 'email': 'anthony.coulthard@icicibank.com', 'department': '/CANLEGAL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Anupam Singh', 'email': 's.anupam@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Anurag Kumar', 'email': 'anurag.ku@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Anushka Sharma', 'email': 'anushka.sharma@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'April Harvey', 'email': 'april.harvey@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Archana Shukla', 'email': 'shukla.archana@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Arsh Seksaria', 'email': 'arsh.seksaria@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Aruna Boila', 'email': 'aruna.boila@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Arvind Sud', 'email': 'arvind.sud@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Ashish Meena', 'email': 'ashish.meena@icicibank.com', 'department': '/SRSG/IBANK/BANGLRE', 'designation': 'Banker'},
{'name': 'Ashwaya Bhatia', 'email': 'ashwaya.bhatia@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ashwin Paldano', 'email': 'paldano.ashwin@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Atharv Kale', 'email': 'kale.atharv@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Avneet Kaur', 'email': 'avneet.kaur3@icicibank.com', 'department': '/CANRETAIL/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Bernard Dias', 'email': 'bernard.dias@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Bharvi Parab', 'email': 'bharvi.parab@icicibank.com', 'department': '/CANADM/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Bhavya Singh', 'email': 'bhavya.singh1@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Bhupinder Singh', 'email': 'sing.bhupinder@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Bhushan Joshi', 'email': 'joshi.bhushan@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Boby Sharma', 'email': 'boby.sharma@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Cameron Ho', 'email': 'cameron.ho@icicibank.com', 'department': '/CANLEGAL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Charmi Desai', 'email': 'desai.charmi@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Christie-ann D’souza', 'email': 'christieann.d@icicibank.com', 'department': '/CANADM/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Damini Gawali', 'email': 'damini.gawali@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Daniya Grover', 'email': 'grover.daniya@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Debasis Dash', 'email': 'debasis.dash1@icicibank.com', 'department': '/CANRETAIL/IBANK/BSCO_366', 'designation': 'Banker'},
{'name': 'Deborah Adhikary', 'email': 'deborah.adhikary@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Deep Dalwadi', 'email': 'dalwadi.deep@icicibank.com', 'department': '/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Deepa Mudgal', 'email': 'deepa.jambur@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Deepika Ghai', 'email': 'deepika.ghai1@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Deepshikha Mutha', 'email': 'deepshikha.mutha1@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Deepti Sebastian', 'email': 'sebastian.deepti@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Deepti Sharma', 'email': 'deepti.sharma2@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Devang Shukla', 'email': 'devang.shukla@ext.icicibank.com', 'department': '/EXT/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Dharminder Mariya', 'email': 'dharminder.mariya@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Dilpreet Bhatia', 'email': 'dilpreet.bhatia@icicibank.com', 'department': '/CANHR/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Dilpreet Kaur', 'email': 'dilpreet.kaur2@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Dimpal Luhana', 'email': 'dimpal.luhana@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Divya Saxena', 'email': 'divya.saxena@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Dixita Joshi', 'email': 'dixita.joshi@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Don Abraham', 'email': 'calipper.abraham@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Enrique Menacho', 'email': 'edwin.menacho@icicibank.com', 'department': '/CANADM/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ganesh Ramachandran', 'email': 'ganesh.ramachandran@icicibank.com', 'department': '/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Gaurav Jalan', 'email': 'gaurav.jalan1@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Gaurav Saklani', 'email': 'gaurav.saklani@icicibank.com', 'department': '/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Gaurav Tiwari', 'email': 'gaurav.ti@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Geet Deshpande', 'email': 'geet.deshpande@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Geetanjali Gadakh', 'email': 'geetanjali.gadakh@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Gunjan Mehra', 'email': 'gunjan.mehra@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Gurleen Shinh', 'email': 'kaur.shinh@icicibank.com', 'department': '/CANRETAIL/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Gursimran Singh', 'email': 'gursimran.si@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Harmanjeet Kaur', 'email': 'kaur.harmanjeet@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Harmanpreet Sandhu', 'email': 'singh.sandhu@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Harsh Sharma', 'email': 'hars.sha@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Harshpreet Singh', 'email': 'harshpreet.singh@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Harvinder Singh', 'email': 'harvinder.s@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Heena Rani', 'email': 'rani.heena@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Hemang Thanavala', 'email': 'hemang.thanavala@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Himanshu Sajlan', 'email': 'himanshu.sajlan@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Hitesh Sharma', 'email': 'hitesh.sharma5@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Hrishik Bhanushali', 'email': 'hrishik.bhanushali@icicibank.com', 'department': '/CANFIN/IBANK/BSCO_366', 'designation': 'Banker'},
{'name': 'Iain Paulin', 'email': 'iain.paulin@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Inderjit Kaur', 'email': 'inderjit.kau@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Jagdeep Kaur', 'email': 'jagdeep.k@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Jaideep Chandok', 'email': 'jaideep.chandok@icicibank.com', 'department': '/CANTRESRY/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Janki Gandhi', 'email': 'janki.gandhi@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Jasmeet Kaur', 'email': 'jasmeet.kaur5@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Jaspreet Kaur', 'email': 'jaspreet.kaur5@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Jaspreet Kaur', 'email': 'kaur.jasp@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Jay Manickam', 'email': 'jay.manickam@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Jeega Liu', 'email': 'jeega.liu@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Jie Zhou', 'email': 'jie.zhou@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Jigar Jain', 'email': 'jigarj.jain@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Jijo John', 'email': 'john.jijo@icicibank.com', 'department': '/CANTRESRY/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Jingtong Yu', 'email': 'jingtong.yu@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Joycy Kovila', 'email': 'kovila.joycy@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Judith Sari', 'email': 'judith.sari@icicibank.com', 'department': '/CANLEGAL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Jyoti Arora', 'email': 'jyoti.arora2@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Kamalpreet Kaur', 'email': 'kaur.kama@icicibank.com', 'department': '/CANRETAIL/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Karamjeet Kaur', 'email': 'karamjeet.kaur2@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Karan Shah', 'email': 'shah.kara@icicibank.com', 'department': '/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Karish Gera', 'email': 'karish.gera@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Karrthik Kumhar', 'email': 'karrthik.kumhar@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Kartik Bhoyare', 'email': 'kartik.bhoyare@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Kavita Rao', 'email': 'kavita.rao1@icicibank.com', 'department': '/CANBRANCH/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Kavya Bhatt', 'email': 'bhatt.kavya@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Kavya Rastogi', 'email': 'kavya.rastogi@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Kawaljeet Kaur', 'email': 'kawaljeet.kaur2@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Kawaljit Kaur', 'email': 'kawaljit.kaur1@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Khaira Devinderpal', 'email': 'khaira.devinderpal@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Kishokanth Kanagaratnam', 'email': 'kishokanth.kanagaratnam@icicibank.com', 'department': '/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Kishore Kumar', 'email': 'kishore.ku@icicibank.com', 'department': '/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Komal Bhagchandani', 'email': 'komal.bhagchandani@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Kreetika Verma', 'email': 'kreetika.verma@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Krishnapriya P', 'email': 'krishnapriya.p@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Kush Prajapati', 'email': 'kush.prajapati@ext.icicibank.com', 'department': '/EXT/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Lakhbir Singh', 'email': 'lakhbir.singh1@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Lakshmi Ram', 'email': 'lakshmi.ram@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Lester Fernandes', 'email': 'lester.fernandes@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Lijeena Jamnas', 'email': 'lijeena.jamnas@icicibank.com', 'department': '/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Lionel Meunier', 'email': 'lionel.meunier@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': "Loveena D'cunha", 'email': 'loveena.dcunha@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Mahendar Kola', 'email': 'mahendar.ko@icicibank.com', 'department': '/CANBRANCH/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Mahesh Jhawar', 'email': 'mahesh.jhawar@icicibank.com', 'department': '/CANAUDIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Malini Siva', 'email': 'malini.siva@icicibank.com', 'department': '/CANBRANCH/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Mandeep Sharma', 'email': 'sharma.mandeep@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Manhar Arora', 'email': 'manhar.arora@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Manish Bohra', 'email': 'manish.bohra1@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Manpreet Bhatia', 'email': 'singh.bhatia@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Manpreet Kaur', 'email': 'manpreet.kaur21@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Manpreet Kaur', 'email': 'manpreet.kaur9@icicibank.com', 'department': '/CANBRANCH/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Manpreet Kaur', 'email': 'manpr.kau@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Manpreet Singh', 'email': 'manpreet.singh31@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Manpreet Wason', 'email': 'manpreet.wason@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Manseerat Kaur', 'email': 'manseerat.kaur@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Marilyn Li', 'email': 'marilyn.li@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Marlene Dsilva', 'email': 'marlene.dsilva@icicibank.com', 'department': '/CANADM/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Megha Hooda', 'email': 'hooda.megha@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Melvin Wong', 'email': 'wong.melvin@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Mohammed Hussain', 'email': 'mohammed.hussain@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Mohit Bhatia', 'email': 'mohit.bhatia@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Monisha Pinto', 'email': 'monisha.pinto@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Nachiket Patel', 'email': 'patel.nachiket@icicibank.com', 'department': '/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Naman Bhargava', 'email': 'naman.bhargava@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Nandita Chhibbar', 'email': 'nandita.chhibbar@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Navneet Grover', 'email': 'grover.navneet@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Navneet Kalra', 'email': 'navneet.kalra@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Navneet Kaur', 'email': 'navneet.kau@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Neeraj Londhe', 'email': 'neeraj.londhe@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Neh Chhaya', 'email': 'neh.chhaya@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Neha Sharma', 'email': 'neha.sharma29@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Nikitaben Patel', 'email': 'nikitaben.patel1@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Nikki Bello', 'email': 'nikki.bello@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Nikunj Suneja', 'email': 'nikunj.suneja@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Niloy Nath', 'email': 'niloy.nath@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Nimit Soni', 'email': 'nimit.soni1@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Nishant Patel', 'email': 'nishant.patel@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Nithish Kolla', 'email': 'nithish.kolla@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Nurisha Kapoor', 'email': 'nurisha.kapoor@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Parag Chitnis', 'email': 'parag.chitnis@icicibank.com', 'department': '/CANRETAIL/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Parth Patel', 'email': 'parth.patel@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Pehal Chandnani', 'email': 'chandnani.pehal@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Prabhjot Kaur', 'email': 'prabhjot.kaur4@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Prachi Desai', 'email': 'prachi.desai2@ext.icicibank.com', 'department': '/EXT/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Prachi Shah', 'email': 'shah.pra@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Prachi Singh', 'email': 'prachi.singh3@icicibank.com', 'department': '/CANRETAIL/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Prachi Vyas', 'email': 'prachi.vyas1@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Prachiti Sewalkar', 'email': 'sewalkar.prachiti@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Pradeep Sharma', 'email': 'pradeep.sharm@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Prafull Bhanushali', 'email': 'prafull.bhanushali@icicibank.com', 'department': '/CANAUDIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Pranami Khaund', 'email': 'khaund.pranami@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Pranav Chadha', 'email': 'pranav.chadha@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Prasidhi Patel', 'email': 'prasidhi.patel@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Praveen Dumbre', 'email': 'praveen.dumbre@ext.icicibank.com', 'department': '/EXT/TECH_INFR/IBANK/thane TCC', 'designation': 'Banker'},
{'name': 'Priya Bayangolkar', 'email': 'priya.bayangolkar@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Pulkit Sareen', 'email': 'pulkit.sareen@ext.icicibank.com', 'department': '/EXT/CANBRANCH/IBANK/Surrey', 'designation': 'Banker'},
{'name': 'Rabinder Kaur', 'email': 'rabinder.kaur@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Raghavendra Shetty', 'email': 'raghavendra.shetty@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rahul Bijalwan', 'email': 'rahul.bijalwan@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rahul Jadhav', 'email': 'rahul.jadh@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rahul Singh', 'email': 'rahul.singh52@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Rajan Sharda', 'email': 'rajan.sharda@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rajesh Nimgire', 'email': 'rajesh.nimgire@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rajitha Kulangarath', 'email': 'rajitha.kulangarath@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rakesh Kondoli', 'email': 'rakesh.kondoli@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rakshanda Vimlesh', 'email': 'rakshanda.vimlesh@icicibank.com', 'department': '/CANMORTGE/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Ramandeep Singh', 'email': 'ramandeep.singh5@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Ramanpreet Chanda', 'email': 'ramanpreet.chanda@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Ramarao Battula', 'email': 'ramarao.battula@ext.icicibank.com', 'department': '/EXT/TECH_INFR/IBANK/thane TCC', 'designation': 'Banker'},
{'name': 'Rashi Chomal', 'email': 'rashi.chomal@icicibank.com', 'department': '/CANTRESRY/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Raymond Lee', 'email': 'raymond.lee@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Reema Yasmeen', 'email': 'reema.y@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rewati Tejwani', 'email': 'rewati.tejwani@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rishi Chug', 'email': 'rishi.chug@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rishi Gulati', 'email': 'rishi.gulati@icicibank.com', 'department': '/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Rishi Sharma', 'email': 'rishi.sharma3@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ritesh Jha', 'email': 'jha.ritesh@icicibank.com', 'department': '/CANHR/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ritesh Pungalia', 'email': 'ritesh.pungalia@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Ritu Sandhu', 'email': 'ritu.sandhu@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rohit Kabra', 'email': 'rohit.kabra@icicibank.com', 'department': '/CANAUDIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Rojina Sharma', 'email': 'rojina.sharma@icicibank.com', 'department': '/CANMORTGE/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Ruchika Tandon', 'email': 'ruchika.tandon@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Rupinder Kaur', 'email': 'kaur.rupi@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Sachin Sharma', 'email': 'sachin.sharma23@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Sachin Yadav', 'email': 'sachin.ya@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Sagar Dhingra', 'email': 'sagar.dhingra@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Sagar Orum', 'email': 'orum.sagar@icicibank.com', 'department': '/CANBRANCH/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Sahil Panwar', 'email': 'sahil.panwar@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Saikat Mitra', 'email': 'saikat.mitra1@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Sainyam Kishnani', 'email': 'sainyam.kishnani@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Sakthishanmugham C', 'email': 'sakthishanmugham.c@icicibank.com', 'department': '/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Saniya Fitter', 'email': 'fitter.saniya@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Sanket Shah', 'email': 'sanket.sh@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Santharam Varahabhotla', 'email': 'varahabhotla.santharam@icicibank.com', 'department': '/CANTRESRY/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Sarabjeet Kaur', 'email': 'sarabjeet.kaur1@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Satinder Virk', 'email': 'virk.satinder@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Saurin Shah', 'email': 'saurin.shah2@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Sayeed Babader', 'email': 'sayeed.babader@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Sehajpreet Singh', 'email': 'sehajpreet.singh@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Sehdev Chauhan', 'email': 'sehdev.singh@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Senthuran Kopalakrishnan', 'email': 'kopalakrishnan.senthuran@icicibank.com', 'department': '/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shaila Pinto', 'email': 'shaila.pinto@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shalini Yadav', 'email': 'shalini.yadav2@icicibank.com', 'department': '/CANHR/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shimoli Shah', 'email': 'shah.shimoli@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shivani Rathore', 'email': 'shivani.rathore1@icicibank.com', 'department': '/CANBRANCH/IBANK/BSCO_366', 'designation': 'Banker'},
{'name': 'Shobhit Bajpai', 'email': 'shobhit.bajpai@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shreya Satra', 'email': 'shreya.satra@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shubh Bagaria', 'email': 'shubh.bagaria@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Shubh Verma', 'email': 'shubh.verma@ext.icicibank.com', 'department': '/EXT/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shubhpreet Sura', 'email': 'shubhpreet.sura@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shweta Moghe', 'email': 'shweta.moghe@icicibank.com', 'department': '/CANBRANCH/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shweta Tiwari', 'email': 'shweta.ti@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Shyam Menon', 'email': 'shyam.menon@ext.icicibank.com', 'department': '/EXT/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Siddharth Kerwar', 'email': 'siddharth.kerwar@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Siddhartha Anand', 'email': 'siddhartha.anand@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Simardeep Kochhar', 'email': 'simardeep.kochhar@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Simranjeet Kaur', 'email': 'simranjeet.kaur8@icicibank.com', 'department': '/CANRETAIL/IBANK/CALGARY', 'designation': 'Banker'},
{'name': 'Simranjeet Singh', 'email': 'singh.simra@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Sukhpreet Kaur', 'email': 'sukhpreet.kaur1@icicibank.com', 'department': '/CANBRANCH/IBANK/BRAMPTON', 'designation': 'Banker'},
{'name': 'Sulagna Batabyal', 'email': 'sulagna.batabyal@icicibank.com', 'department': '/CANRETAIL/IBANK/SCARBOROUGH', 'designation': 'Banker'},
{'name': 'Sumit Dulloo', 'email': 'sumit.dulloo@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Surabhi Doshi', 'email': 'surabhi.doshi@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Swati Dubey', 'email': 'swati.du@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Syed Azgar', 'email': 'syed.azgar@icicibank.com', 'department': '/CANOPS/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Tanveer Kaur', 'email': 'tanveer.kaur1@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Tejas Kakade', 'email': 'tejas.kakade@ext.icicibank.com', 'department': '/EXT/CANIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Tova Blum', 'email': 'tova.blum@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Trupti Solanki', 'email': 'trupti.solanki1@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Tushar Kumar', 'email': 'tushar.kumar@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vaishali Vaishali', 'email': 'vaishali.vaishali1@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Valeny Rodrigues', 'email': 'valeny.rodrigues1@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vatsal Vithalani', 'email': 'vithalani.vatsal@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Versha Kaul', 'email': 'versha.kaul@icicibank.com', 'department': '/IBGCRRISK/IBANK/BSCO_366', 'designation': 'Banker'},
{'name': 'Vidhi Udeshi', 'email': 'vidhi.udeshi@icicibank.com', 'department': '/COMP/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vidyavati Gore', 'email': 'vidyavati.gore@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vikas Jindal', 'email': 'vikas.jin@icicibank.com', 'department': '/CANAUDIT/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vinita Kavarana', 'email': 'vinita.kavarana@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Viraj Hegde', 'email': 'viraj.hegde@icicibank.com', 'department': '/IBGCRRISK/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Virpal Kaur', 'email': 'virpal.kaur@icicibank.com', 'department': '/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vishnu Paranandi', 'email': 'priya.paranandi@icicibank.com', 'department': '/CANRETAIL/IBANK/', 'designation': 'Banker'},
{'name': 'Vishruti Patel', 'email': 'vishruti.patel@icicibank.com', 'department': '/CBGCA/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vivek Joshi', 'email': 'vivek.joshi2@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vivek Upreti', 'email': 'vivek.upreti@icicibank.com', 'department': '/CANFIN/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Vivian Varghese', 'email': 'varghese.vivian@icicibank.com', 'department': '/CANHR/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Xavier Sebastian', 'email': 'sebastian.xavier@icicibank.com', 'department': '/CANMORTGE/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Yannish Khanna', 'email': 'yannish.khanna@ext.icicibank.com', 'department': '/EXT/CANRETAIL/IBANK/TORONTO', 'designation': 'Banker'},
{'name': 'Yash Sharma', 'email': 'yash.sharma6@icicibank.com', 'department': '/CANBRANCH/IBANK/', 'designation': 'Banker'},
{'name': 'Zaira Hasan', 'email': 'zaira.hasan@ext.icicibank.com', 'department': '/EXT/CANBRANCH/IBANK/Surrey', 'designation': 'Banker'},
    ]

    # colleagues = [Colleagues(name=data['name'], email=data['email'],
    #                          designation=data['designation']) for data in colleagues_data]

    for data in colleagues_data:
        existing_colleague = Colleagues.query.filter_by(
            email=data['email']).first()
        if not existing_colleague:  # Only insert if email doesn't exist
            colleague = Colleagues(
                name=data['name'], email=data['email'], department=data['department'], designation=data['designation'])
            db.session.add(colleague)

    questions_data = [
        {"question_text": "What is phishing?", "options": [
            "A method of fishing",
            "An attempt to obtain sensitive information by pretending to be a trustworthy entity",
            "A type of computer virus",
            "A software update"],
         "answer": "An attempt to obtain sensitive information by pretending to be a trustworthy entity"},

        {"question_text": "Which of the following is a common method used in phishing attacks?", "options": [
            "Phone calls",
            "Text messages (SMS)",
            "Emails",
            "All of the above"],
         "answer": "All of the above"},

        {"question_text": "What is a common sign of a phishing email?", "options": [
            "Professional formatting",
            "Misspellings and grammatical errors",
            "A personal greeting using your name",
            "A recognizable sender email address"],
         "answer": "Misspellings and grammatical errors"},

        {"question_text": "What should you do if you receive an email asking for your personal information?", "options": [
            "Reply with the information requested",
            "Click on any links in the email",
            "Verify the sender’s email address and contact the company directly",
            "Ignore it and delete it"],
         "answer": "Verify the sender’s email address and contact the company directly"},

        {"question_text": "Which of these can be a red flag in a phishing attempt?", "options": [
            "Urgent requests for action",
            "Generic greetings (e.g., 'Dear Customer')",
            "Unexpected attachments",
            "All of the above"],
         "answer": "All of the above"},

        {"question_text": "Which of the following is a safe practice when handling emails?", "options": [
            "Open attachments from unknown senders",
            "Hover over links to check their destination before clicking",
            "Use the same password for all accounts",
            "Share personal information over email if requested"],
         "answer": "Hover over links to check their destination before clicking"},

        {"question_text": "What does a phishing website often look like?", "options": [
            "Identical to a legitimate site but with a slightly different URL",
            "Always has a secure connection (https)",
            "Contains a lot of advertisements",
            "Usually has a recognizable logo"],
         "answer": "Identical to a legitimate site but with a slightly different URL"},

        {"question_text": "Which of these is NOT a typical feature of a phishing email?", "options": [
            "Spelling mistakes",
            "A legitimate sender’s email address",
            "An urgent tone",
            "Unsolicited attachments"],
         "answer": "A legitimate sender’s email address"},

        {"question_text": "What is 'whaling' in the context of phishing?", "options": [
            "Phishing targeting high-profile individuals like executives",
            "A type of fishing gear",
            "A phishing method that uses social engineering",
            "Phishing that targets small businesses"],
         "answer": "Phishing targeting high-profile individuals like executives"},

        {"question_text": "How can you protect yourself from phishing attacks?", "options": [
            "Use strong, unique passwords for each account",
            "Enable two-factor authentication",
            "Regularly update software and antivirus programs",
            "All of the above"],
         "answer": "All of the above"},

        {"question_text": "True or False: Phishing attacks only target large organizations.", "options": [
            "True",
            "False"],
         "answer": "False"},

        {"question_text": "What should you do if you suspect you've been a victim of phishing?", "options": [
            "Ignore it; it's not a big deal",
            "Change your passwords immediately and report the incident",
            "Forward the email to your friends",
            "Contact your ISP to complain"],
         "answer": "Change your passwords immediately and report the incident"},

        {"question_text": "Which of the following are key features of a phishing website?", "options": [
            "A URL with strange characters or an incorrect domain name",
            "A site that asks for sensitive data such as passwords or credit card numbers",
            "Poor design or errors on the website",
            "All of the above"],
         "answer": "All of the above"},

        {"question_text": "What role does social engineering play in phishing?", "options": [
            "It’s a method to catch fish",
            "It exploits human psychology to manipulate individuals",
            "It refers to the technology used in phishing attacks",
            "It’s a way to create secure passwords"],
         "answer": "It exploits human psychology to manipulate individuals"},

        {"question_text": "Why is it important to keep software and systems updated?", "options": [
            "To make them look nice",
            "To protect against known vulnerabilities that phishing attacks can exploit",
            "To ensure compatibility with older systems",
            "It’s not important"],
         "answer": "To protect against known vulnerabilities that phishing attacks can exploit"},

        {"question_text": "What is the best way to verify the legitimacy of an email you receive that looks suspicious?", "options": [
            "Reply to the email with questions about the sender’s request",
            "Call the organization using a number from their official website",
            "Click on any included links to verify the information",
            "Forward the email to your friends for their opinions"],
         "answer": "Call the organization using a number from their official website"},

        {"question_text": "What is the first step you should take if you think you’ve fallen for a phishing scam?", "options": [
            "Change your passwords immediately",
            "Ignore the situation and hope it resolves itself",
            "Report it to the phishing site’s customer service",
            "Continue using your account to monitor for unusual activity"],
         "answer": "Change your passwords immediately"},

        {"question_text": "Why should you avoid using public Wi-Fi for logging into sensitive accounts?", "options": [
            "Public Wi-Fi can expose your information to man-in-the-middle attacks",
            "It makes your accounts more secure",
            "It is less likely to be monitored for phishing attempts",
            "Public Wi-Fi networks are designed to prevent phishing"],
         "answer": "Public Wi-Fi can expose your information to man-in-the-middle attacks"},

        {"question_text": "What is 'vishing'?", "options": [
            "Phishing attacks that use voice calls to trick people into sharing personal information",
            "Phishing attacks that occur through email",
            "Phishing attacks via social media",
            "Phishing attacks that target websites with high traffic"],
         "answer": "Phishing attacks that use voice calls to trick people into sharing personal information"},

        {"question_text": "How can attackers disguise a malicious link in a phishing email?", "options": [
            "By using a URL shortener",
            "By embedding the link in an image or button",
            "By using a legitimate-looking URL with a misspelling",
            "All of the above"],
         "answer": "All of the above"},

        {"question_text": "What does 'smishing' refer to?", "options": [
            "Phishing attempts via email",
            "Phishing attempts via text message",
            "Phishing attempts via social media",
            "Phishing attacks that involve fake invoices"],
         "answer": "Phishing attempts via text message"},

        {"question_text": "True or False: You should report phishing attempts to your InfoSec and IT team.", "options": [
            "True",
            "False"],
         "answer": "True"},

        {"question_text": "Which of the following is a common risk of not keeping your software up to date?", "options": [
            "Increased system performance",
            "Exposure to known security vulnerabilities",
            "Reduced software license costs",
            "Faster application load times"],
         "answer": "Exposure to known security vulnerabilities"},

        {"question_text": "What type of information might a phishing attack seek?", "options": [
            "Your favorite movie",
            "Your phone’s wallpaper",
            "Passwords, credit card numbers, or personal information.",
            "Your preferred vacation destination"],
         "answer": "Passwords, credit card numbers, or personal information."},

        {"question_text": "Which of the following is a common sign that a link may be malicious?", "options": [
            "The URL contains a long string of random numbers and letters",
            "The link takes you to a well-known website",
            "The link begins with “https://”",
            "The link ends in '.com'"],
         "answer": "The URL contains a long string of random numbers and letters"},
    ]

    for data in questions_data:
        existing_question = Questions.query.filter_by(
            question_text=data['question_text']).first()
        if not existing_question:
            question = Questions(question_text=data['question_text'],
                                 options=data['options'], answer=data['answer'])
            db.session.add(question)

    users_data = [
        {"email": "tech@kvqaindia.com",
            "username": "tech@kvqaindia", "password": "asdfgh"}
    ]

    for data in users_data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if not existing_user:  # Only insert if email doesn't exist
            user = User(email=data['email'], username=data['username'])
            user.set_password(data['password'])  # Hash the password
            db.session.add(user)

    db.session.commit()


with app.app_context():
    # create_database()
    db.create_all()
    insert_dummy_data()


class EmailTemplate:
    def __init__(self, template_file):

        with open(template_file, 'r') as file:
            self.template = file.read()

    def generate_email(self, sender_name, sender_email, recipient_name, subject):

        email_content = self.template
        email_content = email_content.replace('{{sender_name}}', sender_name)
        email_content = email_content.replace('{{sender_email}}', sender_email)
        email_content = email_content.replace(
            '{{recipient_name}}', recipient_name)
        email_content = email_content.replace('{{subject}}', subject)

        email_content = email_content.replace('\n', '<br>')
        email_content = email_content.replace('\n\n', '</p><p>')
        email_content = f"<p>{email_content}</p>"

        return email_content


@app.route('/')
def home():
    return 'Hello World'


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'message': 'User with this email or username already exists!'}), 409

    new_user = User(email=email, username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    credentials = request.json  # Get JSON data from the request
    username = credentials.get('username')
    password = credentials.get('password')

    user = User.query.filter_by(
        username=username).first()  # Query user by username

    # Verify if user exists and check password
    if user and user.check_password(password):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Correct usage here
        }
        token = jwt.encode(
            payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"message": "Login Successful", "access_token": token}), 200

    return jsonify({"message": "Invalid username or password"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    # JWT is stateless, just inform the client to delete the token
    return jsonify({"message": "Logged out successfully"}), 200


emailed_candidates = []

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():

    request_data = request.json
    selected_department = request_data.get('department')

    if not selected_department:
        return jsonify({'error': 'No department selected'}), 400

    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    signature_image_path = ''

    if selected_department == 'HR, Information Security, Training and TMG':
        with open(os.path.join(templates_dir, 'hr_email_template.html')) as f:
            email_template = f.read()
        action_name = "Update Payroll Information"
        email_subject = "Your Latest RRSP Statement is Ready"
        # signature_image_path = os.path.join('templates', 'hr_signature.jpeg')

    elif selected_department == 'Sales and Marketing, Finance, Admin':
        with open(os.path.join(templates_dir, 'accounts_email_template.html')) as f:
            email_template = f.read()
        action_name = "Update Credentials"
        email_subject = "Reminder: Update Your Credentials for Compliance"
        # signature_image_path = os.path.join(
        #     'templates', 'sales_signature.jpeg')

    elif selected_department == 'Developer and Product Development':
        with open(os.path.join(templates_dir, 'developer_template.html')) as f:
            email_template = f.read()
            action_name = "Download Security Patch"
            email_subject = "Immediate Action Required: Security Patch Deployment for Development Tools"
            # signature_image_path = os.path.join(
            #     'templates', 'product_development_signature.jpeg')

    elif selected_department == 'Leadership':
        with open(os.path.join(templates_dir, 'leadership_template.html')) as f:
            email_template = f.read()
            action_name = "Review Strategic Plan"
            email_subject = "Urgent: Strategic Plan Review for Q4 - Action Required"
            # signature_image_path = os.path.join(
            #     'templates', 'leadership_signature.jpeg')
    # else:
    #     with open(os.path.join(templates_dir, 'email_template.html')) as f:
    #         email_template = f.read()
    #     action_name = "Complete Action"
    #     email_subject = "Action Required: Complete Task"  # Default subject

    
    EmailedCandidate.query.delete()
    db.session.commit()

    colleagues = Colleagues.query.all()

    # from_email = os.getenv('Email_Username')
    # password = os.getenv('Password')

    from_email = os.getenv('Email_Username')
    password = os.getenv('Password')

    # for colleague in colleagues:
    #     # tracking_link = f"https://phishing-mail-application.onrender.com/phishing_test/{colleague.id}"
    #     # tracking_link = f"https://phishing-mail-frontend.vercel.app/phishing_test/{colleague.id}"
    #     # tracking_link = f"http://localhost:8080/phishing_test/{colleague.id}"
    #     tracking_link = f"https://icici-phishing.onrender.com/phish_intermediate/{colleague.id}"
    #     # tracking_link = f"https://phishing-application-demo.vercel.app/phishing_test/{colleague.id}"
    #     # tracking_link = f"http://localhost:8080/phishing_test/{colleague.id}"

    #     print(f"Generated tracking link for {colleague.name}: {tracking_link}")

    #     to_email = colleague.email
    #     msg = MIMEMultipart('related')
    #     msg['Subject'] = email_subject
    #     msg['From'] = from_email
    #     msg['To'] = to_email

    #     body = email_template.replace("{{recipient_name}}", colleague.name)
    #     body = body.replace("{{action_link}}", tracking_link)
    #     body = body.replace("{{action_name}}", action_name)
    #     body = body.replace("{{email_subject}}", email_subject)
    #     body = body.replace("{{department}}", colleague.department)


    #     html_content = f"""
    #     <html>
    #         <body>
    #             {body}
    #         </body>
    #     </html>
    #     """
    #     msg.attach(MIMEText(html_content, 'html'))

    #     # signature_image_path = os.path.join('templates', 'Capture.JPG')
    #     # with open(signature_image_path, 'rb') as img_file:
    #     #     img = MIMEImage(img_file.read())
    #     #     img.add_header('Content-ID', '<signature_image>')
    #     #     msg.attach(img)

    #     # Attach logo image
    #     logo_image_path = os.path.join(templates_dir, 'Icici Bank.png')
    #     with open(logo_image_path, 'rb') as img_file:
    #         img = MIMEImage(img_file.read())
    #         img.add_header('Content-ID', '<logo_image>')
    #         msg.attach(img)

    #     try:
    #         with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #             server.starttls()
    #             server.login(from_email, password)
    #             server.send_message(msg)
    #         print(f"Email sent to {colleague.email}")
    #         # with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
    #         #     server.starttls()
    #         #     server.login(from_email, password)
    #         #     server.send_message(msg)
    #         # print(f"Email sent to {colleague.email}")

    #         # with smtplib.SMTP('smtp.bizmail.yahoo.com', 587) as server:
    #         #     server.starttls()
    #         #     server.login(from_email, password)
    #         #     server.send_message(msg)
    #         # print(f"Email sent to {colleague.email}")

    #         # emailed_candidates.append({
    #         #     'name': colleague.name,
    #         #     'email': colleague.email,
    #         #     'designation': colleague.designation
    #         emailed_candidate = EmailedCandidate(
    #             name=colleague.name,
    #             email=colleague.email,
    #             designation=colleague.designation
    #         )
    #         db.session.add(emailed_candidate)
    #         time.sleep(2)
    #         print("Emailed candidates list after sending:", emailed_candidates)

    #     except Exception as e:
    #         print(f"Failed to send email to {colleague.email}: {str(e)}")
    
    # db.session.commit()

    # return jsonify({'message': 'Phishing emails sent to colleagues.'})

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)

        for colleague in colleagues:
            # Build email message
            msg = MIMEMultipart('related')
            msg['Subject'] = email_subject
            msg['From'] = from_email
            msg['To'] = colleague.email

            tracking_link = f"https://icici-phishing.onrender.com/phish_intermediate/{colleague.id}"
            body = email_template.replace("{{recipient_name}}", colleague.name)
            body = body.replace("{{action_link}}", tracking_link)
            body = body.replace("{{action_name}}", action_name)
            body = body.replace("{{email_subject}}", email_subject)
            body = body.replace("{{department}}", colleague.department)

            print(f"Generated tracking link for {colleague.name}: {tracking_link}")

            html_content = f"<html><body>{body}</body></html>"
            msg.attach(MIMEText(html_content, 'html'))

            logo_image_path = os.path.join(templates_dir, 'Icici Bank.png')
            with open(logo_image_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<logo_image>')
                msg.attach(img)

            server.send_message(msg)

            emailed_candidate = EmailedCandidate(
                name=colleague.name,
                email=colleague.email,
                designation=colleague.designation
            )
            db.session.add(emailed_candidate)

            time.sleep(2)  # Optional: reduce sleep to 0.5s since single connection is more efficient

        server.quit()

    except Exception as e:
        print(f"Failed to send email to {colleague.email}: {str(e)}")

    db.session.commit()
    return jsonify({'message': 'Emails sent.'})


@app.route('/phishing_test/<int:colleague_id>', methods=['GET'])
def phishing_test(colleague_id):
    print(f'Phishing test accessed for colleague ID: {colleague_id}')

    colleague = Colleagues.query.get(colleague_id)
    if not colleague:
        return jsonify({'error': 'Colleague not found.'}), 404

    return jsonify({'message': 'Tracking link accessed successfully', 'colleague_id': colleague_id})
    # return redirect(f'https://kvphishing.netlify.app/phishing_test/{colleague_id}')


@app.route('/generate_emailed_candidates_report', methods=['GET', 'POST'])
def generate_emailed_candidates_report():
    candidates = EmailedCandidate.query.all()

    if not candidates:
        print("No candidates in emailed_candidates:",
              candidates)
        return jsonify({'error': 'No successfully emailed candidates.'}), 400

    print("Generating CSV for:", candidates)

    try:
        csv_file_path = "emailed_candidates_report.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'designation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for c in candidates:
                writer.writerow({
                    'name': c.name,
                    'email': c.email,
                    'designation': c.designation
                })

        return send_file(csv_file_path, as_attachment=True)
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/users')
def users():
    user = Colleagues.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'department': u.department, 'designation': u.designation} for u in user])


@app.route('/phising_click/<int:colleague_id>', methods=['POST'])
def phising_click(colleague_id):
    print(f'Received request for colleague ID: {colleague_id}')
    colleague = Colleagues.query.get(colleague_id)
    if not colleague:
        return jsonify({'error': 'Colleague not found.'}), 404

    report = Reports.query.filter_by(colleague_id=colleague_id).first()
    if report:
        report.clicked = True
    else:
        report = Reports(colleague_id=colleague_id,
                         clicked=True, answered=False, answers={})
        db.session.add(report)
    db.session.commit()

    candidate_data = {
        'id': colleague.id,
        'name': colleague.name,
        'email': colleague.email,
        'department': colleague.department,
        'designation': colleague.designation
    }

    return jsonify({'message': 'Click recorded', 'candidate': candidate_data})


@app.route('/reports', methods=['GET'])
def get_reports():
    reports = Reports.query.all()
    report_data = [{'id': r.id, 'colleague_id': r.colleague_id, 'clicked': r.clicked,
                    'answered': r.answered, 'answers': r.answers, 'status': r.status, 'score': r.score, 'completion_date': r.completion_date} for r in reports]
    return jsonify(report_data)


@app.route('/phishing_opened/<int:colleague_id>', methods=['GET'])
def phishing_opened(colleague_id):
    report = Reports.query.filter_by(colleague_id=colleague_id).first()
    print(
        f'Processing click for colleague ID: {colleague_id} | Existing report: {report}')

    if report:
        report.clicked = True
        print(f'Updated existing report for ID {colleague_id} to clicked=True')
    else:
        report = Reports(colleague_id=colleague_id,
                         clicked=True, answered=False, answers={})
        db.session.add(report)
        print(f'Created new report for ID {colleague_id} with clicked=True')

    db.session.commit()
    return jsonify({'message': 'Thank you for participating in our phishing awareness program.', 'showPopup': True})


def evaluate_answers(submitted_answers, correct_answers, questions):
    score = 0
    total_questions = len(questions)

    for i, submitted_answer in enumerate(submitted_answers):
        question_id = questions[i]['id']  # Get the question ID
        correct_answer = correct_answers.get(question_id, None)

        if correct_answer:
            # Normalize and compare answers
            submitted_answer = str(submitted_answer).strip().lower()
            correct_answer = str(correct_answer).strip().lower()

            print(
                f"Comparing submitted: '{submitted_answer}' with correct: '{correct_answer}'")

            if submitted_answer == correct_answer:
                score += 1

    return (score / total_questions) * 100 if total_questions > 0 else 0

@app.route('/phish_intermediate/<int:colleague_id>', methods=['GET'])
def phish_intermediate(colleague_id):
    colleague = Colleagues.query.get(colleague_id)
    if not colleague:
        return "Invalid link.", 404
    return render_template('intermediate_page.html', colleague_id=colleague_id)



@app.route('/submit_answers/<int:colleague_id>', methods=['POST'])
def submit_answers(colleague_id):
    data = request.get_json()
    report = Reports.query.filter_by(colleague_id=colleague_id).first()

    if report and report.clicked:
        report.answered = True
        report.answers = data['answers']

        # We need to store the correct answers with the corresponding question IDs
        correct_answers = {question['id']: question['answer']
                           for question in data['questions']}  # Using the received questions with answers

        # Evaluate the score using the submitted answers and the corresponding correct answers
        report.score = evaluate_answers(
            data['answers'], correct_answers, data['questions'])
        print(report.score)
        report.status = "Completed" if report.score >= 70 else "Pending"
        report.completion_date = datetime.now()
        db.session.commit()

        # study_material_link = f"http://localhost:8080/study-material/{colleague_id}"
        study_material_link = f"https://icici-phishing.vercel.app/study-material/{colleague_id}"
        # study_material_link = f"https://phishing-application-demo.vercel.app/study-material/{colleague_id}"

        if report.score >= 70:
            subject = "Congratulations on Completing the Training Program!"
            body = f"Dear {report.colleague.name},\n\nYou have successfully completed the training program with a score of {report.score}%."
        else:
            subject = "Reattempt the Training Program"
            body = f"""Dear {report.colleague.name},<br><br>
                    Unfortunately, you did not pass the training program. Please reattempt it by following the link provided:<br><br>
                    <a href="{study_material_link}">Reattempt</a><br><br>
                    Score: {report.score}%."""

        send_result_email(report.colleague.email, subject, body)

        return jsonify({'message': 'Answers submitted successfully.', 'score': report.score})

    return jsonify({'error': 'User did not click the phishing link.'}), 400


@app.route('/generate_reports', methods=['GET', 'POST'])
def generate_reports():
    try:
        reports = Reports.query.all()
        report_data = []

        for report in reports:
            colleague = Colleagues.query.get(report.colleague_id)
            report_entry = {
                'Colleague Name': colleague.name,
                'Colleague Email': colleague.email,
                'Department': colleague.department,
                'Designation': colleague.designation,
                'Link Clicked': 'Yes' if report.clicked else 'No',
                # 'Answered': report.answered,
                'Score': report.score,
                'Status': report.status,
                'Completion Date': report.completion_date.strftime('%Y-%m-%d') if report.completion_date else None,
            }
            report_data.append(report_entry)

        csv_file_path = "candidate_reports.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Colleague Name', 'Colleague Email', 'Department',
                          'Designation', 'Link Clicked', 'Score',
                          'Status', 'Completion Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in report_data:
                writer.writerow(data)

        return send_file(csv_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download_report/<int:colleague_id>', methods=['GET'])
def download_report(colleague_id):
    report = Reports.query.filter_by(colleague_id=colleague_id).first()
    colleague = Colleagues.query.get(colleague_id)

    if not report or not colleague:
        return jsonify({'error': 'Report or colleague not found.'}), 404

    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 770, "Phishing Awareness Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 740, f"Report for: {colleague.name}")
    pdf.drawString(100, 720, f"Email: {colleague.email}")
    pdf.drawString(100, 700, f"Department: {colleague.department}")

    pdf.setLineWidth(1)
    pdf.line(100, 690, 500, 690)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 670, "Phishing Email Status:")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(120, 650, f"Clicked: {'Yes' if report.clicked else 'No'}")
    pdf.drawString(120, 630, f"Answered: {'Yes' if report.answered else 'No'}")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 600, "Answers Provided:")

    pdf.setFont("Helvetica", 12)
    y_position = 580
    if report.answers:
        for i, answer in enumerate(report.answers, start=1):
            pdf.drawString(120, y_position, f"Q{i}: {answer}")
            y_position -= 20
    else:
        pdf.drawString(120, y_position, "No answers submitted")
        y_position -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position - 20, "Overall Performance:")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(120, y_position - 40,
                   f"Score: {report.score if report.score else 0}")

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(100, 50, "Generated on: " +
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    pdf.showPage()
    pdf.save()
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name=f'report_{colleague_id}.pdf', mimetype='application/pdf')

@app.route('/upload_colleagues_data', methods=['POST'])
def upload_colleagues_data():
    try:
        Reports.query.delete()
        # Clear existing data in the colleagues table
        Colleagues.query.delete()  # This will also delete related reports due to cascade delete
        
        file = request.files.get('file')
        if file and file.filename.endswith('.xlsx'):
            # Read Excel file
            df = pd.read_excel(file)
            
            # Check if the expected columns are present in the file
            required_columns = {'Full Name', 'Work Email', 'Department', 'Job Title'}
            if not required_columns.issubset(df.columns):
                return jsonify({'message': 'Invalid file structure. Ensure columns are correct.'}), 400

            # Iterate through each row in the dataframe and add to the database
            for _, row in df.iterrows():
                if pd.isna(row['Full Name']) or pd.isna(row['Work Email']) or pd.isna(row['Department']) or pd.isna(row['Job Title']):
                    continue  # Skip rows with any missing required data

                colleague = Colleagues(
                    name=row['Full Name'],
                    email=row['Work Email'],
                    department=row['Department'],
                    designation=row['Job Title']
                )
                db.session.add(colleague)

            db.session.commit()
            return jsonify({'message': 'Data uploaded successfully'}), 200
        else:
            return jsonify({'message': 'Invalid file format. Please upload an .xlsx file.'}), 400

    except Exception as e:
        db.session.rollback()
        print("Error uploading data:", e)
        return jsonify({'message': f'Error processing file: {str(e)}'}), 500




@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Questions.query.all()
    return jsonify([{
        'id': question.id,
        'question_text': question.question_text,
        'options': question.options,
        'answer': question.answer
    } for question in questions])


@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Questions.query.get(question_id)
    if question:
        return jsonify({
            'id': question.id,
            'question_text': question.question_text,
            'options': question.options,
            'answer': question.answer
        })
    return jsonify({'error': 'Question not found!'}), 404


@app.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    new_question = Questions(
        question_text=data['question_text'],
        options=data['options'],
        answer=data['answer']
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'message': 'Question added!', 'id': new_question.id}), 201


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    print(f"Updating question ID: {question_id}")
    data = request.json
    print(f"Received data: {data}")

    question = Questions.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found!'}), 404

    question.question_text = data['question_text']
    question.options = data['options']
    question.answer = data['answer']
    db.session.commit()
    return jsonify({'message': 'Question updated!'})


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found!'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted!'})

@app.route('/download-certificate/<int:colleague_id>', methods=['GET'])
def download_certificate(colleague_id):
    try:
        # Query the database for the colleague
        colleague = Colleagues.query.get(colleague_id)
        report = Reports.query.filter_by(colleague_id=colleague_id).first()

        if not colleague or report.status != "Completed" or report.score < 70:
            return jsonify({"error": "Certificate not available for this colleague"}), 400

        # Ensure that colleague.name is a string and pass it along with the score
        certificate_path = generate_certificate(colleague.name, report.score)

        if certificate_path is None:
            return jsonify({"error": "Certificate generation failed"}), 500

        # Use send_file with download_name specified
        return send_file(certificate_path, as_attachment=True, mimetype='application/pdf', download_name=f"certificate_{colleague.name}.pdf")

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to download certificate"}), 500


def generate_certificate(candidate_name, score):
    try:
        candidate_name_safe = candidate_name.replace(" ", "_")
        pdf_file_path = f"certificate_{candidate_name_safe}.pdf"

        # Check if the directory exists, create if not
        if not os.path.exists("certificates"):
            os.makedirs("certificates")

        pdf_file_path = os.path.join("certificates", pdf_file_path)

        document = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        styles = getSampleStyleSheet()

        content = []

        title = Paragraph("Certificate of Completion", styles['Title'])
        content.append(title)
        content.append(Spacer(1, 20))

        name = Paragraph(
            f"This certifies that <b>{candidate_name}</b>", styles['Normal'])
        content.append(name)
        content.append(Spacer(1, 20))

        score_paragraph = Paragraph(
            f"Has successfully completed the quiz with a score of <b>{score}%</b>.", styles['Normal'])
        content.append(score_paragraph)
        content.append(Spacer(1, 20))

        footer = Paragraph("Thank you for your participation!", styles['Normal'])
        content.append(footer)

        document.build(content)
        print(f"Generated PDF at: {pdf_file_path}")

        return pdf_file_path

    except Exception as e:
        print(f"Error generating certificate: {e}")
        return None


@app.route('/update_report_status/<colleague_id>', methods=['POST'])
def update_report_status(colleague_id):
    data = request.get_json()
    score = data.get('score')

    if score is None:
        return jsonify({'error': 'Score is required'}), 400

    try:
        # Log the incoming data
        print(
            f"Updating report for colleague_id: {colleague_id} with score: {score}")

        # Fetch the report for the given colleague_id
        report = Reports.query.filter_by(colleague_id=colleague_id).first()

        if report:
            report.score = score
            db.session.commit()
            return jsonify({'message': 'Score updated successfully'})
        else:
            return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        print(f"Error updating report: {e}")  # Log the error to console
        return jsonify({'error': str(e)}), 500


@app.route('/send_result_email', methods=['POST'])
def send_result_email():
    data = request.get_json()

    colleague_email = data.get('colleague_id')
    subject = data.get('subject')
    body = data.get('body')

    if colleague_email and subject and body:
        send_result_email(colleague_email, subject, body)
        return jsonify({'message': 'Email sent successfully.'}), 200
    else:
        return jsonify({'error': 'Missing required fields.'}), 400


def send_result_email(colleague_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = os.getenv('Email_Username')
    password = os.getenv('Password')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = colleague_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, colleague_email, msg.as_string())
        print(f"Email sent to {colleague_email}")

    except Exception as e:
        print(f"Failed to send email to {colleague_email}: {str(e)}")


@app.route('/send_reminder/<int:report_id>', methods=['POST'])
def send_reminder(report_id):
    report = Reports.query.get(report_id)
    if report:

        if report.status in ['Pending', 'Training Completed']:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            from_email = os.getenv('Email_Username')
            password = os.getenv('Password')

            colleague_email = report.colleague.email
            colleague_id = report.colleague_id

            # study_material_link = f"http://localhost:8080/study-material/{colleague_id}"
            study_material_link = f"https://icici-phishing.vercel.app/study-material/{colleague_id}"
            # study_material_link = f"https://phishing-application-demo.vercel.app/study-material/{colleague_id}"

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = colleague_email
            msg['Subject'] = "Reminder: Complete Your Training"

            # body = f"Dear {report.colleague.name},\n\nThis is a reminder to complete your training."

            body = f"""
            Dear {report.colleague.name},<br><br>
            This is a reminder to complete your training.<br><br>
            Please click the link below to access the study material:<br>
            <a href="{study_material_link}">Study Material</a><br><br>
            """
            msg.attach(MIMEText(body, 'html'))

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(from_email, password)
                    server.send_message(msg)
                return jsonify({"message": "Reminder email sent successfully!"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"message": "Status is not Pending or Training Completed."}), 400
    else:
        return jsonify({"message": "Report not found."}), 404


@app.route('/get_random_questions', methods=['GET'])
def get_random_questions():
    try:
        # Fetch 10 random questions from the database
        questions = Questions.query.order_by(func.random()).limit(10).all()
        questions_data = [{
            'id': question.id,
            'question_text': question.question_text,
            'options': question.options,
            'answer': question.answer
        } for question in questions]

        return jsonify({'questions': questions_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_all_reports', methods=['GET'])
def get_all_reports():
    try:
        reports = Reports.query.all()
        report_data = [{'id': r.id, 'colleague_id': r.colleague_id, 'clicked': r.clicked,
                        'answered': r.answered, 'answers': r.answers, 'status': r.status, 'score': r.score, 'completion_date': r.completion_date} for r in reports]
        return jsonify({'reports': report_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_colleagues_data', methods=['Delete'])
def delete_colleagues_data():
    try:
        num_deleted = Colleagues.query.delete()
        db.session.commit()
        return jsonify({"message": "Colleagues data successfully deleted."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# @app.route('/generate_reports_pdf', methods=['GET'])
# def generate_reports_reportlab():
#     try:
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=A4)
#         elements = []

#         styles = getSampleStyleSheet()
#         title_style = styles['Title']
#         normal_style = styles['Normal']

#         elements.append(Paragraph("Monthly Phishing Simulation Report", title_style))
#         elements.append(Spacer(1, 12))
#         elements.append(Paragraph("Document Classification: Company Confidential", normal_style))
#         elements.append(Spacer(1, 20))

#         reports = Reports.query.all()
#         fail_count = Reports.query.filter_by(clicked=True).count()
#         pass_count = len(reports) - fail_count
#         clicked_only = Reports.query.filter(Reports.clicked == True, Reports.answered == False).count()
#         clicked_and_answered = Reports.query.filter(Reports.clicked == True, Reports.answered == True).count()
#         repeat_offender = db.session.query(Reports.colleague_id).filter_by(clicked=True).group_by(Reports.colleague_id).having(func.count(Reports.id) > 1).count()

#         # Total Recipients from database
#         total_recipients = EmailedCandidate.query.count()

#         summary_data = [
#             ["Total Recipients (Emailed)", total_recipients],
#             ["Fail", fail_count],
#             ["Pass", pass_count],
#             ["Clicked Only", clicked_only],
#             ["Clicked & Submitted Data", clicked_and_answered],
#             ["Repeat Offender", repeat_offender]
#         ]
#         summary_table = Table(summary_data, hAlign='LEFT')
#         summary_table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#         ]))
#         elements.append(summary_table)
#         elements.append(Spacer(1, 20))

#         drawing = Drawing(200, 150)
#         pie = Pie()
#         pie.x = 65
#         pie.y = 20
#         pie.width = 120
#         pie.height = 120
#         pie.data = [fail_count, pass_count]
#         pie.labels = ['Fail', 'Pass']
#         pie.slices.strokeWidth = 0.5
#         pie.slices[0].fillColor = colors.red
#         pie.slices[1].fillColor = colors.green

#         drawing.add(pie)
#         elements.append(drawing)
#         elements.append(Spacer(1, 20))

#         elements.append(Paragraph("Detailed Candidate Reports", styles['Heading2']))
#         elements.append(Spacer(1, 12))

#         report_data = [["ID", "Colleague Name", "Link Clicked", "Training Completed", "Score", "Status", "Completion Date"]]
#         for report in reports:
#             colleague = Colleagues.query.get(report.colleague_id)
#             row = [
#                 str(report.id),
#                 colleague.name,
#                 'Yes' if report.clicked else 'No',
#                 'Yes' if report.answered else 'No',
#                 f"{report.score}%" if report.score is not None else "0%",
#                 report.status,
#                 report.completion_date.strftime('%Y-%m-%d') if report.completion_date else "-"
#             ]
#             report_data.append(row)

#         candidate_table = Table(report_data, repeatRows=1, hAlign='LEFT')
#         candidate_table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#         ]))
#         elements.append(candidate_table)

#         doc.build(elements)
#         buffer.seek(0)

#         return send_file(buffer, as_attachment=True, download_name="Phishing_Report_ReportLab.pdf", mimetype='application/pdf')

#     except Exception as e:
#         print({"Error": str(e)})
#         return {'error': str(e)}, 500


# @app.route('/generate_reports_pdf', methods=['GET'])
# def generate_reports_reportlab():
#     try:
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=A4)
#         elements = []

#         styles = getSampleStyleSheet()
#         title_style = styles['Title']
#         normal_style = styles['Normal']

#         elements.append(Paragraph("Monthly Phishing Simulation Report", title_style))
#         elements.append(Spacer(1, 12))
#         elements.append(Paragraph("Document Classification: Company Confidential", normal_style))
#         elements.append(Spacer(1, 20))

#         # 📊 Metrics Calculation
#         total_recipients = EmailedCandidate.query.count()
#         clicked_count = Reports.query.filter_by(clicked=True).count()
#         completed_count = Reports.query.filter(Reports.clicked==True, Reports.answered==True).count()
#         fail_count = completed_count
#         pass_count = total_recipients - fail_count

#         # 📊 1. Emailed vs Clicked
#         drawing1 = Drawing(200, 150)
#         pie1 = Pie()
#         pie1.x = 65
#         pie1.y = 20
#         pie1.width = 120
#         pie1.height = 120
#         pie1.data = [clicked_count, total_recipients - clicked_count]
#         pie1.labels = ['Clicked', 'Not Clicked']
#         pie1.slices[0].fillColor = colors.orange
#         pie1.slices[1].fillColor = colors.green
#         drawing1.add(pie1)
#         elements.append(Paragraph("Emailed Candidates: Clicked vs Not Clicked", styles['Heading3']))
#         elements.append(drawing1)
#         elements.append(Spacer(1, 20))

#         # 📊 2. Clicked vs Completed
#         drawing2 = Drawing(200, 150)
#         pie2 = Pie()
#         pie2.x = 65
#         pie2.y = 20
#         pie2.width = 120
#         pie2.height = 120
#         pie2.data = [completed_count, clicked_count - completed_count]
#         pie2.labels = ['Completed Data Entry', 'Only Clicked']
#         pie2.slices[0].fillColor = colors.red
#         pie2.slices[1].fillColor = colors.orange
#         drawing2.add(pie2)
#         elements.append(Paragraph("Clicked: Submitted Data vs Only Clicked", styles['Heading3']))
#         elements.append(drawing2)
#         elements.append(Spacer(1, 20))

#         # 📊 3. Pass vs Fail
#         drawing3 = Drawing(200, 150)
#         pie3 = Pie()
#         pie3.x = 65
#         pie3.y = 20
#         pie3.width = 120
#         pie3.height = 120
#         pie3.data = [fail_count, pass_count]
#         pie3.labels = ['Fail (Clicked & Submitted)', 'Pass']
#         pie3.slices[0].fillColor = colors.red
#         pie3.slices[1].fillColor = colors.green
#         drawing3.add(pie3)
#         elements.append(Paragraph("Overall Results: Pass vs Fail", styles['Heading3']))
#         elements.append(drawing3)
#         elements.append(Spacer(1, 20))

#         # 📋 Summary Table
#         summary_data = [
#             ["Total Emailed", total_recipients],
#             ["Clicked", clicked_count],
#             ["Completed", completed_count],
#             ["Fail", fail_count],
#             ["Pass", pass_count]
#         ]
#         summary_table = Table(summary_data, hAlign='LEFT')
#         summary_table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#         ]))
#         elements.append(summary_table)
#         elements.append(Spacer(1, 20))

#         # 📋 Detailed Candidate Reports Table
#         reports = Reports.query.all()
#         report_data = [["ID", "Colleague Name", "Clicked", "Completed", "Score", "Status", "Date"]]
#         for report in reports:
#             colleague = Colleagues.query.get(report.colleague_id)
#             row = [
#                 str(report.id),
#                 colleague.name,
#                 'Yes' if report.clicked else 'No',
#                 'Yes' if report.answered else 'No',
#                 f"{report.score}%" if report.score is not None else "0%",
#                 report.status,
#                 report.completion_date.strftime('%Y-%m-%d') if report.completion_date else "-"
#             ]
#             report_data.append(row)

#         candidate_table = Table(report_data, repeatRows=1, hAlign='LEFT')
#         candidate_table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
#             ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#         ]))
#         elements.append(Paragraph("Detailed Candidate Reports", styles['Heading2']))
#         elements.append(Spacer(1, 12))
#         elements.append(candidate_table)

#         doc.build(elements)
#         buffer.seek(0)

#         return send_file(buffer, as_attachment=True, download_name="Phishing_Report_ReportLab.pdf", mimetype='application/pdf')

#     except Exception as e:
#         print({"Error": str(e)})
#         return {'error': str(e)}, 500

# def generate_pie_chart(data, labels, colors):
#     fig, ax = plt.subplots()
#     ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
#     ax.axis('equal')
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close(fig)
#     buffer.seek(0)
#     img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
#     return img_base64

# @app.route('/generate_reports_pdf', methods=['GET'])
# def generate_styled_report():
#     # Query reports
#     reports = Reports.query.all()
#     total_recipients = EmailedCandidate.query.count()
#     fail_count = Reports.query.filter_by(clicked=True).count()
#     pass_count = len(reports) - fail_count
#     clicked_only = Reports.query.filter(Reports.clicked==True, Reports.answered==False).count()
#     clicked_and_answered = Reports.query.filter(Reports.clicked==True, Reports.answered==True).count()
#     repeat_offender = db.session.query(Reports.colleague_id).filter_by(clicked=True).group_by(Reports.colleague_id).having(func.count(Reports.id) > 1).count()

#     # Summary Table
#     summary = [
#         {'label': 'Total Recipients (Emailed)', 'value': total_recipients},
#         {'label': 'Fail', 'value': fail_count},
#         {'label': 'Pass', 'value': pass_count},
#         {'label': 'Clicked Only', 'value': clicked_only},
#         {'label': 'Clicked & Submitted Data', 'value': clicked_and_answered},
#         {'label': 'Repeat Offender', 'value': repeat_offender}
#     ]

#     # Generate 3 Pie Charts
#     chart1 = generate_pie_chart([fail_count, pass_count], ['Fail', 'Pass'], ['#e74c3c', '#2ecc71'])
#     chart2 = generate_pie_chart([clicked_only, clicked_and_answered], ['Clicked Only', 'Clicked & Submitted'], ['#f39c12', '#3498db'])
#     chart3 = generate_pie_chart([len(reports)-fail_count, fail_count], ['Did Not Click', 'Clicked'], ['#2ecc71', '#e74c3c'])

#     charts = [chart1, chart2, chart3]

#     # Candidate Report Table
#     candidate_reports = []
#     for report in reports:
#         colleague = Colleagues.query.get(report.colleague_id)
#         candidate_reports.append({
#             'id': report.id,
#             'name': colleague.name,
#             'clicked': 'Yes' if report.clicked else 'No',
#             'answered': 'Yes' if report.answered else 'No',
#             'score': f"{report.score}%" if report.score else '0%',
#             'status': report.status,
#             'completion_date': report.completion_date.strftime('%Y-%m-%d') if report.completion_date else '-'
#         })

#     # Render HTML
#     rendered_html = render_template(
#         'phishing_report.html',
#         summary=summary,
#         charts=charts,
#         reports=candidate_reports
#     )

#     # Convert to PDF
#     pdf = HTML(string=rendered_html).write_pdf()

#     # Serve PDF
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'inline; filename=styled_report.pdf'
#     return response

def generate_pie_chart(data, labels, colors):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64

# @app.route('/generate_reports_pdf')
# def generate_styled_report():
#     reports = Reports.query.all()
#     total_recipients = EmailedCandidate.query.count()
#     fail_count = Reports.query.filter_by(clicked=True).count()
#     did_not_click_count = total_recipients - fail_count
#     pass_count = len(reports) - fail_count
#     clicked_only = Reports.query.filter(Reports.clicked == True, Reports.answered == False).count()
#     clicked_and_answered = Reports.query.filter(Reports.clicked == True, Reports.answered == True).count()
#     repeat_offender = db.session.query(Reports.colleague_id).filter_by(clicked=True).group_by(Reports.colleague_id).having(func.count(Reports.id) > 1).count()

#     summary = [
#         {'label': 'Total Recipients (Emailed)', 'value': total_recipients},
#         {'label': 'Fail', 'value': fail_count},
#         {'label': 'Pass', 'value': pass_count},
#         {'label': 'Clicked Only', 'value': clicked_only},
#         {'label': 'Clicked & Submitted Data', 'value': clicked_and_answered},
#         {'label': 'Repeat Offender', 'value': repeat_offender}
#     ]

#     # 3 charts: Pass/Fail, Clicked vs Not, Clicked Only vs Clicked&Submitted
#     chart1 = generate_pie_chart([fail_count, pass_count], ['Fail', 'Pass'], ['#e74c3c', '#2ecc71'])
#     chart2 = generate_pie_chart([clicked_only, clicked_and_answered], ['Clicked Only', 'Clicked & Submitted'], ['#f39c12', '#3498db'])
#     # chart3 = generate_pie_chart([len(reports) - fail_count, fail_count], ['Did Not Click', 'Clicked'], ['#2ecc71', '#e74c3c'])
#     chart3 = generate_pie_chart(
#         [did_not_click_count, fail_count],
#         ['Did Not Click', 'Clicked'],
#         ['#2ecc71', '#e74c3c']
#     )
#     charts = [chart1, chart2, chart3]

#     candidate_reports = []
#     for report in reports:
#         colleague = Colleagues.query.get(report.colleague_id)
#         candidate_reports.append({
#             'id': report.id,
#             'name': colleague.name if colleague else 'Unknown',
#             'clicked': 'Yes' if report.clicked else 'No',
#             'answered': 'Yes' if report.answered else 'No',
#             'score': f"{report.score}%" if report.score else '0%',
#             'status': report.status,
#             'completion_date': report.completion_date.strftime('%Y-%m-%d') if report.completion_date else '-'
#         })

#     company_logo_path = os.path.abspath(os.path.join('static', 'Xploit2Secure.png'))
#     company_logo_path = company_logo_path.replace('\\', '/')
#     company_logo_url = f'file:///{company_logo_path}'
#     print(f"Company logo absolute file URL: {company_logo_url}")
#     rendered_html = render_template(
#         'phishing_report.html',
#         summary=summary,
#         charts=charts,
#         reports=candidate_reports,
#         company_logo=company_logo_url
#     )

#     # pdf = HTML(string=rendered_html).write_pdf()
#     pdf = HTML(string=rendered_html, base_url=os.path.abspath(".")).write_pdf()
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'inline; filename=styled_report.pdf'
#     return response

@app.route('/generate_reports_pdf')
def generate_styled_report():
    from sqlalchemy import or_, and_

    # Total number of candidates emailed
    total_recipients = EmailedCandidate.query.count()

    # Fetch all reports
    reports = Reports.query.all()

    # Number of people who clicked the link
    click_count = Reports.query.filter_by(clicked=True).count()

    # Number of people who did not click
    not_clicked_count = total_recipients - click_count

    # ✅ Chart 1: Of those who clicked — Pass (Completed + Score ≥ 60) vs Fail/Pending
    pass_count = Reports.query.filter(
        Reports.clicked == True,
        Reports.answered == True,
        Reports.status == 'Completed',
        Reports.score >= 60
    ).count()

    fail_pending_count = Reports.query.filter(
        Reports.clicked == True
    ).filter(
        or_(
            Reports.status == 'Pending',
            and_(Reports.status == 'Completed', Reports.score < 60)
        )
    ).count()

    chart1 = generate_pie_chart(
        [pass_count, fail_pending_count],
        ['Pass (Score ≥ 60%)', 'Fail/Pending'],
        ['#2ecc71', '#e74c3c']
    )

    # ✅ Chart 2: Clicked & Submitted vs Clicked Only (regardless of score)
    clicked_and_answered = Reports.query.filter(Reports.clicked == True, Reports.answered == True).count()
    clicked_only = Reports.query.filter(Reports.clicked == True, Reports.answered == False).count()

    chart2 = generate_pie_chart(
        [clicked_only, clicked_and_answered],
        ['Clicked Only', 'Clicked & Submitted'],
        ['#f39c12', '#3498db']
    )

    # ✅ Chart 3: Out of total emailed — Did Not Click vs Clicked
    chart3 = generate_pie_chart(
        [not_clicked_count, click_count],
        ['Did Not Click', 'Clicked'],
        ['#2ecc71', '#e74c3c']
    )

    charts = [chart1, chart2, chart3]

    # ✅ Repeat offenders — those who clicked multiple times
    repeat_offender = (
        db.session.query(Reports.colleague_id)
        .filter_by(clicked=True)
        .group_by(Reports.colleague_id)
        .having(func.count(Reports.id) > 1)
        .count()
    )

    # ✅ Summary Data for report header
    summary = [
        {'label': 'Total Recipients (Emailed)', 'value': total_recipients},
        {'label': 'Clicked', 'value': click_count},
        {'label': 'Pass (Score ≥ 60%)', 'value': pass_count},
        {'label': 'Fail/Pending', 'value': fail_pending_count},
        {'label': 'Clicked Only', 'value': clicked_only},
        {'label': 'Clicked & Submitted Data', 'value': clicked_and_answered},
        {'label': 'Repeat Offender', 'value': repeat_offender}
    ]

    # ✅ Candidate-wise detailed report
    candidate_reports = []
    for report in reports:
        colleague = Colleagues.query.get(report.colleague_id)
        candidate_reports.append({
            'id': report.id,
            'name': colleague.name if colleague else 'Unknown',
            'clicked': 'Yes' if report.clicked else 'No',
            'answered': 'Yes' if report.answered else 'No',
            'score': f"{report.score}%" if report.score else '0%',
            'status': report.status,
            'completion_date': report.completion_date.strftime('%Y-%m-%d') if report.completion_date else '-'
        })

    company_logo_path = os.path.abspath(os.path.join('static', 'Xploit2Secure.png'))
    company_logo_path = company_logo_path.replace('\\', '/')
    company_logo_url = f'file:///{company_logo_path}'
    print(f"Company logo absolute file URL: {company_logo_url}")

    # ✅ Render HTML template with summary, charts, and reports
    rendered_html = render_template(
        'phishing_report.html',
        summary=summary,
        charts=charts,
        reports=candidate_reports,
        logo_path=company_logo_url
    )

    # ✅ Convert HTML to PDF
    pdf = HTML(string=rendered_html).write_pdf()

    # ✅ Return PDF as inline response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=styled_report.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template, request, Blueprint
from flask import Blueprint
from banking_system.models import BankMember

main = Blueprint('main', __name__)

# @app.route is decorator and / is route-page
@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='homepage')

@main.route("/about")
def about():
    bank_member = BankMember.query.all()
    return render_template('about.html', title='about-bank',bank_member=bank_member)

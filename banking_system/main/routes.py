from flask import render_template
from flask import Blueprint
from banking_system.models import BankMember

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    """
        main home page
        render the home.html template with few static data
    """
    return render_template('home.html', title='homepage')

@main.route("/about")
def about():
    """
            main about page
            render the about.html template to show all bank member list data
    """
    bank_member = BankMember.query.all()
    return render_template('about.html', title='about-bank',bank_member=bank_member)

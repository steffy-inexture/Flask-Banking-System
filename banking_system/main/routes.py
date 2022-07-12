from flask import render_template, request, Blueprint
# from flaskblog.models import Post
from flask import Blueprint

from banking_system.models import BankMember

main = Blueprint('main', __name__)


# @app.route is decorator and / is routepage
@main.route("/")
@main.route("/home")
def home():
    # print("dsfghjk")
    return render_template('home.html', title='homepage')
    # page= request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # return render_template('home.html', posts = posts)

@main.route("/about")
def about():
    bank_member = BankMember.query.all()
    return render_template('about.html', title='about-bank',bank_member=bank_member)

from flask import render_template
from flask import Blueprint

about = Blueprint('about', __name__)


@about.route("/money")
def money():
    """ render the money.html template to show static data """

    return render_template('money.html', title='money')


@about.route("/fixed-deposits")
def fd():
    """ render the fd.html template to show static data """

    return render_template('fd.html', title='fixed-deposits')


@about.route("/loan")
def loan():
    """ render the loan.html template to show static data """

    return render_template('loan.html', title='loan')


@about.route("/insurance")
def insurance():
    """ render the insurance.html template to show static data """

    return render_template('insurance.html', title='insurance')

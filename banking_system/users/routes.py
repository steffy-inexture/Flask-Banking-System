import subprocess
from os.path import exists

import pdfkit
from flask import render_template, url_for, flash, redirect, request, Blueprint, session, make_response
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
from banking_system import db, bcrypt
from banking_system.models import Account, Branch, Card, FixedDeposit, Insurance, Loan, \
    Transaction, TransactionType, User, LoanDetails, InsuranceDetails, OtpByMail
from banking_system.users.forms import AddMoney, RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, \
    ResetPasswordForm, ApplyLoanForm, TransferMoney, ChangeBranch, ApplyInsuranceForm, OtpCheck
from banking_system.users.utils import send_reset_email, send_otp_email, role_assign, add_loan_type, \
    insurance_type, add_transaction_type
import random
import datetime
from banking_system.users.constants import FLASH_MESSAGES, NEW_USER_ADDED, SUCCESSFUL_REGISTRATION, \
    ADMIN_NOT_ACTIVATE_UR_ACCOUNT, SUCCESSFUL_LOGIN, UNSUCCESSFUL_LOGIN, LOGOUT_SUCCESS, ACCOUNT_UPDATED, EMAIL_INFO, \
    INVALID_TOKEN, PASSWORD_UPDATED, ACCOUNT_ALREADY_EXISTED, ACCOUNT_CREATED, LOGIN_FIRST, ALREADY_CARD_EXISTED, \
    CARD_CREATED, TRANSACTION_SUCCESSFULLY, CANT_TRANSFER, \
    PASSWORD_INCORRECT, INSUFFICIENT_BALANCE, PENDING_ACTIVITY, SUCCESS_ACTIVITY, BRANCH_CHANGED, ERROR

users = Blueprint('users', __name__)


# registration route to register user
@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.user_name.data,
        user_password = form.user_password.data,
        user_email = form.user_email.data,
        user_phone_number = form.user_phone_number.data,
        user_first_name = form.user_first_name.data,
        user_last_name = form.user_last_name.data,
        user_address = form.user_address.data,
        user_age = form.user_age.data,
        date_of_birth = form.date_of_birth.data
        user = User(user_name=user_name, user_password=user_password, user_email=user_email,
                    user_phone_number=user_phone_number, user_first_name=user_first_name, user_last_name=user_last_name,
                    user_address=user_address, user_age=user_age, date_of_birth=date_of_birth)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            flash(f'{e}', FLASH_MESSAGES['FAIL'])
        user = User.query.filter_by(user_email=form.user_email.data).first()
        role_assign(user.user_id)
        account_creation(user.user_id)
        if current_user.is_authenticated:
            if current_user.user_email == 'steffy.inexture@gmail.com':
                flash(NEW_USER_ADDED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_dashboard'))
        flash(SUCCESSFUL_REGISTRATION, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# create the bank account at the initial stage
@users.route("/account-creation", methods=['GET', 'POST'])
def account_creation(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    branch = Branch.query.first()
    branch_id = branch.branch_id
    account = db.session.query(func.max(Account.account_number)).first()
    if account[0]:
        account_number = account[0] + 1
    else:
        account_number = 1000000
    account = Account(account_number=account_number, user_id=user.user_id, branch_id=branch_id, account_balance=5000)
    db.session.add(account)
    db.session.commit()

# for change the account selected default first branch
@users.route("/change_branch", methods=['GET', 'POST'])
@login_required
def change_branch():
    user = User.query.filter_by(user_id=current_user.user_id).first()
    account = Account.query.filter_by(user_id=current_user.user_id).first()
    branches = Branch.query.all()
    form = ChangeBranch()
    if form.validate_on_submit():
        print("this is branch selected by the user: ", form.myField.data)
        selected_branch = form.myField.data
        branch = Branch.query.filter_by(branch_name=selected_branch).first()
        if branch:
            account.branch_id = branch.branch_id
            db.session.commit()
            flash(BRANCH_CHANGED, FLASH_MESSAGES['SUCCESS'])
        else:
            flash(ERROR, FLASH_MESSAGES['FAIL'])
        return redirect(url_for('users.dashboard'))
    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name
        form.account_number.data = account.account_number
        form.myField.choices = [i.branch_name for i in Branch.query.all()]
    return render_template('change_branch.html', user=user, account=account, branches=branches, form=form)


# Login route to log in registered user to the website
@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        account = Account.query.filter_by(user_id=user.user_id).first()
        if account:
            if account.account_status == 'Inactive':
                flash(ADMIN_NOT_ACTIVATE_UR_ACCOUNT, FLASH_MESSAGES['FAIL'])
                return redirect(url_for('users.login'))
            elif account.account_status == 'Active':
                if user is not None and form.user_password.data == user.user_password:
                    login_user(user, remember=form.remember.data)
                    flash(SUCCESSFUL_LOGIN, FLASH_MESSAGES['SUCCESS'])
                    return redirect(url_for('users.dashboard'))
                else:
                    flash(UNSUCCESSFUL_LOGIN, FLASH_MESSAGES['FAIL'])
    return render_template('login.html', title='login', form=form)

# User dashboard to show all the functionalities which is performed by the user only
@users.route("/user-dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    account = Account.query.filter_by(user_id=current_user.user_id).first()
    if account:
        card = Card.query.filter_by(account_number=account.account_number).first()

        transaction = Transaction.query.filter(
            (Transaction.receiver_id == current_user.user_id) |
            (Transaction.sender_id == current_user.user_id)
        ).all()
        transaction_type = TransactionType.query.all()
        loan = Loan.query.filter_by(user_id=account.user_id).first()
        insurance = Insurance.query.filter_by(user_id=account.user_id).first()

        fixed_deposit = FixedDeposit.query.filter_by(account_number=account.account_number).first()
        return render_template(
            'user_dashboard.html',
            title='user_dashboard',
            account=account, card=card,
            loan=loan,
            insurance=insurance,
            fixed_deposit=fixed_deposit,
            transaction=transaction,
            transaction_type=transaction_type)


# logout route to log out the session after login and all procedure
@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash(LOGOUT_SUCCESS, FLASH_MESSAGES['SUCCESS'])
    return redirect(url_for('main.home'))


# Profile route to see the personal data of any user
@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.user_name = form.user_name.data
        current_user.user_phone_number = form.user_phone_number.data
        current_user.user_first_name = form.user_first_name.data
        current_user.user_last_name = form.user_last_name.data
        current_user.user_address = form.user_address.data
        current_user.user_age = form.user_age.data
        current_user.date_of_birth = form.date_of_birth.data
        db.session.commit()
        flash(ACCOUNT_UPDATED, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.dashboard'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.user_phone_number.data = current_user.user_phone_number
        form.user_first_name.data = current_user.user_first_name
        form.user_last_name.data = current_user.user_last_name
        form.user_address.data = current_user.user_address
        form.user_age.data = current_user.user_age
        form.date_of_birth.data = current_user.date_of_birth
        form.user_email.data = current_user.user_email

    return render_template('user_profile.html', title='Account', form=form)

# reset password request for the ser
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        send_reset_email(user)
        flash(EMAIL_INFO, FLASH_MESSAGES['INFO'])
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash(INVALID_TOKEN, FLASH_MESSAGES['WARNING'])
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user.user_password = hashed_password
        user.user_password = form.user_password.data
        db.session.commit()
        flash(PASSWORD_UPDATED, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/request-account", methods=['GET', 'POST'])
def request_account():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id)
        if account:
            flash(ACCOUNT_ALREADY_EXISTED, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
        else:
            user = User.query.filter_by(user_id=current_user.user_id).first()
            branch = Branch.query.first()
            branch_id = branch.branch_id
            account = db.session.query(func.max(Account.account_number)).first()
            if account[0]:
                account_number = account[0] + 1
            else:
                account_number = 1000000
            account = Account(account_number=account_number, user_id=user.user_id, branch_id=branch_id)
            db.session.add(account)
            db.session.commit()
            flash(ACCOUNT_CREATED, FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# Request for the card if not have carded yet
@users.route("/request-card", methods=['GET', 'POST'])
@login_required
def request_card():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id).first()
        if account:
            card = Card.query.filter_by(account_number=account.account_number).first()
            if card:
                flash(ALREADY_CARD_EXISTED, FLASH_MESSAGES['FAIL'])
                return redirect(url_for('users.dashboard'))
            else:
                user = User.query.filter_by(user_id=current_user.user_id).first()
                account = Account.query.filter_by(user_id=user.user_id).first()
                card = db.session.query(func.max(Card.card_number)).first()
                if card[0]:
                    card_number = card[0] + 1
                else:
                    card_number = 10000
                cvv_number = random.randint(111, 999)
                card_pin = random.randint(1111, 9999)
                expiry_date = datetime.datetime(2026, 7, 19, 12, 0, 0)
                account_number = account.account_number
                card = Card(card_number=card_number, cvv_number=cvv_number, card_pin=card_pin, expiry_date=expiry_date,
                            account_number=account_number)
                db.session.add(card)
                db.session.commit()
                flash(CARD_CREATED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('users.dashboard'))
        else:
            account_creation()
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# apply for loan via this route [ request goes to admin panel with INACTIVE STATUS]
# giving the PERSONAL/EDUCATION/HOME/OTHER loan option right now
@users.route("/apply-for-loan", methods=['GET', 'POST'])
@login_required
def apply_loan():
    form = ApplyLoanForm()
    user = User.query.filter_by(user_id=current_user.user_id).first()
    if form.validate_on_submit():
        loan = Loan.query.filter_by(user_id=user.user_id).first()
        if loan:
            flash(PENDING_ACTIVITY.format(activity='LOAN'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
        else:
            loan_amount = form.loan_amount_choices.data
            rate_interest = form.loan_rate_interests.data
            if loan_amount == '1':
                loan_amount = '1000'
            elif loan_amount == '2':
                loan_amount = '5000'
            elif loan_amount == '3':
                loan_amount = '10000'
            else:
                loan_amount = '15000'

            if rate_interest == '1':
                rate_interest = '6.5'
            else:
                rate_interest = '6.7'

            loan_type = form.loan_type.data
            loan = Loan(user_id=user.user_id, loan_amount=loan_amount, rate_interest=rate_interest)
            db.session.add(loan)
            db.session.commit()
            loan_ = Loan.query.filter_by(user_id=user.user_id).first()
            add_loan_type(loan_type, loan_.loan_id)
            flash(SUCCESS_ACTIVITY.format(activity='loan'), FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))

    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name
        form.loan_type.choices = [i.loan_name for i in LoanDetails.query.all()]

    return render_template(
        'applyloan.html',
        user_id=current_user.user_id,
        user_name=current_user.user_name,
        title='apply for loan',
        form=form
    )


# Request for insurance requested to admin panel with INACTIVE STATUS
@users.route("/request-insurance", methods=['GET', 'POST'])
@login_required
def request_insurance():
    form = ApplyInsuranceForm()
    user = User.query.filter_by(user_id=current_user.user_id).first()
    if form.validate_on_submit():
        insurance = Insurance.query.filter_by(user_id=user.user_id).first()
        if insurance:
            flash(PENDING_ACTIVITY.format(activity='LOAN'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
        else:
            insurance_amount = form.insurance_amount_choices.data
            if insurance_amount == '1':
                insurance_amount = '1000'
            elif insurance_amount == '2':
                insurance_amount = '5000'
            elif insurance_amount == '3':
                insurance_amount = '10000'
            else:
                insurance_amount = '15000'

            insurance_type_ = form.insurance_type.data

            insurance = Insurance(user_id=user.user_id, insurance_amount=insurance_amount)
            db.session.add(insurance)
            db.session.commit()
            insurance_type(insurance_type_)
            flash(SUCCESS_ACTIVITY.format(activity='Insurance'), FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))

    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name
        form.insurance_type.choices = [i.insurance_name for i in InsuranceDetails.query.all()]

    return render_template(
        'applyinsurance.html',
        user_id=current_user.user_id,
        user_name=current_user.user_name,
        title='apply for insurance',
        form=form
    )


# add fixed deposit
@users.route("/add_fixed_deposit", methods=['GET', 'POST'])
@login_required
def add_fixed_deposit():
    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id).first()
        fixed_deposit = FixedDeposit(account_number=account.account_number)
        db.session.add(fixed_deposit)
        db.session.commit()
        flash(SUCCESS_ACTIVITY.format(activity='FIXED DEPOSIT'), FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('users.dashboard'))
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')


# add_money
@users.route("/add-money", methods=['GET', 'POST'])
@login_required
def add_money():
    form = AddMoney()
    if form.validate_on_submit():
        if form.user_password.data == current_user.user_password:
            account = Account.query.filter_by(user_id=current_user.user_id).first()
            reciver_account_number = form.reciver_account.data
            reciever = Account.query.filter_by(account_number=reciver_account_number).first()
            transaction_amount = form.credit_amount.data
            receiver_id = reciever.user_id
            sender_id = current_user.user_id
            print(transaction_amount)
            print(account.account_balance)
            if transaction_amount <= account.account_balance:
                if receiver_id != account.user_id:
                    reciever.account_balance += transaction_amount
                    account.account_balance -= transaction_amount
                    transaction = Transaction(
                        transaction_amount=transaction_amount,
                        receiver_id=receiver_id,
                        sender_id=sender_id,
                        user_id=sender_id
                    )

                    db.session.add(transaction)
                    db.session.commit()
                    flash(TRANSACTION_SUCCESSFULLY, FLASH_MESSAGES['SUCCESS'])
                    transaction_id = transaction.transaction_id
                    transaction_type = 'debit'
                    add_transaction_type(transaction_type, transaction_id)
                    return redirect(url_for('users.dashboard'))
                else:
                    flash(CANT_TRANSFER, FLASH_MESSAGES['FAIL'])
                    return redirect(url_for('users.add_money'))
            else:
                flash(INSUFFICIENT_BALANCE.format(data=account.account_balance), FLASH_MESSAGES['FAIL'])
                return redirect(url_for('users.add_money'))
        else:
            flash(PASSWORD_INCORRECT, FLASH_MESSAGES['FAIL'])
            return render_template('add_money.html', title='add_money', form=form)
    return render_template('add_money.html', title='add_money', form=form)


# transfer money
@users.route("/Transfer-money", methods=['GET', 'POST'])
@login_required
def transfer_money():
    user = User.query.filter_by(user_id=current_user.user_id).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
    loan = Loan.query.filter_by(user_id=user.user_id).first()
    fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()

    form = TransferMoney()

    if form.validate_on_submit():

        transfer_choice = form.transfer_choice.data
        transfer_amount = form.transfer_amount.data
        session['transaction_amount'] = transfer_amount
        if transfer_choice == '1':
            transaction_type = 'ac to saving'
            account.saving_balance += transfer_amount
            account.account_balance -= transfer_amount
        elif transfer_choice == '2':
            transaction_type = 'saving to ac'
            account.saving_balance -= transfer_amount
            account.account_balance += transfer_amount
        elif transfer_choice == '3':
            transaction_type = 'paid loan'
            account.account_balance -= transfer_amount
            loan.loan_amount -= transfer_amount
        elif transfer_choice == '4':
            transaction_type = 'fd'
            account.account_balance -= transfer_amount
            fd.fd_amount += transfer_amount
        else:
            flash('something went wrong', 'danger')
            return redirect(url_for('users.dashboard'))
        session['transaction_type'] = transaction_type
        session['user_id'] = user.user_id
        session['receiver_id'] = user.user_id
        session['sender_id'] = user.user_id
        session['user_email'] = current_user.user_email

        send_otp_email(current_user)
        return redirect(url_for('users.otp_check'))

        # transfer = Transaction(
        #     user_id=user.user_id,
        #     transaction_amount=transfer_amount,
        #     sender_id=user.user_id,
        #     receiver_id=user.user_id,
        # )
        # db.session.add(transfer)
        # db.session.commit()
        #
        # add_transaction_type(
        #     transaction_id=transfer.transaction_id,
        #     transaction_type=transaction_type)
        #
        # flash('transaction done', 'success')
        # return redirect(url_for('users.dashboard'))

    elif request.method == 'GET':
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name

    else:
        flash("something went wrong", 'danger')
    return render_template('transfermoney.html', form=form)


@users.route("/otp-check", methods=['GET', 'POST'])
@login_required
def otp_check():
    form = OtpCheck()
    print("form checked")
    if form.validate_on_submit():
        print("")
        user_id = form.user_id.data
        transaction_amount = form.transaction_amount.data
        sender_id = form.sender_id.data
        receiver_id = form.receiver_id.data
        user_email = form.user_email.data
        transaction_type = session.get('transaction_type', None)
        otp_data = OtpByMail.query.filter_by(email=user_email).first()

        if form.otp.data == otp_data.otp:
            transfer = Transaction(
                user_id=user_id,
                transaction_amount=transaction_amount,
                sender_id=sender_id,
                receiver_id=receiver_id,
            )
            db.session.add(transfer)
            db.session.delete(otp_data)
            db.session.commit()

            add_transaction_type(
                transaction_id=transfer.transaction_id,
                transaction_type=transaction_type)

            flash('Transaction Successfully', 'success')
            return redirect(url_for('users.dashboard'))
        else:
            flash('Transaction Unsuccessfully as otp is wrong', 'danger')
            return redirect(url_for('users.dashboard'))

    elif request.method == 'GET':
        form.user_id.data = session.get('user_id', None)
        form.transaction_amount.data = session.get('transaction_amount', None)
        form.sender_id.data = session.get('sender_id', None)
        form.receiver_id.data = session.get('receiver_id', None)
        form.user_email.data = session.get('user_email', None)
        print(form.user_id.data)

    else:
        flash("something is wrong", 'danger')

    return render_template('otp_check.html', form=form)

    pass


count = 0


@users.route("/fd-money-transfer/", methods=['GET', 'POST'])
@login_required
def fd_interest_money():
    global count
    account = Account.query.filter_by(user_id=current_user.user_id).first()
    fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()
    now = datetime.datetime.now()
    old_date = fd.fd_create_date
    if old_date.date() < now.date():
        count += 1
        if count == 1:
            print("fd_amount= ", fd.fd_amount)
            print("fd_rate_interest=", fd.rate_interest)
            amount = (fd.fd_amount * fd.rate_interest) / 100
            account.account_balance += ((fd.fd_amount * fd.rate_interest) / 100)
            db.session.commit()
            flash(f"{amount} has been added", 'success')
        else:
            flash('already done cant do twice', 'danger')
    elif old_date.date() == now.date():
        print("yes same")
        if old_date.time() < now.date():
            count += 1
            if count == 1:
                print("fd_amount= ", fd.fd_amount)
                print("fd_rate_interest=", fd.rate_interest)
                amount = (fd.fd_amount * fd.rate_interest) / 100
                account.account_balance += ((fd.fd_amount * fd.rate_interest) / 100)
                db.session.commit()
                flash(f"{amount} has been added", 'success')
            else:
                flash('already done cant do twice', 'danger')
            print("yes the time")
        else:
            print("no way time")
    else:
        print("no way")

    print("DDSDS", fd.fd_create_date - now)
    return redirect(url_for('users.dashboard'))


@users.route("/bank-statement/", methods=['GET', 'POST'])
@login_required
def bank_statement():
    user = User.query.filter_by(user_name=current_user.user_name).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
    transactions = Transaction.query.filter_by(user_id=user.user_id).all()
    transaction_type = TransactionType.query.all()
    return render_template(
        'bank_statement.html',
        user=user,
        account=account,
        transactions=transactions,
        transaction_type=transaction_type
    )


@users.route("/bank-statement-pdf/", methods=['GET', 'POST'])
@login_required
def bank_statement_pdf():
    user = User.query.filter_by(user_name=current_user.user_name).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
    transactions = Transaction.query.filter_by(user_id=user.user_id).all()
    transaction_type = TransactionType.query.all()
    render = render_template(
        'bank_statement.html',
        user=user,
        account=account,
        transactions=transactions,
        transaction_type=transaction_type
    )

    WKHTMLTOPDF_CMD = subprocess.Popen(['which', './bin/wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
    print(f"CONFIG {WKHTMLTOPDF_CMD}")
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
    pdf = pdfkit.from_string(render, False, configuration=pdfkit_config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment;filename=bank_statement.pdf"
    return response

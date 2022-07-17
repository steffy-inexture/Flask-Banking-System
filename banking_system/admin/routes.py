from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from flask_login import login_user, login_required
from banking_system import db, bcrypt
from banking_system.admin.utils import authentication_req, add_loan_money_to_user, save_picture_about
from banking_system.models import Atm, User, Branch, BankDetails, Account, Loan, LoanType, Insurance, InsuranceType, \
    FixedDeposit, BankMember, MemberRole, LoanDetails, InsuranceDetails
from banking_system.admin.forms import AddBranch, LoginForm, AddAtm, UserAccountStatus, LoanApprovalStatus, \
    InsuranceApprovalForm, BankMemberData, UpdateFdStatus, AddMemberRole, LoanChoice, InsuranceChoice
from banking_system.admin.constants import ADMIN_LOGIN_SUCCESS, FLASH_MESSAGES, ADMIN_LOGIN_UNSUCCESS, USER_DELETED, \
    BRANCH_EXISTED, BRANCH_ADDED, ATM_EXISTED, ATM_ADDED, BANK_MEMBER_DELETED, BANK_MEMBER_ADDED, \
    STATUS_UPDATE, ROLE_ALREADY_EXIST, NEW_ROLE_ADDED, LOAN_CHOICE_ALREADY_EXIST, NEW_LOAN_CHOICE_ADDED, \
    INSURANCE_CHOICE_ALREADY_EXIST, NEW_INSURANCE_CHOICE_ADDED, NO_RECORD_ACTIVITY, NO_USER_FOUND, NOT_VALID_PICTURE, \
    BRANCH_DELETED, BRANCH_IS_ASSOCIATED, ATM_DELETED

admin = Blueprint('admin', __name__)


@admin.route("/admin_login/", methods=['GET', 'POST'])
def admin_login():
    """
        For admin login
        [ only admin can have the authority to login by using this ]
        form: LoginForm
        template: admin_login.html [ for LoginForm ]
                  admin_dashboard.html [ after login ]
        redirects to:
            after successfully login: admin_dashboard.html [ template ]
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email='steffy.inexture@gmail.com').first()
        if user is not None and form.user_password.data == user.user_password:
            login_user(user, remember=form.remember.data)
            flash(ADMIN_LOGIN_SUCCESS, FLASH_MESSAGES['SUCCESS'])
            users = User.query.order_by(User.user_id.desc())
            atms = Atm.query.order_by(Atm.atm_id.desc())
            branchs = Branch.query.order_by(Branch.branch_id.desc())
            return render_template('admin_dashboard.html', users=users, branchs=branchs, atms=atms)
        else:
            flash(ADMIN_LOGIN_UNSUCCESS, FLASH_MESSAGES['FAIL'])
    return render_template('admin_login.html', title='login', form=form)


@admin.route("/admin/admin_dashboard/", methods=['GET', 'POST'])
@login_required
@authentication_req
def admin_dashboard():
    """
        Admin dashboard shows the option functionalities which is performed by the bank admin only
        template/redirects to: admin_dashboard.html
        params:
            users = All user data
            branchs = All branches data of the bank
            atms = All atms data of the bank
            accounts = All accounts data of the bank
    """
    users = User.query.all()
    accounts = Account.query.all()
    atms = Atm.query.order_by(Atm.atm_id.desc())
    branchs = Branch.query.order_by(Branch.branch_id.desc())
    return render_template('admin_dashboard.html', users=users, branchs=branchs, atms=atms, accounts=accounts)


@admin.route("/all-user-data/", methods=['GET', 'POST'])
@login_required
@authentication_req
def admin_user_data():
    """
        Shows all the bank users with its status [ Active / Inactive ]
        template / redirects to: admin_user_data.html
        params:
            page = for pagination purpose
            per_page = number of rows shown in one-page
            users = all bank user data [ from 'User' table ]
            accounts =  user related account detail [ from 'Account' table ]
     """
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=3)
    accounts = Account.query.all()
    return render_template('admin_user_data.html', users=users, accounts=accounts)


@admin.route("/admin/delete-user/<user_id>/", methods=['GET', 'POST'])
@login_required
@authentication_req
def delete_user(user_id):
    """
        DELETE particular selected user and remove from the bank database
        template / redirects to: admin_user_data.html
    """
    User.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash(USER_DELETED, FLASH_MESSAGES['SUCCESS'])
    return redirect(url_for('admin.admin_user_data'))


@admin.route("/admin/all-branch-data/", methods=['GET', 'POST'])
@login_required
@authentication_req
def admin_branch_data():
    """
        show all bank branches data
        templates/redirects to: admin_branch_data.html
        params:
            page = for pagination purpose
            per_page = number of rows shown in one-page
            branchs = all bank branch data [ from 'Branch' table ]
    """
    page = request.args.get('page', 1, type=int)
    branchs = Branch.query.order_by(Branch.branch_id.desc()).paginate(page=page, per_page=5)
    return render_template('admin_branch_data.html', branchs=branchs)


@admin.route("/admin/delete-branch-data/<branch_id>", methods=['GET', 'POST'])
@login_required
@authentication_req
def delete_branch_data(branch_id):
    """
        for delete particular bank branch
        if bank branch is associated / interlinked with any bank user then it will not delete
        else bank branch delete successfully
    """
    accounts = Account.query.all()
    branch_used = 0
    for account in accounts:
        if int(account.branch_id) == int(branch_id):
            branch_used += 1
    if branch_used == 0:
        branch = Branch.query.filter_by(branch_id=branch_id).first()
        db.session.delete(branch)
        db.session.commit()
        flash(BRANCH_DELETED, FLASH_MESSAGES['FAIL'])
    else:
        flash(BRANCH_IS_ASSOCIATED, FLASH_MESSAGES['FAIL'])
    return redirect(url_for('admin.admin_branch_data'))


@admin.route("/admin/all-atm-data/", methods=['GET', 'POST'])
@login_required
@authentication_req
def admin_atm_data():
    """
        show all bank branches data
        templates/redirects to: admin_branch_data.html
        params:
            page = for pagination purpose
            per_page = number of rows shown in one-page
            branchs = all bank branch data [ from 'Branch' table ]
    """
    page = request.args.get('page', 1, type=int)
    atms = Atm.query.order_by(Atm.atm_id.desc()).paginate(page=page, per_page=5)
    return render_template('admin_atm_data.html', atms=atms)


@admin.route("/admin/delete-atm-data/<atm_id>", methods=['GET', 'POST'])
@login_required
@authentication_req
def delete_atm_data(atm_id):
    """
        for delete particular bank atm
        if bank atm has the atm id then delete successfully
        params: particular atm's atm id
    """
    atm = Atm.query.filter_by(atm_id=atm_id).first()
    if atm:
        db.session.delete(atm)
        db.session.commit()
        flash(ATM_DELETED, FLASH_MESSAGES['SUCCESS'])
        return redirect(url_for('admin.admin_atm_data'))


@admin.route("/admin/all-loan-data/", methods=['GET', 'POST'])
@login_required
@authentication_req
def admin_user_loan_data():
    """
        shows the loan's data which is requested by the user
        included status [ Active / Inactive ]
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.paginate(page=page, per_page=5)
    loans = Loan.query.all()
    loantype = LoanType.query.all()
    return render_template('admin_user_loan_data.html', loans=loans, loantype=loantype, user=user)


@admin.route("/admin/loan-approval-status/<user_id>/", methods=['GET', 'POST'])
@login_required
@authentication_req
def loan_approval(user_id):
    """
        admin can change the loan status data
        initially it will be Inactive [ by default ]
        two options for approval : [ 1.Active & 2.Inactive ]
    """
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        loan = Loan.query.filter_by(user_id=user_id).first()
        if loan:
            loan_type = LoanType.query.filter_by(loan_id=loan.loan_id).first()
            form = LoanApprovalStatus()
            if form.validate_on_submit():
                approval_status = form.approval_status.data
                if approval_status == '1':
                    loan.loan_status = 'Active'
                    add_loan_money_to_user(user_id, loan.loan_amount, loan.loan_type)
                else:
                    loan.loan_status = 'Inactive'
                db.session.commit()
                flash(STATUS_UPDATE.format(user_name=user.user_name, activity='loan'), FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_user_loan_data'))
            elif request.method == 'GET':
                form.user_id.data = user_id
                form.user_name.data = user.user_name
                form.loan_id.data = loan.loan_id
                form.loan_amount.data = loan.loan_amount
                form.rate_interest.data = loan.rate_interest
                form.paid_amount.data = loan.paid_amount
                form.loan_type.data = loan_type.loan_type
                form.loan_status.data = loan.loan_status
        else:
            flash(NO_RECORD_ACTIVITY.format(activity='Loan'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
    else:
        flash(NO_USER_FOUND.format(id=user_id), FLASH_MESSAGES['FAIL'])
        return redirect(url_for('admin.admin_dashboard'))

    return render_template(
        'loan_request_approval.html',
        user_id=user_id,
        user_name=user.user_name,
        loan_id=loan.loan_id,
        loan_amount=loan.loan_amount,
        rate_interest=loan.rate_interest,
        paid_amount=loan.paid_amount,
        loan_type=loan_type.loan_type,
        loan_status=loan.loan_status,
        title='account-status', form=form
    )


@admin.route("/admin/all-insurance-data/", methods=['GET', 'POST'])
@login_required
@authentication_req
def admin_user_insurance_data():
    """
        shows all requests for insurance application
        admin has the authority to change the status of insurance
    """
    users = User.query.all()
    insurances = Insurance.query.all()
    insurance_types = InsuranceType.query.all()
    return render_template('admin_user_insurance_data.html', insurances=insurances, insurancetypes=insurance_types,
                           users=users)


@admin.route("/admin/insurance-approval-status/<user_id>/", methods=['GET', 'POST'])
@login_required
@authentication_req
def insurance_approval(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        insurance = Insurance.query.filter_by(user_id=user.user_id).first()
        if insurance:
            insurance_type = InsuranceType.query.filter_by(insurance_id=insurance.insurance_id).first()
            form = InsuranceApprovalForm()
            if form.validate_on_submit():
                approval_status = form.approval_status.data
                insurance = Insurance.query.filter_by(user_id=user_id).first()
                if approval_status == '1':
                    insurance.insurance_status = 'Active'
                else:
                    insurance.insurance_status = 'Inactive'
                db.session.commit()
                flash(STATUS_UPDATE.format(user_name=user.user_name, activity='insurance'), FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_user_insurance_data'))
            elif request.method == 'GET':
                form.user_id.data = user_id
                form.user_name.data = user.user_name
                form.insurance_id.data = insurance.insurance_id
                form.insurance_amount.data = insurance.insurance_amount
                form.insurance_type.data = insurance.insurance_type
                form.insurance_status.data = insurance.insurance_status
        else:
            flash(NO_RECORD_ACTIVITY.format(activity='Insurance'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
    else:
        flash(NO_USER_FOUND.format(id=user_id), FLASH_MESSAGES['FAIL'])
        return redirect(url_for('admin.admin_dashboard'))

    return render_template(
        'insurance_request_approval.html',
        user_id=user_id,
        user_name=user.user_name,
        insurance_id=insurance.insurance_id,
        insurance_amount=insurance.insurance_amount,
        insurance_type=insurance_type.insurance_type,
        insurance_status=insurance.insurance_status,
        title='account-status', form=form
    )


@admin.route("/admin/all-fd-data/", methods=['GET', 'POST'])
@login_required
@authentication_req
def admin_user_fd_data():
    """
        shows all fixed deposits data
        with its status
        admin has the authority to change the status of insurance [Active/Inactive]
    """
    users = User.query.all()
    account = Account.query.all()
    fds = FixedDeposit.query.all()

    return render_template('admin_user_fd_data.html', fds=fds,
                           users=users, account=account)


@admin.route("/admin/update-fd-status/<user_id>/", methods=['GET', 'POST'])
@login_required
@authentication_req
def update_fd_status(user_id):
    """
        Admin has the authority to change the status of the fd
        mainly two options are given
        1.Active & 2.Inactive
    """
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        account = Account.query.filter_by(user_id=user.user_id).first()
        if account:
            fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()
            if fd:
                form = UpdateFdStatus()
                if form.validate_on_submit():
                    status = form.fd_status.data
                    fd.fd_status = status
                    db.session.commit()
                    flash(STATUS_UPDATE.format(user_name=user.user_name, activity='Fd'), FLASH_MESSAGES['SUCCESS'])
                    return redirect(url_for('admin.admin_user_fd_data'))
                elif request.method == 'GET':
                    form.user_id.data = user.user_id
                    form.user_name.data = user.user_name
                    form.fd_id.data = fd.fd_id
                    form.fd_amount.data = fd.fd_amount
            else:
                flash(NO_RECORD_ACTIVITY.format(activity='Fixed deposit'), FLASH_MESSAGES['FAIL'])
                return redirect(url_for('admin.admin_dashboard'))
        else:
            flash(NO_RECORD_ACTIVITY.format(activity='Account'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
    else:
        flash(NO_USER_FOUND.format(id=user_id), FLASH_MESSAGES['FAIL'])
        return redirect(url_for('admin.admin_dashboard'))

    return render_template(
        'update_fd_status.html',
        title='fd-status', form=form
    )


@admin.route("/admin/delete-fd/<user_id>/", methods=['GET', 'POST'])
@login_required
@authentication_req
def delete_fd(user_id):
    """
        Admin has the authority to delete the fixed deposits
    """
    user = User.query.filter_by(user_id=user_id).first()
    flash(f"{user.user_name} this is the name", 'success')
    return redirect(url_for('admin.admin_user_fd_data'))


@admin.route("/admin/change-account-status/<user_id>/", methods=['GET', 'POST'])
@login_required
@authentication_req
def account_status(user_id):
    """
        admin has the authority to change the user's account status
        has two main options
        1.Active & 2.Inactive
    """
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        account = Account.query.filter_by(user_id=user.user_id).first()
        if account:
            form = UserAccountStatus()
            if form.validate_on_submit():
                account_status = form.account_status.data
                account = Account.query.filter_by(user_id=user_id).first()
                if account_status == '1':
                    account.account_status = 'Inactive'
                else:
                    account.account_status = 'Active'
                db.session.commit()
                flash(STATUS_UPDATE.format(user_name=user.user_name, activity='Account'), FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_dashboard'))
            elif request.method == 'GET':
                form.user_id.data = user_id
                form.user_name.data = user.user_name
                form.account_number.data = account.account_number
        else:
            flash(NO_RECORD_ACTIVITY.format(activity='Account'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
    else:
        flash(NO_USER_FOUND.format(id=user_id), FLASH_MESSAGES['FAIL'])
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('user_account_status.html',
                           user_id=int(user_id),
                           user_name=user.user_name,
                           account_number=account.account_number,
                           title='account-status', form=form)


@admin.route("/admin/add_branch/", methods=['GET', 'POST'])
@login_required
@authentication_req
def add_branch():
    """
        Admin has right to add new branch for the bank
        redirects to: admin.admin_dashboard --> after success
                      admin.add_branch --> if already branch exists
    """
    form = AddBranch()
    if form.validate_on_submit():
        table_branch = Branch.query.filter_by(branch_name=form.branch_name.data).first()
        if table_branch:
            flash(BRANCH_EXISTED, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.add_branch'))
        else:
            bank = BankDetails.query.all()
            branch = Branch(
                branch_name=form.branch_name.data,
                branch_address=form.branch_address.data,
                bank_id=bank[0].bank_id
            )
            db.session.add(branch)
            try:
                db.session.commit()
                flash(BRANCH_ADDED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_dashboard'))
            except Exception as e:
                flash(f'{e}', FLASH_MESSAGES['FAIL'])
    return render_template('add_branch.html', title='add-branch', form=form)


@admin.route("/admin/add_atm/", methods=['GET', 'POST'])
@login_required
@authentication_req
def add_atm():
    """
        Admin has right to add new atm for the bank
        redirects to: admin.admin_dashboard --> after success
                      admin.add_branch --> if already atm exists
    """
    form = AddAtm()
    if form.validate_on_submit():
        table_atm = Atm.query.filter_by(atm_address=form.atm_address.data).first()
        if table_atm:
            flash(ATM_EXISTED, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.add_atm'))
        else:
            bank = BankDetails.query.all()
            atm = Atm(
                atm_address=form.atm_address.data,
                bank_id=bank[0].bank_id
            )
            db.session.add(atm)
            try:
                db.session.commit()
                flash(ATM_ADDED, FLASH_MESSAGES['SUCCESS'])
                return redirect(url_for('admin.admin_dashboard'))
            except Exception as e:
                flash(f'{e}', FLASH_MESSAGES['FAIL'])
    return render_template('add_atm.html', title='add-atm', form=form)


@admin.route("/admin/bank-show-all-member/", methods=['GET', 'POST'])
@login_required
@authentication_req
def show_bank_member():
    """
        shows all bank member
        redirects to/ template: show_bank_member.html
    """
    member = BankMember.query.all()
    return render_template('show_bank_member.html', member=member)


@admin.route("/admin/bank-about-member/", methods=['GET', 'POST'])
@login_required
@authentication_req
def bank_about_member():
    """
        Admin has right to add bank member for the bank
        redirects to: admin.admin_dashboard --> after success
    """
    form = BankMemberData()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture_about(form.image_file.data)
            data = BankMember(
                image_file=picture_file,
                bank_member_name=form.bank_member_name.data,
                bank_member_position=form.bank_member_position.data,
                bank_member_about=form.bank_member_about.data,
                bank_member_email_id=form.bank_member_email_id.data,
                bank_member_contact=form.bank_member_contact.data
            )
            db.session.add(data)
            db.session.commit()
            flash(BANK_MEMBER_ADDED, FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash(NOT_VALID_PICTURE, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
    elif request.method == 'GET':
        form.bank_member_position.choices = [i.member_role for i in MemberRole.query.all()]

    return render_template('add_bank_member.html', title='New bank member',
                           form=form, legend='New bank member')


@admin.route("/admin/delete-bank-member/<member_id>/", methods=['GET', 'POST'])
@login_required
@authentication_req
def delete_bank_member(member_id):
    """
        Admin has right to delete the bank member
        redirects to: admin.admin_dashboard --> after success
    """
    BankMember.query.filter_by(bank_member_id=member_id).delete()
    db.session.commit()
    flash(BANK_MEMBER_DELETED, FLASH_MESSAGES['SUCCESS'])
    return redirect(url_for('admin.admin_dashboard'))


@admin.route("/admin/show_member_role_list", methods=['GET', 'POST'])
@login_required
@authentication_req
def show_member_role_list():
    """
        shows all member role of the bank for bank member [ about page ]
        redirects to/template: show_all_member_role.html
    """

    page = request.args.get('page', 1, type=int)
    roles = MemberRole.query.paginate(page=page, per_page=3)
    return render_template('show_all_member_role.html', roles=roles)


@admin.route("/admin/show_loan_choices/", methods=['GET', 'POST'])
@login_required
@authentication_req
def show_loan_choices():
    """
        shows all bank choice for loan available in bank
        redirects to/template: show_all_provided_loans.html
    """
    page = request.args.get('page', 1, type=int)
    loans = LoanDetails.query.paginate(page=page, per_page=3)
    return render_template('show_all_provided_loans.html', loans=loans)


@admin.route("/admin/show_insurance_choices/", methods=['GET', 'POST'])
@login_required
@authentication_req
def show_insurance_choices():
    """
        shows all bank choice for insurances available in bank
        redirects to/template: show_all_provided_insurances.html
    """
    page = request.args.get('page', 1, type=int)
    insurances = InsuranceDetails.query.paginate(page=page, per_page=3)
    return render_template('show_all_provided_insurances.html', insurances=insurances)


@admin.route("/admin/add-bank-role/", methods=['GET', 'POST'])
@login_required
@authentication_req
def member_role_list():
    """
        Admin can have right to add new member role [ no duplication ]
        redirects to: admin.admin_dashboard
    """
    form = AddMemberRole()
    if form.validate_on_submit():
        role_name = form.role_name.data
        role = MemberRole.query.filter_by(member_role=role_name).first()
        if role:
            flash(ROLE_ALREADY_EXIST, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
        else:
            add_role = MemberRole(member_role=role_name)
            db.session.add(add_role)
            db.session.commit()
            flash(NEW_ROLE_ADDED, FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_member_role_list.html', title='add-member-role-list', form=form)


@admin.route("/admin/add-loan-options/", methods=['GET', 'POST'])
@login_required
@authentication_req
def loan_choices():
    """
        Admin can have right to add new loan choice for user [ no duplication ]
        redirects to: admin.admin_dashboard
    """
    form = LoanChoice()
    if form.validate_on_submit():
        loan_choice = form.loan_choice.data
        loan = LoanDetails.query.filter_by(loan_name=loan_choice).first()
        if loan:
            flash(LOAN_CHOICE_ALREADY_EXIST, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
        else:
            add_loan = LoanDetails(loan_name=loan_choice)
            db.session.add(add_loan)
            db.session.commit()
            flash(NEW_LOAN_CHOICE_ADDED, FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_loan_choice_list.html', title='add-loan-choice-list', form=form)


@admin.route("/admin/add-insurance-options/", methods=['GET', 'POST'])
@login_required
@authentication_req
def insurance_choices():
    """
        Admin can have right to add new insurance choice [ no duplication ]
        redirects to: admin.admin_dashboard
    """
    form = InsuranceChoice()
    if form.validate_on_submit():
        insurance_choice = form.insurance_choice.data
        insurance = InsuranceDetails.query.filter_by(insurance_name=insurance_choice).first()
        if insurance:
            flash(INSURANCE_CHOICE_ALREADY_EXIST, FLASH_MESSAGES['FAIL'])
            return redirect(url_for('admin.admin_dashboard'))
        else:
            add_insurance = InsuranceDetails(insurance_name=insurance_choice)
            db.session.add(add_insurance)
            db.session.commit()
            flash(NEW_INSURANCE_CHOICE_ADDED, FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_insurance_choice_list.html', title='add-loan-choice-list', form=form)


@admin.route("/delete", methods=["POST", "GET"])
@login_required
@authentication_req
def delete():
    """
        delete all checked member roles from the bank member role table
    """
    for getid in request.form.getlist('checkdelete'):
        MemberRole.query.filter_by(id=getid).delete()
        db.session.commit()
    return jsonify('Records deleted successfully')

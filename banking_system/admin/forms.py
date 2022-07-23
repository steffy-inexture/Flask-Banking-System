from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, \
    TextAreaField, FileField, EmailField, SelectField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """
        login form to take the user login data
    """
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login IN')


class UserAccountStatus(FlaskForm):
    """
        Admin can change the user's bank account status
        1. Active or 2. Inactive
    """
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User_name', validators=[DataRequired()], render_kw={'readonly': True})
    account_number = StringField('Account_number', validators=[DataRequired()], render_kw={'readonly': True})
    account_status = RadioField('Account status', choices=[('1', 'Inactive'), ('2', 'Active')])
    submit = SubmitField('Submit the changes')


class LoanApprovalStatus(FlaskForm):
    """
        Admin can give approval to the user's bank Loan
        1. Approve [ active ] or 2. Decline [ Inactive ]
    """
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User name', validators=[DataRequired()], render_kw={'readonly': True})
    loan_id = StringField('Loan id', validators=[DataRequired()], render_kw={'readonly': True})
    loan_amount = StringField('Loan amount', validators=[DataRequired()], render_kw={'readonly': True})
    rate_interest = StringField('Rate interest', validators=[DataRequired()], render_kw={'readonly': True})
    paid_amount = StringField('Paid amount', validators=[DataRequired()], render_kw={'readonly': True})
    loan_type = StringField('Loan type', validators=[DataRequired()], render_kw={'readonly': True})
    loan_status = StringField('Loan status', validators=[DataRequired()], render_kw={'readonly': True})
    approval_status = RadioField('Approval status', choices=[('1', 'Approve'), ('2', 'Decline')])
    submit = SubmitField('Submit the changes')


class InsuranceApprovalForm(FlaskForm):
    """
        Admin can give approval to the user's Insurance
        1. Approve [ active ] or 2. Decline [ Inactive ]
    """
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User name', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_id = StringField('Insurance id', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_amount = StringField('Insurance amount', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_type = StringField('Insurance type', validators=[DataRequired()], render_kw={'readonly': True})
    insurance_status = StringField('Insurance status', validators=[DataRequired()], render_kw={'readonly': True})
    approval_status = RadioField('Approval status', choices=[('1', 'Approve'), ('2', 'Decline')])
    submit = SubmitField('Submit the changes')


class UpdateFdStatus(FlaskForm):
    """
        Admin can give update to the user's fd status
        1. Active or 2. Inactive
    """
    user_id = StringField('User_id', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User name', validators=[DataRequired()], render_kw={'readonly': True})
    fd_id = StringField('Fd id', validators=[DataRequired()], render_kw={'readonly': True})
    fd_amount = StringField('Fd amount', validators=[DataRequired()], render_kw={'readonly': True})
    fd_status = RadioField('Fd status', choices=[('Inactive', 'Inactive'), ('Active', 'Active')])
    submit = SubmitField('Update the Fd detail')


class AddBranch(FlaskForm):
    """
        Admin can add new bank branch
        with no duplication
    """
    branch_name = StringField('branch name: ', validators=[DataRequired()])
    branch_address = StringField('Branch addresses: ', validators=[DataRequired()])
    submit = SubmitField('Add this branch')


class AddAtm(FlaskForm):
    """
        Admin can add new bank atm
        with no duplication
    """
    atm_address = StringField('Atm address: ', validators=[DataRequired()])
    submit = SubmitField('Add this atm')


class BankMemberData(FlaskForm):
    """
            Admin can add new bank member
    """
    image_file = FileField('add photo: ', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    bank_member_name = StringField('Member name: ', validators=[DataRequired()])
    bank_member_position = SelectField('Member Position', choices=[], validators=[DataRequired()],
                                       validate_choice=False)
    bank_member_about = TextAreaField('about member', validators=[DataRequired()])
    bank_member_email_id = EmailField('Email id', validators=[DataRequired()])
    bank_member_contact = IntegerField('Contact number', validators=[DataRequired()])

    submit = SubmitField('Update the members')


class AddMemberRole(FlaskForm):
    """
        Admin can add new bank member role which is assign to bank member afterwords
        with no duplication
    """
    role_name = StringField('Role : ', validators=[DataRequired()])
    submit = SubmitField('Add this to role list')


class LoanChoice(FlaskForm):
    """
        Admin can add new bank Loan choices which is further used by user to apply loans
        with no duplication
    """
    loan_choice = StringField('Loan name : ', validators=[DataRequired()])
    submit = SubmitField('Add this to Loan choice list')


class InsuranceChoice(FlaskForm):
    """
        Admin can add new bank Insurance choices which is further used by user to apply Insurance
        with no duplication
    """
    insurance_choice = StringField('insurance name : ', validators=[DataRequired()])
    submit = SubmitField('Add this to insurance choice list')

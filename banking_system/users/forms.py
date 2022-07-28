from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, RadioField, \
    SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from banking_system.models import Account, User, Loan, FixedDeposit
from banking_system.users.utils import CustomValidation


class RegistrationForm(FlaskForm, CustomValidation):
    """
            Registrationform to take user information
            validations:
                validate_user_name - validate the username must be >2 length
                validate_user_email - validate the user_email must b valid and existed id with no duplication
                validate_user_phone_number - must be length of 10
                validate_confirm_password - must be same as user_password
    """
    user_name = StringField('Username: ', validators=[DataRequired(), Length(min=2, max=20)])
    user_email = StringField('Email: ', validators=[DataRequired(), Email()])
    user_phone_number = IntegerField('Phone number: ', validators=[DataRequired()])
    user_first_name = StringField('First name: ', validators=[DataRequired()])
    user_last_name = StringField('Last name: ', validators=[DataRequired()])
    user_address = StringField('Address: ', validators=[DataRequired()])
    user_age = IntegerField('Age: ', validators=[DataRequired()])
    date_of_birth = DateField('Date of birth', format='%Y-%m-%d')
    user_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('user_password')])
    submit = SubmitField('Sign Up')

    def validate_user_name(self, user_name):
        super().validate_user_name(user_name)

    def validate_user_email(self, user_email):
        super().validate_user_email(user_email)

    def validate_user_phone_number(self, user_phone_number):
        if len(str(user_phone_number.data)) != 10:
            raise ValidationError('The length must be 10 for the phone number')

    def validate_confirm_password(self, confirm_password):
        user_password = self.user_password.data
        if confirm_password.data != user_password:
            raise ValidationError('Confirm passwd must be equal to paasword')


class LoginForm(FlaskForm):
    """
        Loginform to take user credential to log in to the website
        with valid user data only
    """
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
        UpdateAccountForm form
        Update the user account information
    """
    user_name = StringField('Username: ', validators=[DataRequired(), Length(min=2, max=20)])
    user_email = StringField('Email: ', validators=[DataRequired(), Email()], render_kw={'readonly': True})
    user_phone_number = IntegerField('Phone number: ', validators=[DataRequired()])
    user_first_name = StringField('First name: ', validators=[DataRequired()])
    user_last_name = StringField('Last name: ', validators=[DataRequired()])
    user_address = StringField('Address: ', validators=[DataRequired()])
    user_age = IntegerField('Age: ', validators=[DataRequired()])
    date_of_birth = DateField('Date of birth', format='%Y-%m-%d')
    submit = SubmitField('Update the profile data')

    def validate_user_name(self, user_name):
        if user_name.data != current_user.user_name:
            user = User.query.filter_by(user_name=user_name.data).first()
            if user:
                raise ValidationError('That username is taken please Choose different one')

    def validate_user_phone_number(self, user_phone_number):
        if len(str(user_phone_number.data)) != 10:
            raise ValidationError('Phone number must be 10 digits')


# request for reset the password
class RequestResetForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_user_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. YOu must register first! ')


class ResetPasswordForm(FlaskForm):
    """
        ResetPasswordForm form
        To reset the user password information
    """
    user_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ApplyLoanForm(FlaskForm):
    """
        Apply for loan using this form
        with valid choices opted by user
    """
    user_id = StringField('Your id: ', render_kw={'readonly': True})
    user_name = StringField('Your name: ', render_kw={'readonly': True})
    loan_amount_choices = RadioField('Available Loans',
                                     choices=[
                                         ('1', '1000'),
                                         ('2', '5000'),
                                         ('3', '10000'),
                                         ('4', '15000')
                                     ]
                                     )
    loan_rate_interests = RadioField('Rate Interest', choices=[('1', '6.5%'), ('2', '6.7%')])
    loan_type = SelectField('Loan type', choices=[], validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Apply for loan')


class ApplyInsuranceForm(FlaskForm):
    """
        Apply for Insurance using this form
        with valid choices opted by user
    """
    user_id = StringField('Your id: ', render_kw={'readonly': True})
    user_name = StringField('Your name: ', render_kw={'readonly': True})
    insurance_amount_choices = RadioField('Available Insurance amount',
                                          choices=[
                                              ('1', '1000'),
                                              ('2', '5000'),
                                              ('3', '10000'),
                                              ('4', '15000')
                                          ]
                                          )
    insurance_type = SelectField('Insurance type', choices=[], validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Apply for Insurance')


class AddMoney(FlaskForm):
    """
           AddMoney to other bank user account
    """
    reciver_account = IntegerField('Enter receiver account number: ', validators=[DataRequired()])
    credit_amount = IntegerField('Amount you wanna add: ', validators=[DataRequired()])
    user_password = PasswordField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Credit the balance', )

    def validate_reciver_account(self, reciver_account):
        account = Account.query.filter_by(account_number=reciver_account.data).first()
        if account is None:
            raise ValidationError('No account is exist in this number')


class TransferMoney(FlaskForm):
    """
        TransferMoney Form
        to transfer money with given options
        here '1': 'Account to saving'
             '2': 'Saving to account'
             '3': 'Account to pay loan'
             '4: 'Account to Fd'
    """
    user_id = IntegerField('user idL ', render_kw={'readonly': True})
    user_name = StringField('User name: ', render_kw={'readonly': True})
    transfer_choice = RadioField('Transaction choice',
                                 choices=[('1', 'Account to saving'),
                                          ('2', 'Saving to account'),
                                          ('3', 'Account to pay loan'),
                                          ('4', 'Account to Fd')])
    transfer_amount = IntegerField('TRANSFER AMOUNT', validators=[DataRequired()])
    user_password = PasswordField('Enter the password', validators=[DataRequired()])
    otp_btn = BooleanField('send otp', default=False)
    enter_otp = StringField('enter your otp:')
    submit = SubmitField('Proceed the transfer')

    def validate_transfer_amount(self, transfer_amount):
        transfer_choice = self.transfer_choice
        user = User.query.filter_by(user_id=current_user.user_id).first()
        account = Account.query.filter_by(user_id=user.user_id).first()
        loan = Loan.query.filter_by(user_id=user.user_id).first()
        fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()

        if transfer_choice.data == '1':
            if transfer_amount.data > account.account_balance:
                raise ValidationError('Insufficient balance')

        elif transfer_choice.data == '4':
            if fd:
                if fd.fd_status == 'Active':
                    if transfer_amount.data > account.account_balance:
                        raise ValidationError('Insufficient balance')
                else:
                    raise ValidationError('Fd status needs to activate first')
            else:
                raise ValidationError('you have not requested for fd yet')

        elif transfer_choice.data == '2':
            if transfer_amount.data > account.saving_balance:
                raise ValidationError('Insufficient saving balance')

        elif transfer_choice.data == '3':
            if loan:
                if loan.loan_status == 'Active':
                    if transfer_amount.data > account.account_balance:
                        raise ValidationError('Insufficient balance')
                    elif account.account_balance > transfer_amount.data > loan.loan_amount:
                        raise ValidationError('Your loan amount is less')
                else:
                    raise ValidationError('Admin needs to active your loan first')
            else:
                raise ValidationError('You have no loans pending to pay')

    def validate_user_password(self, user_password):
        if user_password.data != current_user.user_password:
            raise ValidationError('Password incorrect')


class ChangeBranch(FlaskForm):
    """
        User can change the bank branch by selecting myField option here
    """
    user_id = IntegerField('User id:  ', validators=[DataRequired()], render_kw={'readonly': True})
    user_name = StringField('User name ', validators=[DataRequired()], render_kw={'readonly': True})
    account_number = StringField('Account number', validators=[DataRequired()], render_kw={'readonly': True})
    myField = SelectField('Available branches', choices=[], validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Change the bank branch')


class OtpCheck(FlaskForm):
    """
        User can cross-check the Otp from mail and typing in this from
        if correct then and only money can transfer
    """
    user_id = IntegerField('User id:  ', render_kw={'readonly': True})
    transaction_amount = IntegerField('Transaction amount:  ',
                                      render_kw={'readonly': True})
    sender_id = IntegerField('Sender id:  ', render_kw={'readonly': True})
    receiver_id = IntegerField('Receiver id:  ', render_kw={'readonly': True})
    user_email = user_name = StringField('User Email ', render_kw={'readonly': True})
    otp = IntegerField('Otp:  ')
    submit = SubmitField('Proceed for transaction')


class ChangePassword(FlaskForm):
    """
        Us can change password
        if old password is correct then and only new password will be chnages
    """
    old_pwd = PasswordField('Old password: ', validators=[DataRequired()])
    new_pwd = PasswordField('New password: ', validators=[DataRequired()])
    confirm_new_pwd = PasswordField('Confirm new password: ', validators=[DataRequired()])
    submit = SubmitField('Proceed ')



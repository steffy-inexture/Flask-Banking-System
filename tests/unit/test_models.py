def test_new_user(new_user):
    assert new_user.user_name == 'testuser'
    assert new_user.user_password == 'testuser@123'
    assert new_user.user_email == 'testuser@gmail.com'
    assert new_user.u_p == 1234567888
    assert new_user.user_first_name == 'test'
    assert new_user.user_last_name == 'user'
    assert new_user.user_address == 'NYC'
    assert new_user.user_age == 21


def test_new_user_type(new_user_type):
    assert new_user_type.user_id == 1
    assert new_user_type.user_role == 'user'


def test_new_account(new_account):
    assert new_account.user_id == 1
    assert new_account.account_number == 1
    assert new_account.branch_id == '1'


def test_new_account_type(new_account_type):
    assert new_account_type.account_type_id == 1
    assert new_account_type.account_number == 1
    assert new_account_type.account_type == 'Active'


def test_new_card(new_card):
    assert new_card.card_number == 1000
    assert new_card.cvv_number == 1000
    assert new_card.card_pin == 1234
    assert new_card.account_number == 1


def test_new_transaction(new_transaction):
    assert new_transaction.transaction_id == 1
    assert new_transaction.transaction_amount == 1000
    assert new_transaction.sender_id == 1
    assert new_transaction.receiver_id == 1
    assert new_transaction.user_id == 1


def test_new_transaction_type(new_transaction_type):
    assert new_transaction_type.transaction_type_id == 1
    assert new_transaction_type.transaction_id == 1
    assert new_transaction_type.transaction_type == 'Credit'


def test_new_loan(new_loan):
    assert new_loan.loan_id == 1
    assert new_loan.loan_amount == 100
    assert new_loan.loan_status == 'Active'
    assert new_loan.rate_interest == 5.6
    assert new_loan.paid_amount == 5
    assert new_loan.user_id == 1


def test_new_loan_type(new_loan_type):
    assert new_loan_type.loan_type_id == 1
    assert new_loan_type.loan_id == 1
    assert new_loan_type.loan_type == 'Car loan'


def test_new_insurance(new_insurance):
    assert new_insurance.insurance_id == 1
    assert new_insurance.insurance_amount == 10000
    assert new_insurance.insurance_status == 'Active'
    assert new_insurance.user_id == 1


def test_new_insurance_type(new_insurance_type):
    assert new_insurance_type.insurance_type_id == 1
    assert new_insurance_type.insurance_id == 1
    assert new_insurance_type.insurance_type == 'Life insurance'


def test_new_fixed_deposit(new_fixed_deposit):
    assert new_fixed_deposit.fd_id == 1
    assert new_fixed_deposit.fd_amount == 10000
    assert new_fixed_deposit.fd_status == 'Active'
    assert new_fixed_deposit.rate_interest == 5.6
    assert new_fixed_deposit.added_amount == 5000
    assert new_fixed_deposit.account_number == 1


def test_new_bank_details(new_bank_details):
    assert new_bank_details.bank_name == 'demobank'
    assert new_bank_details.bank_id == 5
    assert new_bank_details.bank_email == 'demo122@gmail.com'
    assert new_bank_details.bank_contact == 12345


def test_new_branch(new_branch):
    assert new_branch.branch_id == 1
    assert new_branch.branch_name == 'sjk'
    assert new_branch.branch_address == 'ahmedabad'
    assert new_branch.bank_id == 1


def test_new_atm(new_atm):
    assert new_atm.atm_id == 1
    assert new_atm.atm_address == 'ahmedabad'
    assert new_atm.bank_id == 1


def test_new_member(new_bank_member):
    assert new_bank_member.image_file == "testprofile.jpg"
    assert new_bank_member.bank_member_id == 1
    assert new_bank_member.bank_member_name == 'steffy'
    assert new_bank_member.bank_member_position == 'user'
    assert new_bank_member.bank_member_about == 'hey this is steffy,nice to meet ya'
    assert new_bank_member.bank_member_email_id == 'user@gmail.com'
    assert new_bank_member.bank_member_contact == 1234567895


def test_new_member_role(new_member_role):
    assert new_member_role.id == 5
    assert new_member_role.member_role == 'bank user'


def test_new_loan_detail(new_loan_detail):
    assert new_loan_detail.id == 1
    assert new_loan_detail.loan_name == 'home loan'


def test_new_insurance_detail(new_insurance_detail):
    assert new_insurance_detail.id == 1
    assert new_insurance_detail.insurance_name == 'home loan'


def test_otp_by_mail(otp_by_mail):
    assert otp_by_mail.id == 1
    assert otp_by_mail.email == 'home@gmail.com'
    assert otp_by_mail.otp == 1234

from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Account

class Management:
    class User:
        @staticmethod
        def login(request, user):
            session = request.session
            session['name'] = user.name
            session['role'] = user.role
            session['LoggedIn'] = True
        @staticmethod    
        def authenticate_user(username, password):
            try:
                user = Account.objects.get(username=username)
                if user.password == password:
                    return user
            except Account.DoesNotExist:
                return None
        @staticmethod
        def logout(request):
            request.session.clear()
    class Account:
        @staticmethod
        def create_account(request):
            form_name = request.POST['name']
            form_phone = request.POST['phone']
            form_email = request.POST['email']
            form_address = request.POST['address']
            form_password = request.POST['password']
            acctype = request.POST['acctype']
            new_account = Account(
                username=form_name,
                password=form_password,
                role=(1 if acctype == "instructor" else 2),
                name=form_name,
                phone=form_phone,
                email=form_email,
                address=form_address
            )
            new_account.save()

        @staticmethod
        def update_account(request, selected_account):
            # Case 1: emptyLogin
            if not request.POST or request.POST['username'] == '' or request.POST['password'] == '':
                return 'Login fields cannot be empty'
            # Case 2: usernameTaken
            user_id = selected_account.account_id
            if Account.objects.filter(username=request.POST['username']).exclude(account_id=user_id).exists():
                return 'An account with that username already exists.'
            # Case 3: invalid fields
            try:
                # Update user information with form data
                selected_account.username = request.POST['username']
                selected_account.password = request.POST['password']
                selected_account.role = request.POST['role']
                selected_account.name = request.POST['name']
                selected_account.phone = request.POST['phone']
                selected_account.email = request.POST['email']
                selected_account.address = request.POST['address']
                selected_account.office_hour_location = request.POST['office_hour_location']
                selected_account.office_hour_time = request.POST['office_hour_time']

                # Save the changes
                selected_account.full_clean()
                selected_account.save()
            except ValidationError as e:
                return str(e)

        @staticmethod
        def delete_account(selected_account):
            # Implement the logic to delete the account based on the provided user_id
            pass
    class Profile: 
        @staticmethod
        def edit_profile_data(request, user, field_name, field_type, error_name):
            if request.POST.get(field_name) != "":
                new_data = request.POST.get(field_name)
                if not isinstance(new_data, field_type):
                    raise TypeError(f"{error_name} not {field_type.__name__} fails to raise TypeError")

                if new_data == "Null":
                    raise ValueError("Null value fails raise ValueError")

                setattr(user, field_name.lower(), new_data)
                user.save()

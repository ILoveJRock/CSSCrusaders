from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import *

# call this as loginCheck(request, x) with x being the int value of the role needed to access
def loginCheck(request, role):
  session = request.session
  logged_in = session.get('LoggedIn', False)# `session.get('LoggedIn', False)` is retrieving the value of the 'LoggedIn' key from
  # the session dictionary. If the key does not exist, it will return the default value of
  # False.
  session.get('LoggedIn', False)
  user_role = session.get('role', 3)
  if logged_in:
    if user_role > role:
      print("perm error")
      error = 'You do not have permission to view this page'
      return render(request, "login.html", {"error": error})
    else:
      print("pass")
      pass
  else:
    print("not logged in")
    error = 'You need to be logged in to view this resource'
    return render(request, "login.html", {"error": error})




def create_account(request):
  formName = request.POST['name']
  formPhone = request.POST['phone']
  formEmail = request.POST['email']
  formAddress = request.POST['address']
  formPassword = request.POST['password']
  acctype = request.POST['acctype']
  newAccount = Account(
    username=formName,
    password=formPassword,
    role=(1 if acctype == "instructor" else 2),
    name=formName,
    phone=formPhone,
    email=formEmail,
    address=formAddress
  )
  newAccount.save()

  # Helper Method for EditAccount POST
def updateAccount(self, request, selected_account):
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
    selected_account.save()

def editProfileData(self, request, user, field_name, field_type, error_name):
    if request.POST.get(field_name) != "":
        new_data = request.POST.get(field_name)
        if not isinstance(new_data, field_type):
            raise TypeError(f"{error_name} not {field_type.__name__} fails to raise TypeError")

        if new_data == "Null":
            raise ValueError("Null value fails raise ValueError")

        setattr(user, field_name.lower(), new_data)
        user.save()


def queryFromCourses(courses, labs):
  for course in courses:
    course["labs"] = ""
  for lab in labs:
     course = filter(lambda c : c["id"] == lab.course_id, courses)[0]
     course["labs"] += lab.name + ", "
  for course in courses:
     course["labs"] = course["labs"][:-2]
  return courses    


class Management:
    class User:
        @staticmethod
        def login(request, user):
            session = request.session
            print(f"Logging in user: {user.account_id}, {user.name}, {user.role}")
            session['userID'] = user.account_id
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
            session = request.session
            session.clear()
            session['LoggedIn'] = False
    class Account:
        @staticmethod
        def create_account(request):
            if len(Account.objects.filter(username=request.POST["name"])) != 0:
                return "There is already an account with that username."
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
            if acctype == "instructor":
                # creates instructor model
                new_instructor = Instructor(instructor_id=new_account)
                try:
                    new_instructor.full_clean()
                    new_instructor.save()
                except ValidationError as e:
                    print(e)
            else:
                # creates ta model
                new_ta = TA(ta_id=new_account)
                try:
                    new_ta.full_clean()
                    new_ta.save()
                except ValidationError as e:
                    print(e)

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
        def delete_account(request):
            try:
                user_id = request.POST.get('userId')
                Account.objects.get(account_id=user_id).delete()
            except Account.DoesNotExist:
                return 'Cannot delete an account that does not exist'
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

def create_lab(request):
    formName = request.POST['name']
    formTime = request.POST['time']
    formTA = request.POST['ta']
    new_lab = LabSection(formName, formTime, formTA)
    new_lab.save()
    
def update_user_field(user, field_name, new_value, value_type=str, check_null=True):
    if new_value != "":
        if check_null and new_value == "Null":
            raise ValueError("Null value fails raise ValueError")

        if not isinstance(new_value, value_type):
            raise TypeError(f"{field_name} not {value_type.__name__} fails to raise TypeError")

        setattr(user, field_name, new_value)
        user.save()

def update_user_password(user, new_password, repeat_password):
    current_password = user.password

    if new_password != "":
        if current_password == new_password:
            raise ValueError("New password cannot be the same as the old password")

        if type(new_password) != str:
            raise TypeError("Password not string fails to raise TypeError")

        if new_password == "Null":
            raise ValueError("Null value fails raise ValueError")

        # TODO: Check that the new password fits password criteria
        if new_password != repeat_password:
            raise ValueError("Passwords do not match")

        user.password = new_password
        user.save()


from django.shortcuts import render
from .models import *

# call this as loginCheck(request, x) with x being the int value of the role needed to access
def loginCheck(request, role):
  session = request.session
  logged_in = session.get('LoggedIn', False)
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



def authenticate_user(self, username, password):
    try:
        user = Account.objects.get(username=username)
        if user.password == password:
            return user
    except Account.DoesNotExist:
        self.missingUser = True


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

def queryFromCourses(courses, labs, junctions):
   pass
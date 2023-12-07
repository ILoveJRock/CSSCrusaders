from .models import *

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
    # Case 1: emptyLogin
    if request.POST['username'] == '' or request.POST['password'] == '':
        return render(request, 'edit_account.html', {'error': 'Login fields cannot be empty'})

    # Case 2: usernameTaken
    if Account.objects.filter(username=request.POST['username']).exclude(account_id=user_id).exists():
        return render(request, 'edit_account.html', {'error': 'An account with that username already exists.'})

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
def deleteAccount(self, id):
    pass

def editProfileData(self, request, user, field_name, field_type, error_name):
    if request.POST.get(field_name) != "":
        new_data = request.POST.get(field_name)
        if not isinstance(new_data, field_type):
            raise TypeError(f"{error_name} not {field_type.__name__} fails to raise TypeError")

        if new_data == "Null":
            raise ValueError("Null value fails raise ValueError")

        setattr(user, field_name.lower(), new_data)
        user.save()
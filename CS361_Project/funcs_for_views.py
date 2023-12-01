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
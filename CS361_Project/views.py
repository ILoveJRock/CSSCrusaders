from django.shortcuts import render
from django.views import View

from .models import *


class Login(View):
    def get(self, request):
        #TODO Check if there was an error withi login and display error if so
        return render(request, 'Login.html')

    def post(self, request):
        #TODO Check login 
        return render(request, 'Login.html')


class Profile(View):
    def get(self, request):
        return render(request, 'Profile.html')

    def post(self, request):
        return render(request, 'Profile.html')


class EditProfile(View):
    def get(self, request):
        return render(request, 'Profile.html')

    def post(self, request):
        #TODO Edit the profile
        return render(request, 'Profile.html')


class Home(View):
    def get(self, request):
        #TODO Figure out who's logged in and what to display based on their permission levels
        return render(request,"Home.html")


class ManageAccounts(View):
    def get(self, request):
        return render(request, 'Manage.html')

    def post(self, request):
        #TODO Figure out if it's a create/edit/delete operation
        return render(request, 'Manage.html')


class CreateAccount(View):
    def get(self, request):
        return render(request, 'CreateAccount.html')

    def post(self, request):
        if len(Account.objects.filter(id=request.POST.get(id))) != 0:
            return render(request, 'CreateAccount.html', {"message": "There is already an account with that ID."})

        if len(Account.objects.filter(username=request.POST.get(name))) != 0:
            return render(request, 'CreateAccount.html', {"message": "There is already an account with that username."})

        id = request.POST.get(id)
        formName = request.POST.get(name)
        formPhone = request.POST.get(phone)
        formEmail = request.POST.get(email)
        formAddressddress = request.POST.get(address)
        formPassword = request.POST.get(password)
        acctype = request.POST.get(acctype)
        newAccount = Account(
            account_id=id,
            username=formName,
            password=formPassword,
            role=(1 if acctype=="instructor" else 2),
            name=formName,
            phone=formPhone,
            email=formEmail,
            address=formAddress
        )
        newAccount.save()
        return render(request, 'CreateAccount.html')


class EditAccount(View):
    def post(self, request):
        #TODO Edit the account information
        return render(request, 'Manage.html')


class DeleteAccount(View):
    def post(self, request):
        #TODO Delete the account
        return render(request, 'Manage.html')


class Notification(View):
    def get(self, request):
        return render(request, 'NotificationForm.html')

    def post(self, request):
        #TODO Send email to all the users in the email list
        return render(request, 'NotificationForm.html')


class ManageCourse(View):
    def get(self, request):
        #TODO get the courses and labs and pass them to render {"courses": courses, "labs": labs}
        return render(request, 'ManageCourse.html')

    def post(self, request):
        #TODO Post actions for every single action to the courses
        return render(request, 'ManageCourse.html', {"courses": courses, "labs": labs})


#TODO For all of these, persist the course and/or lab selected back to manage course
class CreateCourse(View):
    def post(self, request):
        #TODO Create the course
        return render(request, 'ManageCourse.html')


class CreateLab(View):
    def post(self, request):
        #TODO Create the lab
        return render(request, 'ManageCourse.html')


class EditCourse(View):
    def post(self, request):
        #TODO Edit the course
        return render(request, 'ManageCourse.html')


class EditLab(View):
    def post(self, request):
        #TODO Edit the lab
        return render(request, 'ManageCourse.html')


class DeleteCourse(View):
    def post(self, request):
        #TODO Delete the course
        return render(request, "ManageCourse.html")


class DeleteLab(View):
    def post(self, request):
        #TODO Delete the lab
        return render(request, "ManageCourse.html")


class ManageAssign(View):
    def get(self, request):
        #TODO Ensure only logged in users can see this
        return render(request, 'Assign.html', {"selectedUsers": users, "courses": courses, "labs": labs})
        
    def post(self, request):
        #TODO Figure out if we're assigning or removing a user
        return render(request, 'Assign.html', {"selectedUsers": users, "courses": courses, "labs": labs})


class AssignUser(View):
    def get(self, request):
        #TODO Ensure only logged in users can see this
        return render(request, 'Assign.html')

    def post(self, request):
        #TODO Assign user to course / lab
        return render(request, 'Assign.html')


class RemoveAssign(View):
    def get(self, request):
        #TODO Ensure only logged in users can see this
        return render(request, 'Assign.html')

    def post(self, request):
        #TODO Remove user from course/lab
        return render(request, 'Assign.html')


class Logout(View):
    def get(self, request):
        #TODO Log out and clear all data stored
        return render(request, 'login.html')

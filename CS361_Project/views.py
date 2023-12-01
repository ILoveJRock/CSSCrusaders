from django.middleware.csrf import rotate_token
from django.shortcuts import render, redirect
from django.views import View
from CS361_Project.models import Account
from .models import *
from datetime import datetime
from django.core.mail import send_mail
from funcs_for_views import *


class Login(View):
    def __init__(self):
        # Error Tracking
        self.missingUser = False

    def get(self, request):
        # If the user is already logged in, redirect to home page
        if 'LoggedIn' in request.GET:
            return redirect('/dashboard/')

        return render(request, 'Login.html')

    def post(self, request):
        # Get login details from post request
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate user w/ helper method
        user = self.authenticate_user(username, password)
        # If the user is authenticated, log the user in and redirect them to the ADMIN DASHBOARD page
        if user:
            session = request.session
            session['name'] = user.name
            session['role'] = user.role
            session['LoggedIn'] = True
            return redirect('/dashboard')
        else:
            # If the user is not authenticated, redisplay the page with the appropriate error
            error = 'User does not exist' if self.missingUser else "Incorrect Password"
            return render(request, "login.html", {"error": error})

    def authenticate_user(self, username, password):
        try:
            user = Account.objects.get(username=username)
            if user.password == password:
                return user
        except Account.DoesNotExist:
            self.missingUser = True


class ForgotPassword(View):
    # TODO: Check Username and Send Recovery Email when appropriate
    def get(self, request):
        return render(request, 'ForgotPassword.html')

    def post(self, request):
        return render(request, 'ForgotPassword.html')


class Profile(View):
    def get(self, request):
        request.session['action'] = None
        return render(request, 'Profile.html', {'validForm': 'invalid'})

    def post(self, request):
        request.session['action'] = None
        username = request.session['user']['username']
        user = Account.objects.get(username=username)
        return render(request, 'Profile.html')


class EditProfile(View):
    def get(self, request):
        return render(request, 'EditProfile.html', {'validForm': 'invalid'})

    def post(self, request):
        username = request.session['user']['username']
        user = Account.objects.get(username=username)

        self.editProfileData(request, user, "Name", str, "Name")
        self.editProfileData(request, user, "Phone", int, "Number")
        self.editProfileData(request, user, "Email", str, "Email")
        self.editProfileData(request, user, "Address", str, "Address")
        self.editProfileData(request, user, "Location", str, "Location")
        self.editProfileData(request, user, "Time", str, "Time")

        return render(request, 'EditProfile.html')




class EditPassword(View):
    def get(self, request):
        request.session['action'] = None
        return render(request, 'Profile.html', {'validForm': 'invalid'})

    def post(self, request):
        username = request.session['user']['username']
        user = Account.objects.get(username=username)
        currentpass = user.password

        # TODO move password to own class
        if request.POST.get("NewPassword") != "":
            newPass = request.POST.get("NewPassword")
            if currentpass == newPass:
                error = "New password cannot be the same as old password"
                return render(request, "Profile.html", {"error": error})

            if type(newPass) != str:
                raise TypeError("Password not string fails to raise TypeError")

            if newPass == "Null":
                raise ValueError("Null value fails raise ValueError")

            # TODO check that new password fits password criteria
            if newPass != request.POST.get("NewPasswordRepeat"):
                error = "Passwords do not match"
                return render(request, "Profile.html", {"error": error})

            user.password = newPass
            user.save()
        return render(request, 'Profile.html')


class Home(View):
    def get(self, request):
        if 'LoggedIn' not in request.GET:
            return render(request, "Login.html")
        # TODO Figure out who's logged in and what to display based on their permission levels
        return render(request, "Home.html")


class ManageAccounts(View):
    def get(self, request):
        return render(request, 'ManageAccount.html')

    def post(self, request):
        return render(request, 'ManageAccount.html')


class CreateAccount(View):
    def get(self, request):
        return render(request, 'CreateAccount.html')

    def post(self, request):
        if len(Account.objects.filter(username=request.POST["name"])) != 0:
            return render(request, 'CreateAccount.html', {"message": "There is already an account with that username."})

        create_account(request)
        return render(request, 'CreateAccount.html')


class EditAccount(View):
    def get(self, request):
        user_id = request.GET.get('userId')
        try:
            selected_user = Account.objects.get(account_id=user_id)
            return render(request, 'edit_account.html', {'user': selected_user})
        except Account.DoesNotExist:
            # Handle the case where the account with the specified ID does not exist
            return render(request, 'error_page.html', {'error_message': f"Account with ID {user_id} does not exist."})

    def post(self, request):
        # Get user to edit from accountID
        user_id = request.POST.get('userId')
        selected_account = Account.objects.get(account_id=user_id)

        # Catch errors before changes are made

        # Case 1: emptyLogin
        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'edit_account.html', {'error': 'Login fields cannot be empty'})

        # Case 2: usernameTaken
        if Account.objects.filter(username=request.POST['username']).exclude(account_id=user_id).exists():
            return render(request, 'edit_account.html', {'error': 'An account with that username already exists.'})

        self.updateAccount(request, selected_account)

        # Redirect to ManageAccount view
        return redirect('/manage/')




class DeleteAccount(View):
    def post(self, request):
        user_id = request.GET.get('userId')
        # TODO Delete the account
        return render(request, 'ManageAccount.html')


class Notification(View):
    def get(self, request):
        return render(request, 'NotificationForm.html')

    def post(self, request):
        # TODO Send email to all the users in the email list
        email = request.POST['email']
        subject = request.POST['subject']
        body = request.POST['body']
        send_mail(subject, body, "JoeBidenSaysGiveThisGroupAnA@example.com", [email], fail_silently=False, )
        return redirect('/dashboard/')


class ManageCourse(View):
    def get(self, request):
        # TODO get the courses and labs and pass them to render {"courses": courses, "labs": labs}
        return render(request, 'ManageCourse.html')

    def post(self, request):
        # TODO Post actions for every single action to the courses
        return render(request, 'ManageCourse.html')


# TODO For all of these, persist the course and/or lab selected back to manage course
class CreateCourse(View):
    def post(self, request):
        # TODO Create the course
        return render(request, 'ManageCourse.html')


class CreateLab(View):
    def post(self, request):
        # TODO Create the lab
        return render(request, 'ManageCourse.html')


class EditCourse(View):
    def post(self, request):
        # TODO Edit the course
        return render(request, 'ManageCourse.html')


class EditLab(View):
    def post(self, request):
        # TODO Edit the lab
        return render(request, 'ManageCourse.html')


class DeleteCourse(View):
    def post(self, request):
        # TODO Delete the course
        return render(request, "ManageCourse.html")


class DeleteLab(View):
    def post(self, request):
        # TODO Delete the lab
        return render(request, "ManageCourse.html")


class ManageAssign(View):
    def get(self, request):
        # TODO Ensure only logged in users can see this
        return render(request, 'Assign.html')

    def post(self, request):
        # TODO Figure out if we're assigning or removing a user
        return render(request, 'Assign.html')


class AssignUser(View):
    def get(self, request):
        # TODO Ensure only logged in users can see this
        return render(request, 'Assign.html')

    def post(self, request):
        # TODO Assign user to course / lab
        return render(request, 'Assign.html')


class RemoveAssign(View):
    def get(self, request):
        # TODO Ensure only logged in users can see this
        return render(request, 'Assign.html')

    def post(self, request):
        # TODO Remove user from course/lab
        return render(request, 'Assign.html')


class Logout(View):
    def get(self, request):
        request.session.clear()
        return render(request, 'login.html')


class AdminDashboard(View):
    def get(self, request):
        return render(request, 'AdminDashboard.html')

    def post(self, request):
        return render(request, 'AdminDashboard.html')


class ViewContact(View):
    def get(self, request):
        return render(request, 'view_contact_info.html')

    def post(self, request):
        return render(request, 'view_contact_info.html')

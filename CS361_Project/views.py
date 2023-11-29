from django.shortcuts import render, redirect
from django.views import View
from CS361_Project.models import Account


class Login(View):
    def __init__(self):
        # Error Tracking
        self.missingUser = False

    def get(self, request):
        # If the user is already logged in, redirect to home page
        if 'LoggedIn' in request.GET:
            return redirect('/')

        return render(request, 'Login.html')

    def post(self, request):
        # Get login details from post request
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate user w/ helper method
        user = self.authenticate_user(username, password)
        # If the user is authenticated, log the user in and redirect them to the home page
        if user:
            session = request.session
            session['name'] = user.name
            session['role'] = user.role
            session['LoggedIn'] = True
            return redirect('/')
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
        return render(request, 'Profile.html')

    def post(self, request):
        return render(request, 'Profile.html')


class EditProfile(View):
    def get(self, request):
        return render(request, 'Profile.html')

    def post(self, request):
        # TODO Edit the profile
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
        if len(Account.objects.filter(account_id=request.POST["id"])) != 0:
            return render(request, 'CreateAccount.html', {"message": "There is already an account with that ID."})

        if len(Account.objects.filter(username=request.POST["name"])) != 0:
            return render(request, 'CreateAccount.html', {"message": "There is already an account with that username."})

        formId = request.POST["id"]
        # TODO: Fix these errors by using POST['variable'], see below
        formName = request.POST['name']
        formPhone = request.POST['phone']
        formEmail = request.POST['email']
        formAddress = request.POST['address']
        formPassword = request.POST['password']
        acctype = request.POST['acctype']
        newAccount = Account(
            account_id=formId,
            username=formName,
            password=formPassword,
            role=(1 if acctype == "instructor" else 2),
            name=formName,
            phone=formPhone,
            email=formEmail,
            address=formAddress
        )
        newAccount.save()
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
        return render(request, 'NotificationForm.html')


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
        # TODO Log out and clear all data stored
        return render(request, 'login.html')

from django.middleware.csrf import rotate_token
from django.shortcuts import render, redirect
from django.views import View
from CS361_Project.models import Account
from .models import *
from datetime import datetime
from django.core.mail import send_mail
from .functions import *
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator


class Login(View):
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
        user = authenticate_user(self, username, password)
        # If the user is authenticated, log the user in and redirect them to the ADMIN DASHBOARD page
        # TODO: Each role should have its own dash
        if user:
            Management.User.login(request, user)
            if (user.role == 0):
                return redirect('/dashboard')
            else:
                return redirect('home')
        else:
            # If the user is not authenticated, redisplay the page with the appropriate error
            error = 'User does not exist' if not user else "Incorrect Password"
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
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, 'ForgotPassword.html')

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, 'ForgotPassword.html')


class Profile(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        request.session['action'] = None
        user = Account.objects.get(username=request.session['name'])
        named = user.name
        phone = user.phone
        email = user.email
        address = user.address
        office_hour_location = user.office_hour_location
        office_hour_time = user.office_hour_time
        return render(request, 'Profile.html', {"named": named, "phone": phone, "email": email, "address": address, "office_hour_location": office_hour_location, "office_hour_time": office_hour_time, 'validForm': 'invalid'})

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        request.session['action'] = None
        return render(request, 'Profile.html')


class EditProfile(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, 'EditProfile.html', {'validForm': 'invalid'})

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        user = Account.objects.get(username=request.session['name'])
        if request.POST.get("Name") != "":
            newName = request.POST.get("Name")
            if type(newName) != str:
                raise TypeError("Name not string fails to raise TypeError")

            if newName == "Null":
                raise ValueError("Null value fails raise ValueError")

            user.name = newName
            user.save()

        if request.POST.get("Phone") != "":
            newNum = request.POST.get("Phone")
            if type(newNum) != int:
                raise TypeError("Number not integer fails to raise TypeError")

            if newNum == "Null":
                raise ValueError("Null value fails raise ValueError")

            user.phone = newNum
            user.save()

        if request.POST.get("Email") != "":
            #TODO valid email check (contains @ and .)
            newEmail = request.POST.get("Email")
            if type(newEmail) != str:
                raise TypeError("Email not string fails to raise TypeError")

            if newEmail == "Null":
                raise ValueError("Null value fails raise ValueError")

            user.email = newEmail
            user.save()

        if request.POST.get("Address") != "":
            newAddress = request.POST.get("Address")
            if type(newAddress) != str:
                raise TypeError("Address not string fails to raise TypeError")

            if newAddress == "Null":
                raise ValueError("Null value fails raise ValueError")

            user.address = newAddress
            user.save()

        if request.POST.get("Location") != "":
            newLocation = request.POST.get("Location")
            if type(newLocation) != str:
                raise TypeError("Location not string fails to raise TypeError")

            if newLocation == "Null":
                raise ValueError("Null value fails raise ValueError")

            user.office_hour_location = newLocation
            user.save()

        if request.POST.get("Time") != "":
            #TODO valid time check
            newTime = request.POST.get("Time")
            if type(newTime) != str:
                raise TypeError("Time not string fails to raise TypeError")

            if newTime == "Null":
                raise ValueError("Null value fails raise ValueError")

            user.office_hour_time = newTime
            user.save()

        return render(request, 'EditProfile.html')


class EditPassword(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view        if result: return result
        request.session['action'] = None
        return render(request, 'Profile.html', {'validForm': 'invalid'})

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view        if result: return result
        if result: return result
        user = Account.objects.get(username=request.session['name'])
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
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, "Home.html")


class ManageAccounts(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        accounts = Account.objects.all()
        
        selected_user_id = request.POST.get('selected_user_id')
        
        print(f"Selected User ID: {selected_user_id}")
        
        selected_user = None
        if selected_user_id:
            try:
                selected_user = Account.objects.get(account_id=selected_user_id)
            except Account.DoesNotExist:
                # Handle the case where the account with the specified ID does not exist
                pass
        
        query = [{"role": account.role, "named": account.name, "phone": account.phone, "email": account.email, "address": account.address, "office_hour_location": account.office_hour_location, "office_hour_time": account.office_hour_time} for account in accounts]
        
        return render(request, 'Manage_Account.html', {"accounts": query, "selected_user": selected_user})

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        
        selected_user_id = request.POST.get('selected_user_id')
        request.session['selected_user_id'] = selected_user_id
        
        return self.get(request)
        


class CreateAccount(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'CreateAccount.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        error = Management.Account.create_account(request)
        if error:
            return render(request, 'CreateAccount.html', {"message": error})
        return redirect('/manage/')


class EditAccount(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        user_id = request.GET.get('userId')
        # Get the selected user
        try:
            selected_user = Account.objects.get(account_id=user_id)
            return render(request, 'edit_account.html', {'user': selected_user})
        except Account.DoesNotExist:
            # Handle the case where the account with the specified ID does not exist
            return render(request, 'error_page.html', {'error_message': f"Account with ID {user_id} does not exist."})

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        selected_account = Account.objects.get(account_id=request.POST.get('userId'))
        error = Management.Account.updateAccount(request, selected_account)
        if error:
            return render(request, 'edit_account.html', {'error' : error})
        # Redirect to ManageAccount view
        return redirect('/manage/')


class DeleteAccount(View):
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        user_id = request.GET.get('userId')
        Management.Account.deleteAccount(request, user_id)
        return render(request, 'ManageAccount.html')


class Notification(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'NotificationForm.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Send email to all the users in the email list
        email = request.POST['email']
        subject = request.POST['subject']
        body = request.POST['body']
        send_mail(subject, body, "nate.valentine.r@gmail.com", [email], fail_silently=False, )
        return redirect('/dashboard/')


class ManageCourse(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO get the courses and labs and pass them to render {"courses": courses, "labs": labs}
        return render(request, 'ManageCourse.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Post actions for every single action to the courses
        return render(request, 'ManageCourse.html')


# TODO For all of these, persist the course and/or lab selected back to manage course
class CreateCourse(View):
    def get(self, request):
        return render(request, 'CreateCourse.html')
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Create the course
        return render(request, 'CreateCourse.html')


class CreateLab(View):
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Create the lab
        return render(request, 'ManageCourse.html')


class EditCourse(View):
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Edit the course
        return render(request, 'ManageCourse.html')


class EditLab(View):
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Edit the lab
        return render(request, 'ManageCourse.html')


class DeleteCourse(View):
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Delete the course
        return render(request, "ManageCourse.html")


class DeleteLab(View):
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Delete the lab
        return render(request, "ManageCourse.html")


class ManageAssign(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'Assign.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Figure out if we're assigning or removing a user
        return render(request, 'Assign.html')


class AssignUser(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'Assign.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Assign user to course / lab
        return render(request, 'Assign.html')


class RemoveAssign(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'Assign.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        # TODO Remove user from course/lab
        return render(request, 'Assign.html')


@method_decorator(cache_control(no_cache=True, must_revalidate=True), name='dispatch')
class Logout(View):
    def get(self, request):
        Management.User.logout(request)
        return render(request, 'login.html')


class AdminDashboard(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'AdminDashboard.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'AdminDashboard.html')


class ViewContact(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, 'view_contact_info.html')

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, 'view_contact_info.html')

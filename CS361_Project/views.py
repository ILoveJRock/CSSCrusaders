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
from django.db.models import Max


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
        user = Management.User.authenticate_user(username, password)
        # If the user is authenticated, log the user in and redirect them to the ADMIN DASHBOARD page
        # TODO: Each role should have its own dash
        if user:
            Management.User.login(request, user)
            if (user.role == 0):
                return redirect('/dashboard')
            elif (user.role == 1):
                return redirect('/dashboard/prof')
            else:
                return redirect('/dashboard/ta')
        else:
            # If the user is not authenticated, redisplay the page with the appropriate error
            error = 'User does not exist' if not user else "Incorrect Password"
            return render(request, "login.html", {"error": error})


class ForgotPassword(View):
    # TODO: Check Username and Send Recovery Email when appropriate
    def get(self, request):
        return render(request, 'ForgotPassword.html')

    def post(self, request):
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
        session = request.session
        current_account = Account.objects.get(account_id=session.get('userID'))
        return render(request, 'EditProfile.html', {'currentAccount': current_account})

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        user = Account.objects.get(username=request.session['name'])
        update_user_field(user, "name", request.POST.get("Name"))
        update_user_field(user, "phone", request.POST.get("Phone"))
        update_user_field(user, "email", request.POST.get("Email"))
        update_user_field(user, "address", request.POST.get("Address"))
        update_user_field(user, "office_hour_location", request.POST.get("Location"))
        update_user_field(user, "office_hour_time", request.POST.get("Time"))
        return render(request, 'EditProfile.html', {'currentAccount': user})


class EditPassword(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        request.session['action'] = None
        return render(request, 'Profile.html', {'validForm': 'invalid'})

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        user = Account.objects.get(username=request.session['name'])
        update_user_password(user, request.POST.get("NewPassword"), request.POST.get("NewPasswordRepeat"))
        return render(request, 'Profile.html')


class Home(View):
    def get(self, request):
        return render(request, "Home.html")


class ManageAccounts(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        accounts = Account.objects.all()
        
        selected_user_id = request.POST.get('selected_user_id')
        selected_user = None
        if selected_user_id:
            try:
                selected_user = Account.objects.get(account_id=selected_user_id)
            except Account.DoesNotExist:
                return render(request, 'error_page.html', {'error_message': f"Account with ID {selected_user_id} does not exist."})

        
        query = [{"id" : account.account_id, "role": account.role, "named": account.name, "phone": account.phone, "email": account.email, "address": account.address, "office_hour_location": account.office_hour_location, "office_hour_time": account.office_hour_time} for account in accounts]
        
        return render(request, 'Manage_Account.html', {"accounts": query, "selected_user": selected_user})


    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
  
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
        selected_user = Management.Account.get_from_id(user_id)
        if selected_user:
            request.session['selected_user_id'] = user_id
            return render(request, 'edit_account.html', {'user': selected_user})
        else:
            return render(request, 'error_page.html', {'error_message': f"Account with ID {user_id} does not exist."})

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        
        user_id = request.session.get('selected_user_id')
        
        if user_id is None:
            return render(request, 'error_page.html', {'error_message': "Can't edit null user"})

        # Get the selected user based on the account_id
        user = Management.Account.get_from_id(user_id)
        if user is None:
            return render(request, 'error_page.html', {'error_message': f"Account with ID {user_id} does not exist."})
        
        error = Management.Account.update_account(request, user)
        if error:
            return render(request, 'edit_account.html', {'error' : error})
        # Redirect to ManageAccount view
        return redirect('/manage/')

class ManageCourses(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result

        courses = Course.objects.all()
        labs = LabSection.objects.all()
        query1 = [{"name": course.name, "dept": course.dept, "id": course.Labid} for course in courses]
        query2 = [{"name": lab.name, "course_id": lab.course} for lab in labs]
        query = queryFromCourses(query1, query2)
        return render(request, 'ManageCourse.html',  {"courses": query})


    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result

        selected_course_id = request.POST["selected_course_id"]
        selected_course = Course.objects.filter(Labid=selected_course_id).first()
        
        courses = request.POST["courses"]
        return render(request, 'ManageCourse.html', {"courses": courses, "selected_course": selected_course_id})


class DeleteAccount(View):
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        msg = Management.Account.delete_account(request)
        if not msg:
            # Deletion was successful, add a success message
            messages.success(request, 'Account Deleted Successfully')
        else:
            # Deletion failed, add an error message
            messages.error(request, msg)
        return redirect('/manage/')


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
        result = loginCheck(request, 0)
        if result: return result
        proffessors = Account.objects.filter(role=1)
        return render(request, 'CreateCourse.html', {'profs' : proffessors})
    
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        course_name = request.POST.get('name')
        department = request.POST.get('dept')
        proffessor = request.POST.get('section') # Unused for now
        max_id = Course.objects.aggregate(Max('Courseid'))['Courseid__max']
        new_id = (max_id or 0) + 1
        new_course = Course(
            Courseid=new_id,
            name=course_name,
            dept=department,
            prof=proffessor

        )
        new_course.save()
        return redirect('create_course')


class CreateLab(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        selected_course = Course.objects.get(Courseid=request.GET.get('courseId'))
        tas = TA.objects.filter(course=selected_course)
        return render(request, 'CreateLab.html', {"tas": tas})
    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        if len(LabSection.objects.filter(name=request.POST["name"])) != 0:
            return render(request, 'CreateLab.html', {"message": "There is already a lab section with that number."})
        create_lab(request)
        return render(request, 'CreateLab.html')


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
        return redirect('/login/')


class AdminDashboard(View):
    def get(self, request):
        # Small little hack, checks if user is supervisor, if not it directs them to the proper dashboard
        session = request.session
        current_account = Account.objects.get(account_id=session.get('userID'))
        if current_account.role == 1:  # Instructor
            return redirect('prof_dashboard')
        elif current_account.role == 2:  # TA
            return redirect('ta_dashboard')
        else:  # Admin
            return render(request, 'AdminDashboard.html')

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'AdminDashboard.html')

class ProfDashboard(View):
    def get(self, request):
        result = loginCheck(request, 1)
        if result: return result
        return render(request, 'ProfDashboard.html')
    def post(self, request):
        result = loginCheck(request, 1)
        if result: return result
        return render(request, 'ProfDashboard.html')

class TADashboard(View):
    def get(self, request):
        result = loginCheck(request, 2)
        if result: return result
        return render(request, 'TADashboard.html')

    def post(self, request):
        result = loginCheck(request, 2)
        if result: return result
        return render(request, 'TADashboard.html')

class ViewContact(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, 'view_contact_info.html')

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        return render(request, 'view_contact_info.html')

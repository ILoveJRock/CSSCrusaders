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
from django.forms import Form, ModelChoiceField
from django import forms



class Login(View):
    def get(self, request):
        # If the user is already logged in, redirect to home page
        if 'LoggedIn' in request.GET:
            return redirect('/dashboard/')
        return render(request, 'Login.html')

    def post(self, request):
        return login_post(self, request)


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
        return render(request, profile_information(request))

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        request.session['action'] = None
        return render(request, 'Profile.html')


class EditProfile(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        current_account = Account.objects.get(account_id=request.session.get('userID'))
        return render(request, 'EditProfile.html', {'currentAccount': current_account})

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return 
        # Edit profile information of user currently logged in
        Management.Profile.edit_profile(request, Account.objects.get(username=request.session['name']))
        return redirect('profile')


class EditPassword(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can 
        if result: return result
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
        return Management.Account.manage_account(request)


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
        # Returns error if account wasn't able to be created
        error = Management.Account.create_account(request)
        if error: return render(request, 'CreateAccount.html', {"message": error})
        return redirect('/manage/') # Redirect to ManageAccount view


class EditAccount(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return Management.Account.edit_account_GETview(request)


    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return Management.Account.edit_account_POSTview(request)
        


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
        Management.Notification.send_notification(request)
        return redirect('/dashboard/')


class ManageCourse(View):
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return render(request, 'ManageCourse.html',  Management.Course.manage_course(request))

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        return self.get(request)


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
        Management.Course.create_course(request)
        return redirect('course')


class CreateLab(View):
    template_name = 'CreateLab.html'
    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result
        selected_course_id = request.GET.get('courseId')

        # Check if the course ID is provided
        if not selected_course_id:
            return render(request, 'error_page.html', {'error_message': "No course ID provided."})

        try:
            selected_course = Course.objects.get(Courseid=selected_course_id)
            tas = Account.objects.filter(role=2)
            return render(request, self.template_name, {"tas": tas, "selected_course": selected_course})
        except Course.DoesNotExist:
            return render(request, 'error_page.html', {'error_message': "Selected course does not exist."})

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result
        selected_course_id = request.POST.get('courseId')
        if not selected_course_id:
            return render(request, 'error_page.html', {'error_message': "No course ID provided."})

        try:
            selected_course = Course.objects.get(Courseid=selected_course_id)
        except Course.DoesNotExist:
            return render(request, 'error_page.html', {'error_message': "Selected course does not exist."})

        if len(LabSection.objects.filter(name=request.POST.get("name"))) != 0:
            return render(request, self.template_name, {"message": "There is already a lab section with that number.",
                                                        "tas": Account.objects.filter(role=2),
                                                        "selected_course": selected_course})

        create_lab(request)
        return render(request, 'ManageCourse.html')


class EditCourse(View):
    template_name = 'EditCourse.html'

    from CS361_Project.models import Instructor  # Import the Instructor model at the top of your file

    from CS361_Project.models import Instructor  # Import the Instructor model at the top of your file

    def get(self, request):
        result = loginCheck(request, 0)
        if result: return result

        selected_course_id = request.GET.get('courseId')
        if not selected_course_id:
            return render(request, 'error_page.html',
                          {'error_message': "No course ID provided."})
        try:
            selected_course = Course.objects.get(Courseid=selected_course_id)
            instructors = Account.objects.filter(role=1)  # Fetch all Accounts with the Instructor rol
            return render(request, self.template_name, {'selected_course': selected_course, 'profs': instructors})
        except Course.DoesNotExist:
            return render(request, 'error_page.html',
                          {'error_message': f"Course with ID {selected_course_id} does not exist."})

    def post(self, request):
        result = loginCheck(request, 0)
        if result: return result

        selected_section_id = request.POST.get('selected_section_id')
        try:
            selected_section = Course.objects.get(Courseid=selected_section_id)
        except Course.DoesNotExist:
            return render(request, 'error_page.html',
                          {'error_message': f"Section with ID {selected_section_id} does not exist."})

        form = EditCourseLabSectionForm(request.POST, instance=selected_section)
        if form.is_valid():
            form.save()
            return redirect('/course')

        return render(request, self.template_name, {'form': form, 'selected_section': selected_section})


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
        Management.Course.delete_course(request)
        return redirect("course")


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

# TODO MOVE THIS TO A FORM CLASS SUPER BAD PRACTICE THAT IT'S IN HERE!!!!
class UserForm(Form):
    user = ModelChoiceField(queryset=Account.objects.all())

class ViewContact(View):
    def get(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        form = UserForm()
        return render(request, 'view_contact_info.html', {'form': form})

    def post(self, request):
        result = loginCheck(request, 2) # Everyone logged in can view
        if result: return result
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            return render(request, 'view_contact_info.html', {'form': form, 'selected_user': user})
        return render(request, 'view_contact_info.html', {'form': form})


class EditCourseLabSectionForm(Form):
    class Meta:
        model = Course_LabSection
        fields = ['labSection']

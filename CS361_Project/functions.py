from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.db.models import Max
from .models import *


def profile_information(request):
    request.session["action"] = None
    user = Account.objects.get(username=request.session["name"])
    named = user.name
    phone = user.phone
    email = user.email
    address = user.address
    office_hour_location = user.office_hour_location
    office_hour_time = user.office_hour_time
    return {
        "named": named,
        "phone": phone,
        "email": email,
        "address": address,
        "office_hour_location": office_hour_location,
        "office_hour_time": office_hour_time,
        "validForm": "invalid",
    }


def authenticate_user(self, username, password):
    try:
        user = Account.objects.get(username=username)
        if user.password == password:
            return user
    except Account.DoesNotExist:
        self.missingUser = True


# call this as loginCheck(request, x) with x being the int value of the role needed to access
def loginCheck(request, role):
    session = request.session
    logged_in = session.get(
        "LoggedIn", False
    )  # `session.get('LoggedIn', False)` is retrieving the value of the 'LoggedIn' key from
    # the session dictionary. If the key does not exist, it will return the default value of
    # False.
    session.get("LoggedIn", False)
    user_role = session.get("role", 3)
    if logged_in:
        if user_role > role:
            print("perm error")
            error = "You do not have permission to view this page"
            return render(request, "login.html", {"error": error})
        else:
            print("pass")
            pass
    else:
        print("not logged in")
        error = "You need to be logged in to view this resource"
        return render(request, "login.html", {"error": error})


def create_account(request):
    formName = request.POST["name"]
    formPhone = request.POST["phone"]
    formEmail = request.POST["email"]
    formAddress = request.POST["address"]
    formPassword = request.POST["password"]
    acctype = request.POST["acctype"]
    newAccount = Account(
        username=formName,
        password=formPassword,
        role=(1 if acctype == "instructor" else 2),
        name=formName,
        phone=formPhone,
        email=formEmail,
        address=formAddress,
    )
    newAccount.save()

    # Helper Method for EditAccount POST


def updateAccount(self, request, selected_account):
    # Update user information with form data
    selected_account.username = request.POST["username"]
    selected_account.password = request.POST["password"]
    selected_account.role = request.POST["role"]
    selected_account.name = request.POST["name"]
    selected_account.phone = request.POST["phone"]
    selected_account.email = request.POST["email"]
    selected_account.address = request.POST["address"]
    selected_account.office_hour_location = request.POST["office_hour_location"]
    selected_account.office_hour_time = request.POST["office_hour_time"]

    # Save the changes
    selected_account.save()


def editProfileData(self, request, user, field_name, field_type, error_name):
    if request.POST.get(field_name) != "":
        new_data = request.POST.get(field_name)
        if not isinstance(new_data, field_type):
            raise TypeError(
                f"{error_name} not {field_type.__name__} fails to raise TypeError"
            )

        if new_data == "Null":
            raise ValueError("Null value fails raise ValueError")

        setattr(user, field_name.lower(), new_data)
        user.save()


def queryFromCourses(courses, instructors, accounts):
    for instructor in instructors:
        print(courses)
        print(instructor)
        course = None
        for c in courses:
            print(c)
            if c["id"] == instructor["course"]:
                course = c
                break
        if course != None:
            print("found course")
            account = None
            for a in accounts:
                if a["id"] == instructor["id"]:
                    account = a
            course["instructor"] = account["name"]
    print(courses)
    return courses


class Management:
    class User:
        @staticmethod
        def login(request, user):
            session = request.session
            print(f"Logging in user: {user.account_id}, {user.name}, {user.role}")
            session["userID"] = user.account_id
            session["name"] = user.name
            session["role"] = user.role
            session["LoggedIn"] = True

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
            session["LoggedIn"] = False

    class Account:
        @staticmethod
        def get_from_id(id):
            try:
                return Account.objects.get(account_id=id)
            except Account.DoesNotExist:
                return None

        @staticmethod
        def edit_account_GETview(request):
            user_id = request.GET.get("userId")
            # Get the selected user
            selected_user = Management.Account.get_from_id(user_id)
            if selected_user:
                request.session["selected_user_id"] = user_id
                return render(request, "edit_account.html", {"user": selected_user})
            else:
                return render(
                    request,
                    "error_page.html",
                    {"error_message": f"Account with ID {user_id} does not exist."},
                )
        @staticmethod
        def edit_account_POSTview(request):
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
            return redirect('/manage/') # Redirect to ManageAccount view
        @staticmethod
        def manage_account(request):
            accounts = Account.objects.all()
            selected_user_id = request.POST.get("selected_user_id")
            selected_user = None
            if selected_user_id:
                try:
                    selected_user = Account.objects.get(account_id=selected_user_id)
                except Account.DoesNotExist:
                    return render(
                        request,
                        "error_page.html",
                        {
                            "error_message": f"Account with ID {selected_user_id} does not exist."
                        },
                    )
            query = [
                {
                    "id": account.account_id,
                    "role": account.role,
                    "named": account.name,
                    "phone": account.phone,
                    "email": account.email,
                    "address": account.address,
                    "office_hour_location": account.office_hour_location,
                    "office_hour_time": account.office_hour_time,
                }
                for account in accounts
            ]
            return render(
                request,
                "Manage_Account.html",
                {"accounts": query, "selected_user": selected_user},
            )

        @staticmethod
        def create_account(request):
            form_username = request.POST["username"]
            if len(Account.objects.filter(username=form_username)) != 0:
                return "There is already an account with that username."
            form_name = request.POST["name"]
            form_phone = request.POST["phone"]
            form_email = request.POST["email"]
            form_address = request.POST["address"]
            form_password = request.POST["password"]
            acctype = request.POST["acctype"]
            new_account = Account(
                username=form_username,
                password=form_password,
                role=(1 if acctype == "instructor" else 2),
                name=form_name,
                phone=form_phone,
                email=form_email,
                address=form_address,
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
            if (
                not request.POST
                or request.POST["username"] == ""
                or request.POST["password"] == ""
            ):
                return "Login fields cannot be empty"
            # Case 2: usernameTaken
            user_id = selected_account.account_id
            if (
                Account.objects.filter(username=request.POST["username"])
                .exclude(account_id=user_id)
                .exists()
            ):
                return "An account with that username already exists."
            # Case 3: invalid fields
            try:
                # Update user information with form data
                selected_account.username = request.POST["username"]
                selected_account.password = request.POST["password"]
                selected_account.role = request.POST["role"]
                selected_account.name = request.POST["name"]
                selected_account.phone = request.POST["phone"]
                selected_account.email = request.POST["email"]
                selected_account.address = request.POST["address"]
                selected_account.office_hour_location = request.POST[
                    "office_hour_location"
                ]
                selected_account.office_hour_time = request.POST["office_hour_time"]

                # Save the changes
                selected_account.full_clean()
                selected_account.save()

                return "Account information updated successfully."
            except ValidationError as e:
                return str(e)

        @staticmethod
        def delete_account(request):
            try:
                user_id = request.POST.get("userId")
                Account.objects.get(account_id=user_id).delete()
                messages.success(request, "Account Deleted Successfully")

            except Account.DoesNotExist:
                messages.error(request, "Account Deletion Failed: DoesNotExist")

    class Course:
        @staticmethod
        def manage_course(request):
            selected_course_id = request.POST.get("selected_course_id")
            selected_course = None
            if selected_course_id:
                selected_course = Course.objects.get(Courseid=selected_course_id)
            courses = Course.objects.all()
            instructors = Instructor.objects.all()
            accounts = Account.objects.all()
            query1 = [
                {"name": course.name, "dept": course.dept, "id": course.Courseid}
                for course in courses
            ]
            query2 = [
                {
                    "id": instructor.instructor_id.account_id,
                    "course": instructor.course.Courseid if instructor.course else None,
                }
                for instructor in instructors
            ]
            query3 = [
                {"id": account.account_id, "name": account.name} for account in accounts
            ]
            query = queryFromCourses(query1, query2, query3)
            return {"courses": query, "selected_course": selected_course}

        @staticmethod
        def create_course(request):
            course_name = request.POST.get("name")
            department = request.POST.get("dept")
            proffessor = request.POST.get("professor")
            max_id = Course.objects.aggregate(Max("Courseid"))["Courseid__max"]
            new_id = (max_id or 0) + 1
            new_course = Course(Courseid=new_id, name=course_name, dept=department)
            new_course.save()
            instructor = Instructor.objects.filter(instructor_id=proffessor)
            instructor.course = new_course

        @staticmethod
        def delete_course(request):
            selected_course_id = request.POST.get('courseId')
            try:
                selected_course = Course.objects.get(Courseid=selected_course_id)
                selected_course.delete()
                messages.success(request, 'Course Deleted Successfully')
            except Course.DoesNotExist:
                messages.error(request, 'Course does not exist')

    class Notification:
        @staticmethod
        def send_notification(request):
            session = request.session
            account = Account.objects.get(account_id=session.get("userID"))
            if account.role == 0:  # account is a supervisor
                # Fetch all accounts with a valid email
                accounts = Account.objects.exclude(email__exact="")
                # Extract email addresses
                emails = [account.email for account in accounts]
            elif account.role == 1:  # account is an instructor
                # Get the selected course
                course_id = request.POST["course"]
                course = Course.objects.get(course_id=course_id)
                # Fetch all TAs associated with the selected course
                tas = TA.objects.filter(course=course)
                # Extract email addresses
                emails = [ta.account.email for ta in tas]
            subject = request.POST["subject"]
            body = request.POST["body"]
            send_mail(
                subject, body, "nate.valentine.r@gmail.com", emails, fail_silently=True
            )

        @staticmethod
        def notification_context(request):
            session = request.session
            account = Account.objects.get(account_id=session.get("userID"))
            if account.role == 0:  # account is a supervisor
                context = {"is_supervisor": True}
            elif account.role == 1:  # account is an instructor
                instructor = Instructor.objects.get(instructor_id=account.account_id)
                courses = Course.objects.filter(instructor=instructor)
                context = {"courses": courses}

    class Profile:
        @staticmethod
        def edit_profile_data(request, user, field_name, field_type, error_name):
            if request.POST.get(field_name) != "":
                new_data = request.POST.get(field_name)
                if not isinstance(new_data, field_type):
                    raise TypeError(
                        f"{error_name} not {field_type.__name__} fails to raise TypeError"
                    )

                if new_data == "Null":
                    raise ValueError("Null value fails raise ValueError")

                setattr(user, field_name.lower(), new_data)
                user.save()

        @staticmethod
        def edit_profile(request, user):
            update_user_field(user, "name", request.POST.get("Name"))
            update_user_field(user, "phone", request.POST.get("Phone"))
            update_user_field(user, "email", request.POST.get("Email"))
            update_user_field(user, "address", request.POST.get("Address"))
            update_user_field(
                user, "office_hour_location", request.POST.get("Location")
            )
            update_user_field(user, "office_hour_time", request.POST.get("Time"))


def create_lab(request):
    formName = request.POST['name']
    formTime = request.POST['time']
    formTA = request.POST['ta']
    new_lab = LabSection(name=formName, time=formTime)
    new_lab.save()
    selected_course_id = request.POST['courseId']
    selected_course = Course.objects.get(Courseid=selected_course_id)
    ta_instance = TA.objects.get(ta_id=formTA)
    ta_instance.course = selected_course
    ta_instance.section = new_lab
    ta_instance.save()
    new_lab_course = Course_LabSection(course=selected_course, labSection=new_lab)
    new_lab_course.save()


def update_user_field(user, field_name, new_value, value_type=str, check_null=True):
    if new_value != "":
        if check_null and new_value == "Null":
            raise ValueError("Null value fails raise ValueError")

        if not isinstance(new_value, value_type):
            raise TypeError(
                f"{field_name} not {value_type.__name__} fails to raise TypeError"
            )

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


def login_post(self, request):
    username = request.POST["username"]
    password = request.POST["password"]
    # Authenticate user w/ helper method
    user = authenticate_user(self, username, password)
    # If the user is authenticated, log the user in and redirect them to the ADMIN DASHBOARD page
    if user:
        Management.User.login(request, user)
        if user.role == 0:
            return redirect("/dashboard")
        elif user.role == 1:
            return redirect("/dashboard/prof")
        else:
            return redirect("/dashboard/ta")
    else:
        # If the user is not authenticated, redisplay the page with the appropriate error
        error = "User does not exist" if not user else "Incorrect Password"
        return render(request, "login.html", {"error": error})

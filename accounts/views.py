from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileUpdateForm
from .models import Userdetail, Usergroupdetail, Course, CourseAccess
from django.contrib.auth.models import User
from .decorators import admin_required, role_required
from django.http import HttpResponse
from django.contrib import messages

# Admin creates a new user

def Home(request):
    return render(request,"accounts/base.html")

@login_required(login_url='login')
def user_list(request):
    users = Userdetail.objects.select_related('usergroupid').all()  # Fetch all users with related user group
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required(login_url='login')
def user_detail(request, user_id):
    user = get_object_or_404(Userdetail, userid=user_id)
    return render(request, 'accounts/user_detail.html', {'user': user})

@login_required(login_url='login')
@role_required(["Admin", "Staff"])
def register(request):
    user = request.user  # Get logged-in user
    
    try:
        # Fetch user details
        user_detail = Userdetail.objects.get(username=user.username)
        user_role = user_detail.usergroupid.usergroupname  # Get role name
    except Userdetail.DoesNotExist:
        user_role = None
    
    # Assign createdby value
    created_by = None
    if user_role == 'Admin':
        created_by = 1
        user_groups = Usergroupdetail.objects.all()  # Fetch all user groups
    elif user_role == 'Staff':
        created_by = 2
        user_groups = Usergroupdetail.objects.exclude(usergroupname='Admin')  # Exclude Admin group
    else:
        return HttpResponse("You don't have permission to register a user.")
    
 

    if request.method == 'POST':
        username = request.POST.get('username')
        useremail = request.POST.get('useremail')
        usercontactnumber = request.POST.get('usercontactnumber')
        userpassword = request.POST.get('userpassword')
        usergroupid = request.POST.get('usergroupid')
        usergender = request.POST.get('usergender')

        # if created_by:
            # ✅ Save to the database
        new_user = Userdetail(
                username=username,
                useremail=useremail,
                usercontactnumber=usercontactnumber,
                userpassword=userpassword,  # ⚠️ Hash password before saving in production!
                usergroupid_id=usergroupid,  # FK reference
                usergender=usergender,
                createdby=created_by,
            )
        new_user.save()
        messages.success(request, "User registered successfully!")
        # ✅ Redirect based on role
        if created_by == 1:  # Admin
            return redirect('admin_dashboard')
        elif created_by == 2:  # Staff
            return redirect('staff_dashboard')
        # else:
        messages.error(request, "You don't have permission to register a user.")

    return render(request, 'accounts/register.html', {'user_groups': user_groups, 'created_by': created_by})

# User Login
# @login_required
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next') or request.POST.get('next')  # ✅ Get `next` URL if exists

        user = authenticate(request, username=username, password=password)
        print(f"User authenticated: {user}")  # Debugging Step 1

        if user is not None:
            login(request, user)
            print(f"User is now logged in: {request.user.is_authenticated}")  # Debugging Step 2

            try:
                user_detail = Userdetail.objects.get(username=username)
                
                # ✅ Store user details in session
                request.session['user_id'] = user_detail.userid
                request.session['username'] = user_detail.username
                request.session['user_role'] = user_detail.usergroupid.usergroupname
                request.session.modified = True  # ✅ Ensure session is saved
                request.session.save()

                print(f"Session Data: {dict(request.session)}")  # ✅ Debugging Step 3

                # ✅ Redirect to `next` URL if available
                if next_url:
                    print(f"Redirecting to next: {next_url}")
                    return redirect(next_url)

                # ✅ Otherwise, redirect based on role
                return redirect_based_on_role(user_detail)

            except Userdetail.DoesNotExist:
                print("User details not found.")
                return render(request, 'accounts/login.html', {'error': 'User details not found.'})

        # ✅ If Django authentication fails, try manual authentication
        try:
            user_detail = Userdetail.objects.get(username=username)

            if user_detail.userpassword == password:
                django_user, created = User.objects.get_or_create(username=user_detail.username)
                django_user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, django_user)

                # ✅ Store user details in session
                request.session['user_id'] = user_detail.userid
                request.session['username'] = user_detail.username
                request.session['user_role'] = user_detail.usergroupid.usergroupname
                request.session.modified = True
                request.session.save()

                print(f"Session after login: {dict(request.session)}")  # ✅ Debugging Step 4
                
                # ✅ Redirect to `next` if available
                if next_url:
                    return redirect(next_url)

                return redirect_based_on_role(user_detail)

            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid password.'})

        except Userdetail.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'User not found.'})

    return render(request, 'accounts/login.html', {'next': request.GET.get('next', '')})


# Redirect based on role
def redirect_based_on_role(user_detail):
    role = user_detail.usergroupid.usergroupname
    print(f"Redirecting {user_detail.username} to {role} dashboard")

    if role == "Admin":
        return redirect('admin_dashboard')
    elif role == "Trainer":
        return redirect('trainer_dashboard')
    elif role == "Student":
        return redirect('student_dashboard')
    elif role == "Staff":
        return redirect('staff_dashboard')
    else:
        return redirect('unauthorized_page')  # Fallback for unknown roles


# User Dashboard (Profile Update)
# @login_required
def dashboard(request):
    user = Userdetail.objects.get(userid=request.user.id)
    # usergroup_name = user.usergroupid.usergroupname
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileUpdateForm(instance=user)
    return render(request, 'accounts/dashboard.html', {'form': form, 'usergroup': user.usergroupid.usergroupname})

# Logout User
def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@role_required("Admin")
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')


@login_required(login_url='login')
@role_required("Trainer")
def trainer_dashboard(request):
    return render(request, 'accounts/trainer_dashboard.html')


@login_required(login_url='login')
@role_required("Staff")
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')


@login_required(login_url='login')
@role_required("Student")
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')

def no_permission(request):
    return render(request, 'accounts/no_permission.html')

def unauthorized_page(request):
    print(f"Session in unauthorized page: {dict(request.session)}")
    return render(request, "accounts/unauthorized.html", {"message": "Access Denied! You are not authorized to view this page."})





# # User Management Views

@login_required(login_url='login')
@role_required(["Admin", "Staff"])
def user_list(request):
    users = Userdetail.objects.select_related('usergroupid').all()  # Fetch all users with related user group
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required(login_url='login')
@role_required(["Admin", "Staff"])
def user_detail(request, user_id):
    user = get_object_or_404(Userdetail, userid=user_id)
    return render(request, 'accounts/user_detail.html', {'user': user})






# # Course Management Views
@login_required
@role_required(["Admin", "Staff"])
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'accounts/course_list.html', {'courses': courses})


@login_required
@role_required(["Admin", "Staff"])
def course_create(request):
    if request.method == 'POST':
        name = request.POST.get('coursename')
        description = request.POST.get('coursedescription')
        created_by = Userdetail.objects.get(username=request.user.username) # Assuming you have a Userdetail model with a username field
        print(f"Created by: {created_by}")# Print the created_by value for debugging purposes
        if not created_by:
            messages.error(request, 'User not found. Please check your credentials.')
            return redirect('course_create')
        
        course = Course(
            coursename=name,
            coursedescription=description,
            createdby=created_by
        )
        course.save()
        messages.success(request, 'Course created successfully!')
        return redirect('course_list')
    
    return render(request, 'accounts/course_create.html')

@login_required
@role_required(["Admin", "Staff"])
def course_update(request, course_id):
    course = get_object_or_404(Course, courseid=course_id)
    
    if request.method == 'POST':
        course.coursename = request.POST.get('coursename')
        course.coursedescription = request.POST.get('coursedescription')
        course.updatedby = Userdetail.objects.get(username=request.user.username) # Assuming you have a Userdetail model with a username field
        course.save()
        messages.success(request, 'Course updated successfully!')
        return redirect('course_list')
    
    return render(request, 'accounts/course_update.html', {'course': course})

@login_required
@role_required(["Admin", "Staff"])
def course_delete(request, course_id):
    course = get_object_or_404(Course, courseid=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully!')
    return redirect('course_list')

@login_required
@role_required(["Admin", "Staff"])
def course_access_manage(request, course_id):
    course = get_object_or_404(Course, courseid=course_id)
    user_groups = Usergroupdetail.objects.all()

    if request.method == 'POST':
        access_updates = []
        
        for group in user_groups:
            can_view = request.POST.get(f'can_view_{group.usergroupid}') == 'on'
            can_edit = request.POST.get(f'can_edit_{group.usergroupid}') == 'on'
            can_delete = request.POST.get(f'can_delete_{group.usergroupid}') == 'on'
            
            access, created = CourseAccess.objects.get_or_create(course=course, usergroup=group)
            
            # Only update if values have changed
            if access.can_view != can_view or access.can_edit != can_edit or access.can_delete != can_delete:
                access.can_view = can_view
                access.can_edit = can_edit
                access.can_delete = can_delete
                access_updates.append(access)
        
        # Bulk update for efficiency
        if access_updates:
            CourseAccess.objects.bulk_update(access_updates, ['can_view', 'can_edit', 'can_delete'])

        messages.success(request, 'Course access updated successfully!')
        return redirect('course_list')

    # Fetch current access permissions in a dictionary format
    current_access = {
        access.usergroup.usergroupid: {
            "can_view": access.can_view,
            "can_edit": access.can_edit,
            "can_delete": access.can_delete
        }
        for access in course.courseaccess_set.all()
    }

    return render(request, 'accounts/course_access_manage.html', {
        'course': course,
        'user_groups': user_groups,
        'current_access': current_access
    })

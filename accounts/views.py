
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileUpdateForm
from .models import Userdetail,Usergroupdetail
from django.contrib.auth.models import User
from .decorators import admin_required,role_required
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
# @admin_required
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


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        print(f"Trying to authenticate: {username}")  # Debugging Step 1

        # ✅ First, check if it's a Django superuser
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"Authenticated successfully: {user}")  # Debugging Step 2
            login(request, user)  # ✅ Django login works here

            # ✅ Check if this user is in Userdetail
            try:
                user_detail = Userdetail.objects.get(username=username)  # `username` instead of `userid`
                print(f"User Detail Found: {user_detail}")  # Debugging Step 3
                
                # ✅ Store user details in session
                request.session['user_id'] = user_detail.userid
                request.session['username'] = user_detail.username
                request.session['user_role'] = user_detail.usergroupid.usergroupname  # Ensure role is stored!
                
                print(f"Session after login: {dict(request.session)}")  # ✅ Print full session

                # Redirect based on role
                return redirect_based_on_role(user_detail)

            except Userdetail.DoesNotExist:
                print("User details not found.")
                return render(request, 'accounts/login.html', {'error': 'User details not found.'})

        # ✅ If `authenticate()` failed, check if user exists in Userdetail (Custom Users)
        try:
            user_detail = Userdetail.objects.get(username=username)

            # ✅ Manually verify password (assuming plaintext password)
            if user_detail.userpassword == password:
                print(f"Manual authentication successful for: {username}")

                # ✅ Manually create a Django user for session login
                django_user, created = User.objects.get_or_create(username=user_detail.username)
                django_user.backend = 'django.contrib.auth.backends.ModelBackend'  # Required for login()
                login(request, django_user)  # ✅ Force login Django session

                # ✅ Store Userdetail data in session
                request.session['user_id'] = user_detail.userid
                request.session['username'] = user_detail.username
                request.session['user_role'] = user_detail.usergroupid.usergroupname
                
                # Verify session data
                print(f"Session after login: {dict(request.session)}")

                # ✅ Redirect based on role
                return redirect_based_on_role(user_detail)

            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid password.'})

        except Userdetail.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'User not found.'})

    return render(request, 'accounts/login.html')


# ✅ Helper function to handle role-based redirection
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
    
    # user_detail = Userdetail.objects.get(userid=request.user.id)
    
    # if user_detail.usergroupid.usergroupname != "Admin":
    #     return redirect('no_permission')  # Redirect if not a Admin
    
    return render(request, 'accounts/admin_dashboard.html')


@login_required(login_url='login')
@role_required("Trainer")
def trainer_dashboard(request):
    
    # user_detail = Userdetail.objects.get(userid=request.user.id)
    
    # if user_detail.usergroupid.usergroupname != "Trainer":
    #     return redirect('no_permission')  # Redirect if not a Trainer
    
    return render(request, 'accounts/trainer_dashboard.html')


@login_required(login_url='login')
@role_required("Staff")
def staff_dashboard(request):
    
    # user_detail = Userdetail.objects.get(userid=request.user.id)
    
    # if user_detail.usergroupid.usergroupname != "Staff":
    #     return redirect('no_permission')  # Redirect if not a Staff
    
    return render(request, 'accounts/staff_dashboard.html')


@login_required(login_url='login')
@role_required("Student")
def student_dashboard(request):
    
    # user_detail = Userdetail.objects.get(userid=request.user.id)
    
    # if user_detail.usergroupid.usergroupname != "Student":
    #     return redirect('no_permission')  # Redirect if not a Student
    
    return render(request, 'accounts/student_dashboard.html')


def no_permission(request):
    return render(request, 'accounts/no_permission.html')

def unauthorized_page(request):
    print(f"Session in unauthorized page: {dict(request.session)}")
    return render(request, "accounts/unauthorized.html", {"message": "Access Denied! You are not authorized to view this page."})

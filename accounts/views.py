
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileUpdateForm
from .models import Userdetail
from django.contrib.auth.models import User
from .decorators import admin_required,role_required

# Admin creates a new user



def Home(request):
    
    return render(request,"accounts/base.html")




# @login_required()
# @admin_required
def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect admin after user creation
    else:
        form = UserRegistrationForm() 
    return render(request, 'accounts/register.html', {'form': form})


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
    else:
        return redirect('staff_dashboard')  # Fallback for unknown roles
"""
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        print(f"Trying to authenticate: {username}")  # Debugging Step 1

        # First, check if it's a Django superuser
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"Authenticated successfully: {user}")  # Debugging Step 2
            login(request, user)  # Log in the user
            
            # Check if this user is in Userdetail
            try:
                user_detail = Userdetail.objects.get(userid=user.id) 
                print(f"User Detail Found: {user_detail}")  # Debugging Step 3
                
                # Redirect based on role
                if user_detail.usergroupid.usergroupname == "Admin":
                    return redirect('admin_dashboard')
                elif user_detail.usergroupid.usergroupname == "Trainer":
                    return redirect('trainer_dashboard')
                elif user_detail.usergroupid.usergroupname == "Student":
                    return redirect('student_dashboard')
                else:
                    return redirect('staff_dashboard')  # Fallback in case of an unknown role

            except Userdetail.DoesNotExist:
                print("User details not found.")
                return render(request, 'accounts/login.html', {'error': 'User details not found.'})

        # If `authenticate()` failed, check if the user exists in Userdetail
        try:
            user_detail = Userdetail.objects.get(username=username)

            # Manually verify password
            if user_detail.userpassword == password:  # Assuming userpassword stores plain text
                print(f"Manual authentication successful for: {username}")

                # Create a Django session manually
                request.session['user_id'] = user_detail.userid
                request.session['username'] = user_detail.username

                # Redirect based on role
                if user_detail.usergroupid.usergroupname == "Admin":
                    return redirect('admin_dashboard')
                elif user_detail.usergroupid.usergroupname == "Trainer":
                    return redirect('trainer_dashboard')
                elif user_detail.usergroupid.usergroupname == "Student":
                    return redirect('student_dashboard')
                else:
                    return redirect('staff_dashboard')  # Fallback in case of an unknown role

            else:
                return render(request, 'accounts/login.html', {'error': 'Invalid password.'})

        except Userdetail.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'User not found.'})

    return render(request, 'accounts/login.html')
 
""" 

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
    logout(request)
    # request.session.flush() # Clear session data
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
    return render(request, "accounts/unauthorized.html", {"message": "Access Denied! You are not authorized to view this page."})

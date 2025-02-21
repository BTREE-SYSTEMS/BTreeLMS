from django.shortcuts import redirect
from functools import wraps
from .models import Userdetail

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            user_detail = Userdetail.objects.get(userid=request.user.id)
            if user_detail.usergroupid.usergroupname != "Admin":
                return redirect('no_permission')  # Redirect to a "No Permission" page
        except Userdetail.DoesNotExist:
            return redirect('no_permission')  # Redirect if user details are missing
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def role_required(*required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Get user role from session
            print(f"Session in decorator: {dict(request.session)}")
            user_role = request.session.get('user_role')
            
            print(f"Session in decorator: {dict(request.session)}")  # Debugging session

            if user_role not in required_role:
                print(f"Unauthorized access blocked! {user_role} tried to access {required_role} page.")
                return redirect('unauthorized_page')  # Redirect if role doesn't match

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
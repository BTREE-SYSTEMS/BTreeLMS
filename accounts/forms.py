# from django import forms

# class UserDetailForm(forms.Form):
#     UserName = forms.CharField(max_length=100)
#     UserEmail = forms.EmailField(max_length=100)
#     UserContactNumber = forms.CharField(max_length=50)
#     UserPassword = forms.CharField(max_length=50, widget=forms.PasswordInput)
#     UserGroupId = forms.IntegerField()
#     IsActive = forms.BooleanField(required=False, initial=True)
#     CreatedBy = forms.IntegerField()

#     # Optional Fields
#     UserGender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
#     UserDOB = forms.DateTimeField(required=False)
#     UserResumeName = forms.CharField(max_length=100, required=False)
#     UserResumeData = forms.FileField(required=False)
#     UserAadhaarNumber = forms.IntegerField(required=False)
#     UserPanNumber = forms.CharField(max_length=100, required=False)
#     CurrentOTP = forms.IntegerField(required=False)
#     IsCurrentOTPExpired = forms.BooleanField(required=False)
#     UserImageFileName = forms.CharField(max_length=50, required=False)

#     PresentAddress = forms.CharField(max_length=500, required=False)
#     PresentVillage = forms.CharField(max_length=100, required=False)
#     PresentCity = forms.CharField(max_length=100, required=False)
#     PresentDistrict = forms.CharField(max_length=100, required=False)
#     PresentState = forms.CharField(max_length=100, required=False)

#     NativeAddress = forms.CharField(max_length=500, required=False)
#     NativeVillage = forms.CharField(max_length=100, required=False)
#     NativeCity = forms.CharField(max_length=100, required=False)
#     NativeDistrict = forms.CharField(max_length=100, required=False)
#     NativeState = forms.CharField(max_length=100, required=False)

#     EducationDegreeName = forms.CharField(max_length=100, required=False)
#     EducationInstitutionName = forms.CharField(max_length=200, required=False)
#     EducationUniversityName = forms.CharField(max_length=200, required=False)
#     EducationStartYear = forms.IntegerField(required=False)
#     EducationEndYear = forms.IntegerField(required=False)
#     EducationPercentageOrCGPA = forms.DecimalField(max_digits=5, decimal_places=2, required=False)

#     ProfessionalJobTitle = forms.CharField(max_length=100, required=False)
#     ProfessionalCompanyName = forms.CharField(max_length=200, required=False)
#     ProfessionalStartDate = forms.DateField(required=False)
#     ProfessionalEndDate = forms.DateField(required=False)
#     ProfessionalCurrentCTC = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

#     ReferralPersonName = forms.CharField(max_length=100, required=False)
#     ReferralPersonEmail = forms.EmailField(max_length=100, required=False)
#     ReferralPersonPhone = forms.CharField(max_length=15, required=False)


# ----------------------------


from django import forms
from .models import Userdetail

# User Registration Form
class UserRegistrationForm(forms.ModelForm):
    userpassword = forms.CharField(widget=forms.PasswordInput)  # Hide password input

    class Meta:
        model = Userdetail
        fields = ['username', 'useremail', 'userpassword', 'usergroupid', 'usergender','usercontactnumber']

# User Profile Update Form
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Userdetail
        fields = ['userdob', 'userresumename', 'userresumedata', 'useraadhaarnumber', 'userpannumber']

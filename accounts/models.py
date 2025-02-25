# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addressdetail(models.Model):
    addressid = models.AutoField(db_column='AddressId', primary_key=True)  # Field name made lowercase.
    presentaddress = models.CharField(db_column='PresentAddress', unique=True, max_length=500, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    presentvillage = models.CharField(db_column='PresentVillage', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    presentcity = models.CharField(db_column='PresentCity', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    presentdistrict = models.CharField(db_column='PresentDistrict', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    presentstate = models.CharField(db_column='PresentState', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    nativeaddress = models.CharField(db_column='NativeAddress', unique=True, max_length=500, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    nativevillage = models.CharField(db_column='NativeVillage', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    nativecity = models.CharField(db_column='NativeCity', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    nativedistrict = models.CharField(db_column='NativeDistrict', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    nativestate = models.CharField(db_column='NativeState', max_length=100, db_collation='utf8mb3_general_ci', null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'addressdetail'


class Combinedbackup(models.Model):
    action_type = models.CharField(max_length=10, blank=True, null=True)
    user_id = models.ForeignKey('Userdetail', on_delete=models.CASCADE, db_column='UserId')
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)
    user_contact_number = models.CharField(max_length=50, blank=True, null=True)
    user_password = models.CharField(max_length=50, blank=True, null=True)
    user_group_id = models.IntegerField(blank=True, null=True)
    user_gender = models.CharField(max_length=1, blank=True, null=True)
    user_dob = models.DateTimeField(blank=True, null=True)
    user_resume_name = models.CharField(max_length=100, blank=True, null=True)
    user_aadhaar_number = models.BigIntegerField(blank=True, null=True)
    user_pan_number = models.CharField(max_length=100, blank=True, null=True)
    current_otp = models.BigIntegerField(blank=True, null=True)
    is_current_otp_expired = models.IntegerField(blank=True, null=True)
    user_image_file_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    present_address = models.CharField(max_length=500, db_collation='utf8mb3_general_ci', blank=True, null=True)
    present_village = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    present_city = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    present_district = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    present_state = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    native_address = models.CharField(max_length=500, db_collation='utf8mb3_general_ci', blank=True, null=True)
    native_village = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    native_city = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    native_district = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    native_state = models.CharField(max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    degree_name = models.CharField(max_length=100, blank=True, null=True)
    institution_name = models.CharField(max_length=200, blank=True, null=True)
    university_name = models.CharField(max_length=200, blank=True, null=True)
    start_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    end_year = models.TextField(blank=True, null=True)  # This field type is a guess.
    percentage_or_cgpa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    current_ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    referral_person_name = models.CharField(max_length=100, blank=True, null=True)
    referral_person_email = models.CharField(max_length=100, blank=True, null=True)
    referral_person_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'combinedbackup'


class Educationdetail(models.Model):
    educationid = models.AutoField(db_column='EducationId', primary_key=True)  # Field name made lowercase.
    degreename = models.CharField(db_column='DegreeName', max_length=100,null=True)  # Field name made lowercase.
    institutionname = models.CharField(db_column='InstitutionName', max_length=200,null=True)  # Field name made lowercase.
    universityname = models.CharField(db_column='UniversityName', max_length=200,null=True)  # Field name made lowercase.
    startyear = models.TextField(db_column='StartYear',null=True)  # Field name made lowercase. This field type is a guess.
    endyear = models.TextField(db_column='EndYear',null=True)  # Field name made lowercase. This field type is a guess.
    percentageorcgpa = models.DecimalField(db_column='PercentageOrCGPA', max_digits=5, decimal_places=2,null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userdetail', on_delete=models.CASCADE, db_column='UserId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'educationdetail'


class Professionaldetail(models.Model):
    professionalid = models.AutoField(db_column='ProfessionalId', primary_key=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=100,null=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=200,null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate',null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate',null=True)  # Field name made lowercase.
    currentctc = models.DecimalField(db_column='CurrentCTC', max_digits=10, decimal_places=2,null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userdetail', on_delete=models.CASCADE, db_column='UserId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'professionaldetail'


class Referrals(models.Model):
    referralid = models.AutoField(db_column='ReferralId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userdetail', on_delete=models.CASCADE, db_column='UserId')  # Field name made lowercase.
    referralpersonname = models.CharField(db_column='ReferralPersonName', max_length=100,null=True)  # Field name made lowercase.
    referralpersonemail = models.CharField(db_column='ReferralPersonEmail', unique=True, max_length=100,null=True)  # Field name made lowercase.
    referralpersonphone = models.CharField(db_column='ReferralPersonPhone', max_length=15,null=True)  # Field name made lowercase.
    referraldate = models.DateTimeField(db_column='ReferralDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'referrals'


class Userdetail(models.Model):
    userid = models.AutoField(db_column='UserId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=100)  # Field name made lowercase.
    useremail = models.CharField(db_column='UserEmail', unique=True, max_length=100)  # Field name made lowercase.
    usercontactnumber = models.CharField(db_column='UserContactNumber', unique=True, max_length=50)  # Field name made lowercase.
    userpassword = models.CharField(db_column='UserPassword', unique=True, max_length=50)  # Field name made lowercase.
    usergroupid = models.ForeignKey('Usergroupdetail', on_delete=models.CASCADE, db_column='UserGroupId')  # Field name made lowercase.
    usergender = models.CharField(db_column='UserGender', max_length=1)  # Field name made lowercase.
    userdob = models.DateTimeField(db_column='UserDOB',null=True,blank=True)  # Field name made lowercase.
    userresumename = models.CharField(db_column='UserResumeName', max_length=100,null=True,blank=True)  # Field name made lowercase.
    userresumedata = models.TextField(db_column='UserResumeData', blank=True, null=True)  # Field name made lowercase.
    useraadhaarnumber = models.BigIntegerField(db_column='UserAadhaarNumber', unique=True, null=True,blank=True)  # Field name made lowercase.
    userpannumber = models.CharField(db_column='UserPanNumber', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    currentotp = models.BigIntegerField(db_column='CurrentOTP', unique=True,null=True)  # Field name made lowercase.
    iscurrentotpexpired = models.IntegerField(db_column='IsCurrentOTPExpired',null=True)  # Field name made lowercase.
    userimagefilename = models.CharField(db_column='UserImageFileName', unique=True, max_length=50,null=True,blank=True)  # Field name made lowercase.
    isactive = models.IntegerField(db_column='IsActive',null=True)  # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate',auto_now_add=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='UpdatedBy', blank=True, null=True)  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'userdetail'


class Usergroupdetail(models.Model):
    usergroupid = models.AutoField(db_column='UserGroupId', primary_key=True)  # Field name made lowercase.
    usergroupname = models.CharField(db_column='UserGroupName', unique=True, max_length=100)  # Field name made lowercase.
    usergroupdescription = models.CharField(db_column='UserGroupDescription', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    isactive = models.TextField(db_column='IsActive', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    createdby = models.IntegerField(db_column='CreatedBy')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate',auto_now_add=True)  # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'usergroupdetail'

    def __str__(self):
        return self.usergroupname  # This helps in displaying the name instead of ID

class Course(models.Model):
    courseid = models.AutoField(db_column='CourseId', primary_key=True)
    coursename = models.CharField(db_column='CourseName', max_length=200)
    coursedescription = models.TextField(db_column='CourseDescription', blank=True, null=True)
    createdby = models.ForeignKey(Userdetail, on_delete=models.CASCADE, db_column='CreatedBy', related_name='created_courses')
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    updatedby = models.ForeignKey(Userdetail, on_delete=models.CASCADE, db_column='UpdatedBy', blank=True, null=True, related_name='updated_courses')
    updateddate = models.DateTimeField(db_column='UpdatedDate', blank=True, null=True, auto_now=True)
    isactive = models.BooleanField(db_column='IsActive', default=True)
    allowed_groups = models.ManyToManyField(Usergroupdetail, through='CourseAccess')

    class Meta:
        db_table = 'course'


class CourseAccess(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    usergroup = models.ForeignKey(Usergroupdetail, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'course_access'
        unique_together = ('course', 'usergroup')    
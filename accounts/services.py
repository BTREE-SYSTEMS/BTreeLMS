# from django.db import connection

# def insert_user_details(data):
#     # Ensure mandatory fields are provided
#     required_fields = ["UserName", "UserEmail", "UserContactNumber", "UserPassword", "UserGroupId", "IsActive", "CreatedBy"]
    
#     for field in required_fields:
#         if field not in data or data[field] in [None, ""]:
#             raise ValueError(f"{field} is required")

#     # Optional fields - insert None if not provided
#     optional_fields = [
#         "UserGender", "UserDOB", "UserResumeName", "UserResumeData", "UserAadhaarNumber", "UserPanNumber",
#         "CurrentOTP", "IsCurrentOTPExpired", "UserImageFileName", "PresentAddress", "PresentVillage",
#         "PresentCity", "PresentDistrict", "PresentState", "NativeAddress", "NativeVillage", "NativeCity",
#         "NativeDistrict", "NativeState", "EducationDegreeName", "EducationInstitutionName",
#         "EducationUniversityName", "EducationStartYear", "EducationEndYear", "EducationPercentageOrCGPA",
#         "ProfessionalJobTitle", "ProfessionalCompanyName", "ProfessionalStartDate", "ProfessionalEndDate",
#         "ProfessionalCurrentCTC", "ReferralPersonName", "ReferralPersonEmail", "ReferralPersonPhone"
#     ]

#     # Assign None to missing optional fields
#     for field in optional_fields:
#         data[field] = data.get(field, None)

#     # Read resume data as binary if provided
#     resume_data = data["UserResumeData"].read() if data["UserResumeData"] else None

#     with connection.cursor() as cursor:
#         cursor.callproc("InsertUserDetails", [
#             data["UserName"], data["UserEmail"], data["UserContactNumber"], data["UserPassword"],
#             data["UserGroupId"], data["UserGender"], data["UserDOB"], data["UserResumeName"],
#             resume_data, data["UserAadhaarNumber"], data["UserPanNumber"], data["CurrentOTP"],
#             data["IsCurrentOTPExpired"], data["UserImageFileName"], data["IsActive"], data["CreatedBy"],
#             data["PresentAddress"], data["PresentVillage"], data["PresentCity"], data["PresentDistrict"],
#             data["PresentState"], data["NativeAddress"], data["NativeVillage"], data["NativeCity"],
#             data["NativeDistrict"], data["NativeState"], data["EducationDegreeName"],
#             data["EducationInstitutionName"], data["EducationUniversityName"], data["EducationStartYear"],
#             data["EducationEndYear"], data["EducationPercentageOrCGPA"], data["ProfessionalJobTitle"],
#             data["ProfessionalCompanyName"], data["ProfessionalStartDate"], data["ProfessionalEndDate"],
#             data["ProfessionalCurrentCTC"], data["ReferralPersonName"], data["ReferralPersonEmail"],
#             data["ReferralPersonPhone"]
#         ])




# from django.db import connection

# def insert_user_details(
#     UserName, UserEmail, UserContactNumber, UserPassword, UserGroupId, IsActive, CreatedBy,
#     UserGender=None, UserDOB=None, UserResumeName=None, UserResumeData=None,
#     UserAadhaarNumber=None, UserPanNumber=None, CurrentOTP=None, IsCurrentOTPExpired=None,
#     UserImageFileName=None, PresentAddress=None, PresentVillage=None, PresentCity=None,
#     PresentDistrict=None, PresentState=None, NativeAddress=None, NativeVillage=None,
#     NativeCity=None, NativeDistrict=None, NativeState=None, EducationDegreeName=None,
#     EducationInstitutionName=None, EducationUniversityName=None, EducationStartYear=None,
#     EducationEndYear=None, EducationPercentageOrCGPA=None, ProfessionalJobTitle=None,
#     ProfessionalCompanyName=None, ProfessionalStartDate=None, ProfessionalEndDate=None,
#     ProfessionalCurrentCTC=None, ReferralPersonName=None, ReferralPersonEmail=None,
#     ReferralPersonPhone=None
# ):
#     try:
#         with connection.cursor() as cursor:
#             cursor.callproc('InsertUserDetails', [
#                 UserName, UserEmail, UserContactNumber, UserPassword, UserGroupId,
#                 UserGender, UserDOB, UserResumeName, UserResumeData, UserAadhaarNumber,
#                 UserPanNumber, CurrentOTP, IsCurrentOTPExpired, UserImageFileName, IsActive,
#                 CreatedBy, PresentAddress, PresentVillage, PresentCity, PresentDistrict,
#                 PresentState, NativeAddress, NativeVillage, NativeCity, NativeDistrict,
#                 NativeState, EducationDegreeName, EducationInstitutionName,
#                 EducationUniversityName, EducationStartYear, EducationEndYear,
#                 EducationPercentageOrCGPA, ProfessionalJobTitle, ProfessionalCompanyName,
#                 ProfessionalStartDate, ProfessionalEndDate, ProfessionalCurrentCTC,
#                 ReferralPersonName, ReferralPersonEmail, ReferralPersonPhone
#             ])
#         return {"status": "success", "message": "User details inserted successfully"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


# --------------------------------------------------- 

from django.db import connection

def insert_user_details(data):
    """ Calls MySQL stored procedure to insert user details """
    try:
        with connection.cursor() as cursor:
            cursor.callproc('InsertUserDetails', [
                data.get('UserName'),
                data.get('UserEmail'),
                data.get('UserContactNumber'),
                data.get('UserPassword'),
                int(data.get('UserGroupId', 0) or 0),  # Ensures integer input
                data.get('UserGender', None),
                data.get('UserDOB', None),
                data.get('UserResumeName', None),
                data.get('UserResumeData').read() if data.get('UserResumeData') else None,
                data.get('UserAadhaarNumber', None),
                data.get('UserPanNumber', None),
                data.get('CurrentOTP', None),
                data.get('IsCurrentOTPExpired', None),
                data.get('UserImageFileName', None),
                int(data.get('IsActive', 0) or 0),  # Ensures integer input
                int(data.get('CreatedBy', 0) or 0),  # Ensures integer input
                data.get('PresentAddress', None),
                data.get('PresentVillage', None),
                data.get('PresentCity', None),
                data.get('PresentDistrict', None),
                data.get('PresentState', None),
                data.get('NativeAddress', None),
                data.get('NativeVillage', None),
                data.get('NativeCity', None),
                data.get('NativeDistrict', None),
                data.get('NativeState', None),
                data.get('EducationDegreeName', None),
                data.get('EducationInstitutionName', None),
                data.get('EducationUniversityName', None),
                int(data.get('EducationStartYear')) if data.get('EducationStartYear') else None,
                int(data.get('EducationEndYear')) if data.get('EducationEndYear') else None,
                data.get('EducationPercentageOrCGPA', None),
                data.get('ProfessionalJobTitle', None),
                data.get('ProfessionalCompanyName', None),
                data.get('ProfessionalStartDate', None),
                data.get('ProfessionalEndDate', None),
                data.get('ProfessionalCurrentCTC', None),
                data.get('ReferralPersonName', None),
                data.get('ReferralPersonEmail', None),
                data.get('ReferralPersonPhone', None)
            ])
        
        return {"status": "success", "message": "User details inserted successfully"}

    except Exception as e:
        print(f"InsertUserDetails Error: {e}")  # Logs the exact error
        return {"status": "error", "message": str(e)}

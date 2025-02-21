import requests
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
from msal import ConfidentialClientApplication
from django.http import JsonResponse

# Initialize MSAL client
msal_client = ConfidentialClientApplication(
    client_id=settings.MS_GRAPH_CLIENT_ID,
    authority=settings.MS_GRAPH_AUTHORITY,
    client_credential=settings.MS_GRAPH_CLIENT_SECRET,
)

# Microsoft Login View
def microsoft_login(request):
    # Generate the authorization URL
    auth_url = msal_client.get_authorization_request_url(
        scopes=settings.MS_GRAPH_SCOPES,
        redirect_uri=settings.MS_GRAPH_REDIRECT_URI,
    )
    return redirect(auth_url)

# Callback View
def auth_callback(request):
    code = request.GET.get("code")
    if not code:
        return render(request, "error.html", {"message": "Authorization failed!"})

    # Exchange the authorization code for an access token
    result = msal_client.acquire_token_by_authorization_code(
        code=code,
        scopes=settings.MS_GRAPH_SCOPES,
        redirect_uri=settings.MS_GRAPH_REDIRECT_URI,
    )

    if "access_token" not in result:
        return render(request, "error.html", {"message": "Failed to obtain access token!"})

    # Save the access token and refresh token in the session
    request.session["access_token"] = result["access_token"]
    request.session["refresh_token"] = result["refresh_token"]
    request.session["token_expiry_time"] = datetime.utcnow().isoformat()
    return redirect("create_meeting")  # Redirect to the meeting creation page

# Function to refresh the access token using the refresh token
def refresh_access_token(request):
    refresh_token = request.session.get("refresh_token")
    if not refresh_token:
        return None

    try:
        result = msal_client.acquire_token_by_refresh_token(
            refresh_token=refresh_token,
            scopes=settings.MS_GRAPH_SCOPES,
        )

        if "access_token" not in result:
            return None

        # Update the session with the new access token and refresh token
        request.session["access_token"] = result["access_token"]
        request.session["refresh_token"] = result.get("refresh_token", refresh_token)
        request.session["token_expiry_time"] = datetime.utcnow().isoformat()
        return result["access_token"]

    except Exception as e:
        print(f"Error refreshing access token: {e}")
        return None

# Meeting Creation View
def create_meeting(request):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("microsoft_login")  # Redirect to login if no token is available

    if is_token_expired(request.session.get("token_expiry_time")):
        access_token = refresh_access_token(request)
        if not access_token:
            return redirect("microsoft_login")  # Redirect to login if token refresh failed

    if request.method == "POST":
        subject = request.POST.get("subject")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        if not subject or not start_time or not end_time:
            return render(request, "error.html", {"message": "Missing required fields!"})

        # Convert from "YYYY-MM-DDTHH:MM" format to ISO 8601
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M").isoformat() + "+05:30"
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M").isoformat() + "+05:30"

        # Meeting data
        meeting_data = {
            "subject": subject,
            "startDateTime": start_time,
            "endDateTime": end_time,
        }

        # Create the meeting using Graph API
        response = requests.post(
            url="https://graph.microsoft.com/v1.0/me/onlineMeetings",
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
            json=meeting_data,
        )

        if response.status_code == 201:
            meeting_info = response.json()
            return render(request, "meeting_created.html", {"meeting_info": meeting_info})
        else:
            return render(request, "error.html", {"message": response.json()})

    return render(request, "create_meeting.html")


def is_token_expired(token_expiry_time):
    if token_expiry_time is None:
        return True
    return datetime.utcnow() > datetime.fromisoformat(token_expiry_time)

# Get Meeting Recordings (Search OneDrive for "Meeting" MP4 files)
def get_meeting_recordings(request):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("microsoft_login")

    if is_token_expired(request.session.get("token_expiry_time")):
        access_token = refresh_access_token(request)
        if not access_token:
            return redirect("microsoft_login")

    # Search OneDrive for meeting recordings
    url = "https://graph.microsoft.com/v1.0/me/drive/root/search(q='Meeting')"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return render(request, "error.html", {"message": response.json()})

    data = response.json()
    recordings = [
        {"name": item["name"], "url": item["webUrl"]}
        for item in data.get("value", []) if item["name"].endswith(".mp4")
    ]

    return render(request, "recordings.html", {"recordings": recordings})

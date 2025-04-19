from django.shortcuts import render
from .models import CalendlyEvent
from django.http import JsonResponse
import requests

# Create your views here.
def book_meeting(request):
    if request.method == 'POST':
        url = "https://api.calendly.com/v2/users/me"
        headers={
            "Authorization": "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzQ1MDQ0NTE4LCJqdGkiOiJhYmJiYTU5ZS1kNjhhLTRmOGEtYTNkYS1mYTYxMTY5ODQzYzUiLCJ1c2VyX3V1aWQiOiJkMzVkNTgwNS02NDg4LTRmYTYtYWU0OC1mNjc2NGMyNGI1MzIifQ.OMVDYrYiy3eOj4dz0I6E7HBvv6RY__bW5Hr_gPorWM0mnnym46J_dO2N4mU1azcg7lPLhqejOwIromEhwyC9eA"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()["resource"]
            email = user_data["email"]
            name = user_data.get("slug","NoName")
            calendly_uri = user_data["uri"]

            CalendlyEvent.objects.create(
                email=email,
                name=name,
                calendly_uri=calendly_uri
            )
            return render(request, "bookmeeting.html", {'message': "User info saved successfully!"})
        else:
            return render(request,"bookmeeting.html", {'error': "Failed to fetch user data from Calendly."})
    return render(request, 'bookmeeting.html')

def fetch_events(request):
    token = "Bearer eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzQ1MDQ0NTE4LCJqdGkiOiJhYmJiYTU5ZS1kNjhhLTRmOGEtYTNkYS1mYTYxMTY5ODQzYzUiLCJ1c2VyX3V1aWQiOiJkMzVkNTgwNS02NDg4LTRmYTYtYWU0OC1mNjc2NGMyNGI1MzIifQ.OMVDYrYiy3eOj4dz0I6E7HBvv6RY__bW5Hr_gPorWM0mnnym46J_dO2N4mU1azcg7lPLhqejOwIromEhwyC9eA"

    user_resp = requests.get(
        "https://api.calendly.com/v2/users/me",
        headers={"Authorization": token}
    )
    
    if user_resp.status_code != 200:
        return JsonResponse({"error": "Failed to fetch user data"}, status=500)
    
    user_uri = user_resp.json()["resource"]["uri"]
    
    events_resp = requests.get(
        f"https://api.calendly.com/v2/users/{user_uri}/scheduled_events",
        headers={"Authorization": token}
    )
    
    if events_resp.status_code != 200:
        return JsonResponse({"error": "Failed to fetch events"}, status=500)
    
    events = events_resp.json()["collection"]
    all_data =[]

    for event in events:
        event_uri = event["uri"]
        invitee_url = event_uri + "/invitees"

        invitee_resp = requests.get(invitee_url,headers={"Authorization": token})
        
        if invitee_resp.status_code == 200:
            invitees = invitee_resp.json()["collection"]
            for invitee in invitees:
                event_name = event["name"]
                event_start_time = event["start_time"]
                invitee_email = invitee["email"]
                invitee_name = invitee["name"]

                # Save to database
                CalendlyEvent.objects.get_or_create(
                    event_name=event_name,
                    event_start_time=event_start_time,
                    invitee_email=invitee_email,
                    invitee_name=invitee_name
                )

                all_data.append({
                    "event_name": event["name"],
                    "event_start_time": event["start_time"],
                    "invitee_email": invitee["email"],
                    "invitee_name": invitee["name"]
                })
    return JsonResponse({"data": "all_data"})
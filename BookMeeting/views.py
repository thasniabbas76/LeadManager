from django.shortcuts import render
from .models import CalendlyEvent
from django.http import JsonResponse
import requests
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
access_token = "Bearer eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzQ1MDQ0NTE4LCJqdGkiOiJhYmJiYTU5ZS1kNjhhLTRmOGEtYTNkYS1mYTYxMTY5ODQzYzUiLCJ1c2VyX3V1aWQiOiJkMzVkNTgwNS02NDg4LTRmYTYtYWU0OC1mNjc2NGMyNGI1MzIifQ.OMVDYrYiy3eOj4dz0I6E7HBvv6RY__bW5Hr_gPorWM0mnnym46J_dO2N4mU1azcg7lPLhqejOwIromEhwyC9eA"

def book_meeting(request):
    if request.method == 'POST':
        url = "https://api.calendly.com/users/me"
        headers={
            "Authorization": access_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()["resource"]
            email = user_data["email"]
            name = user_data.get("slug","NoName")
            calendly_uri = user_data["uri"]

            CalendlyEvent.objects.create(
                invitee_email=email,
                invitee_name=name,
                event_start_time=timezone.now(),
                calendly_uri = calendly_uri,
            )

            
            return render(request, "bookmeeting.html", {'message': "User info saved successfully!"})
        
        else:
            return render(request,"bookmeeting.html", {'error': "Failed to fetch user data from Calendly."})
    return render(request, 'bookmeeting.html')

def fetch_events(request):
    user_resp = requests.get(
        "https://api.calendly.com/users/me",
        headers={"Authorization": access_token}
    )
    
    if user_resp.status_code != 200:
        return JsonResponse({"error": "Failed to fetch user data"}, status=500)
    
    user_uri = user_resp.json()["resource"]["uri"]
    
    events_resp = requests.get(
        f"https://api.calendly.com/scheduled_events?user=" + user_uri
,
        headers={"Authorization": access_token}
    )
    
    if events_resp.status_code != 200:
        return JsonResponse({"error": "Failed to fetch events"}, status=500)
    
    events = events_resp.json()["collection"]
    all_data =[]

    for event in events:
        event_uri = event["uri"]
        invitee_url = event_uri + "/invitees"

        invitee_resp = requests.get(invitee_url,headers={"Authorization": access_token})
        
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
    return JsonResponse({"data": all_data})
def availability(request):
        user_avail = requests.get ( 
            "https://api.calendly.com/users/me",
            headers = {
            "Authorization": access_token
            }
        )
        if user_avail.status_code != 200:
            return JsonResponse({"error":"failed to fetch user data"})    
        user_uri = user_avail.json()["resource"]["uri"]
        avail_resp = requests.get(
            url = f"https://api.calendly.com/user_availability_schedules?user={user_uri}",
            headers={
                "Authorization":access_token
            }
        )
        if avail_resp.status_code ==200:
            schedules = avail_resp.json().get("collection", [])
            if "organization" in schedules:
                org_uri = schedules[0]["organization"]
            else:
                return JsonResponse({"error": "No availability schedules found"})
            event_type_resp = requests.get(
            f"https://api.calendly.com/event_types?user={user_uri}",
            headers={
                "Authorization":access_token
            }
        )
        if event_type_resp.status_code != 200:
            return JsonResponse({"error:Failed to fetch events"})
        events = event_type_resp.json()['collection', []]
        data = []

        for event in events:
            event_uri = event['uri']

            start_time = datetime.utcnow().isoformat()+"Z"
            end_time = (datetime.utcnow() +  timedelta(days=7)).isoformat + "Z"

            avail_resp = requests.post(
                "https://api.calendly.com/availability",
                headers={
                    "Authorization":access_token,
                    "Content-Type": "application/json"
                },
                json = {
                    "event_type":event_uri,
                    "invitee_email": "thasniabbas76@gmail.com",
                    "start_time":start_time,
                    "end_time":end_time
                }
            )
            # if avail_resp.status_code == 200:
            #     slots = avail_resp.json().get("collection",[])
            #     data.append({
            #         "event_name":event["name"],
            #         "available_slots": slots
            #     })
            if avail_resp.status_code == 200:
                data = avail_resp.json()
                print("Available Slots:")
                for slot in data.get("collection", []):
                    print(f"- {slot['start_time']} to {slot['end_time']}")
            else:
                print("Error:", avail_resp.status_code, avail_resp.text)
        return JsonResponse({"data":data})
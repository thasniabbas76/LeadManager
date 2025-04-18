from django.shortcuts import render

# Create your views here.
def book_meeting(request):
    return render(request, 'bookmeeting.html')
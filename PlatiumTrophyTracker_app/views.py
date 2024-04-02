from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Count
from .forms import TrophyTrackerForm  # Importing TrophyTrackerForm from the correct location
from .models import UserAccount, TrophyTracker

def index(request):
    # Call the home view function to get the data
    users = UserAccount.objects.filter(isActive=True).annotate(num_trophytrackers=Count('trophytracker')).order_by('?')[:10]
    # Render the index.html template with the data
    return render(request, 'PlatiumTrophyTracker_app/index.html', {'users': users})

def create_trophytracker(request):
    if request.method == 'POST':
        form = TrophyTrackerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trophytracker_list')  # Redirect to a page where you list all TrophyTrackers
    else:
        form = TrophyTrackerForm()
    user_accounts = UserAccount.objects.all()  # Pass all UserAccounts to the template for the dropdown
    return render(request, 'PlatiumTrophyTracker_app/create_trophytracker.html', {'form': form, 'user_accounts': user_accounts})

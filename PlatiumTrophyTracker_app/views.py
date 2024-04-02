from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Count
from .forms import TrophyTrackerForm  
from .models import UserAccount, TrophyTracker
from django.shortcuts import render, get_object_or_404
from .models import UserAccount
from .models import TrophyTracker
from django.views.generic.edit import CreateView

def index(request):
    # Get 10 random active users along with the count of TrophyTrackers they have
    users = UserAccount.objects.filter(is_active=True).annotate(num_trophytrackers=Count('trophytracker')).order_by('?')[:10]
    # Render the index.html template with the data
    return render(request, 'PlatiumTrophyTracker_app/index.html', {'users': users})

def user_account_detail(request, pk):
    user_account = get_object_or_404(UserAccount, pk=pk)
    trophy_trackers = user_account.trophytracker_set.all()
    return render(request, 'PlatiumTrophyTracker_app/user_account_detail.html', {'user_account': user_account, 'trophy_trackers': trophy_trackers})

def trophy_tracker_detail(request, pk):
    trophy_tracker = get_object_or_404(TrophyTracker, pk=pk)
    return render(request, 'PlatiumTrophyTracker_app/trophy_tracker_detail.html', {'trophy_tracker': trophy_tracker})

from django.shortcuts import render, redirect
from .models import TrophyTracker, UserAccount

def create_trophytracker(request):
    if request.method == 'POST':
        # Extract data from POST request
        game_title = request.POST.get('game_title')
        game_difficulty = int(request.POST.get('game_difficulty'))
        description = request.POST.get('description')
        
        # Create TrophyTracker instance
        trophy_tracker = TrophyTracker.objects.create(
            game_title=game_title,
            game_difficulty=game_difficulty,
            description=description,
            userAccount=request.user.useraccount  # Assuming user is authenticated
        )
        
        # Redirect to detail page of newly created TrophyTracker
        return redirect(trophy_tracker)
    
    # Render the template for creating TrophyTracker
    return render(request, 'create_trophytracker.html')
     
def update_trophytracker(request, pk):
    trophytracker = get_object_or_404(TrophyTracker, pk=pk)
    if request.method == 'POST':
        form = TrophyTrackerForm(request.POST, instance=trophytracker)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page or to the homepage if the referrer is not available
    else:
        form = TrophyTrackerForm(instance=trophytracker)
    return render(request, 'PlatiumTrophyTracker_app/update_trophytracker.html', {'form': form})
 
def delete_confirmation(request, pk):
    trophy_tracker = get_object_or_404(TrophyTracker, pk=pk)
    if request.method == 'POST':
        trophy_tracker.delete()
        # Redirect to the user account detail page after deleting the Trophy Tracker
        return redirect('user_account_detail', pk=trophy_tracker.user_account.pk)
    return render(request, 'PlatiumTrophyTracker_app/delete_confirmation.html', {'trophy_tracker': trophy_tracker})
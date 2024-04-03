from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Count
from .models import UserAccount, TrophyTracker
from django.shortcuts import render, get_object_or_404
from .models import UserAccount
from .models import TrophyTracker
from .forms import TrophyTrackerForm

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

def create_trophy_tracker(request):
    if request.method == 'POST':
        form = TrophyTrackerForm(request.POST)
        if form.is_valid():
            trophy_tracker = form.save()
            # Redirect to the detail view of the associated UserAccount
            return redirect('user_account_detail', pk=trophy_tracker.userAccount.pk)
    else:
        form = TrophyTrackerForm()
    return render(request, 'PlatiumTrophyTracker_app/trophytracker_form.html', {'form': form})
 
def update_trophy_tracker(request, pk):
    trophy_tracker = get_object_or_404(TrophyTracker, pk=pk)
    if request.method == 'POST':
        form = TrophyTrackerForm(request.POST, instance=trophy_tracker)
        if form.is_valid():
            form.save()
            return redirect('user_account_detail', pk=pk)  # Redirect to detail view after update
    else:
        form = TrophyTrackerForm(instance=trophy_tracker)
    return render(request, 'PlatiumTrophyTracker_app/update_trophy_tracker.html', {'form': form})
 
def delete_trophy_tracker(request, pk):
    trophy_tracker = get_object_or_404(TrophyTracker, pk=pk)
    user_account_id = trophy_tracker.userAccount_id  # Store user account ID for redirect
    if request.method == 'POST':
        trophy_tracker.delete()
        return redirect('user_account_detail', pk=user_account_id)  # Redirect to user account detail
    return render(request, 'PlatiumTrophyTracker_app/delete_confirmation_trophy_tracker.html', {'user_account_id': user_account_id})
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Count
from .models import User, UserAccount, TrophyTracker
from django.shortcuts import get_object_or_404
from .models import UserAccount
from .models import TrophyTracker
from .forms import TrophyTrackerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
import requests
from bs4 import BeautifulSoup



def index(request):
    # Get 10 random active users along with the count of TrophyTrackers they have
    users = UserAccount.objects.filter(is_active=True).annotate(num_trophytrackers=Count('trophytracker')).order_by('?')[:10]
    
    return render(request, 'PlatiumTrophyTracker_app/index.html', {'users': users})

def user_account_detail(request, pk):
    user_account = get_object_or_404(UserAccount, pk=pk)
    trophy_trackers = user_account.trophytracker_set.all()
    return render(request, 'PlatiumTrophyTracker_app/user_account_detail.html', {'user_account': user_account, 'trophy_trackers': trophy_trackers})

def trophy_tracker_detail(request, pk):
    trophy_tracker = get_object_or_404(TrophyTracker, pk=pk)
    return render(request, 'PlatiumTrophyTracker_app/trophy_tracker_detail.html', {'trophy_tracker': trophy_tracker})

def create_trophy_tracker(request):
    # Update game choices before rendering the form
    TrophyTracker.update_game_choices()
    
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
            return redirect('user_account_detail', pk=trophy_tracker.userAccount.pk)  # Redirect to detail view of associated UserAccount
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

def trophy_tracker_list(request):
    trophy_trackers = TrophyTracker.objects.all().order_by('game_title')
    return render(request, 'PlatiumTrophyTracker_app/list_trophy_tracker.html', {'trophy_trackers': trophy_trackers})
 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the desired page after login (e.g., the index page)
            return redirect('index')  # Assuming 'index' is the name of your index view or URL
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'registration/login.html')

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')  # Redirect to the desired page after logout
    else:
        return render(request, 'registration/logout.html')
 
 
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the index page after registration
            return redirect('index')  # Assuming 'index' is the name of your index view or URL
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def game_list(request):
    url = "https://www.truetrophies.com/gamelist"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find_all("tr")

    games = []
    for row in rows:
        cell_game = row.find("td", class_="game")
        if cell_game:
            game_link = cell_game.a["href"]
            game_name = cell_game.a.get_text()
            img_url = row.find("td", class_="gamethumb").img["src"]
            completion_time = row.find_all("td")[6].get_text(strip=True) if len(row.find_all("td")) >= 7 else "N/A"
            rating = row.find("td", class_="icon-rating").get_text(strip=True).split()[-1] if row.find("td", class_="icon-rating") else "N/A"
            games.append({
                "name": game_name,
                "link": game_link,
                "image_url": img_url,
                "completion_time": completion_time,
                "rating": rating
            })

    return render(request, 'PlatiumTrophyTracker_app/game_list.html', {'games': games})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from .models import Car, Arena, GameUpdate, Achievement, Tournament, VisitorComment, Highlight
from .forms import VisitorCommentForm, HighlightForm

def home(request):
    featured_cars = Car.objects.all()[:3]
    featured_arenas = Arena.objects.all()[:2]
    recent_updates = GameUpdate.objects.order_by('-release_date')[:3]
    recent_comments = VisitorComment.objects.order_by('-created_at')[:5]
    featured_highlights = Highlight.objects.filter(is_featured=True).order_by('-created_at')[:3]
    
    context = {
        'featured_cars': featured_cars,
        'featured_arenas': featured_arenas,
        'recent_updates': recent_updates,
        'recent_comments': recent_comments,
        'featured_highlights': featured_highlights,
    }
    return render(request, 'museum/home.html', context)

def car_collection(request):
    cars = Car.objects.all().order_by('rarity', 'name')
    return render(request, 'museum/car_collection.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'museum/car_detail.html', {'car': car})

def arena_collection(request):
    arenas = Arena.objects.all().order_by('arena_type', 'name')
    return render(request, 'museum/arena_collection.html', {'arenas': arenas})

def arena_detail(request, arena_id):
    arena = get_object_or_404(Arena, id=arena_id)
    return render(request, 'museum/arena_detail.html', {'arena': arena})

def game_history(request):
    updates = GameUpdate.objects.all().order_by('-release_date')
    return render(request, 'museum/game_history.html', {'updates': updates})

def update_detail(request, update_id):
    update = get_object_or_404(GameUpdate, id=update_id)
    return render(request, 'museum/update_detail.html', {'update': update})

def achievements(request):
    achievements_list = Achievement.objects.all().order_by('difficulty', 'title')
    return render(request, 'museum/achievements.html', {'achievements': achievements_list})

def tournaments(request):
    tournament_list = Tournament.objects.all().order_by('-date')
    return render(request, 'museum/tournaments.html', {'tournaments': tournament_list})

def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    highlights = Highlight.objects.filter(tournament=tournament)
    return render(request, 'museum/tournament_detail.html', {
        'tournament': tournament,
        'highlights': highlights
    })

def highlights(request):
    highlight_list = Highlight.objects.all().order_by('-created_at')
    
    # Фильтрация
    moment_type = request.GET.get('type')
    tournament_id = request.GET.get('tournament')
    search_query = request.GET.get('search')
    
    if moment_type:
        highlight_list = highlight_list.filter(moment_type=moment_type)
    if tournament_id:
        highlight_list = highlight_list.filter(tournament_id=tournament_id)
    if search_query:
        highlight_list = highlight_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(player__icontains=search_query)
        )
    
    tournaments_list = Tournament.objects.all()
    
    return render(request, 'museum/highlights.html', {
        'highlights': highlight_list,
        'tournaments': tournaments_list,
        'selected_type': moment_type,
        'selected_tournament': tournament_id,
        'search_query': search_query or ''
    })

def highlight_detail(request, highlight_id):
    highlight = get_object_or_404(Highlight, id=highlight_id)
    highlight.increment_views()
    
    # Получаем похожие хайлайты
    similar_highlights = Highlight.objects.filter(
        Q(moment_type=highlight.moment_type) |
        Q(tournament=highlight.tournament) |
        Q(player=highlight.player)
    ).exclude(id=highlight.id).distinct()[:4]
    
    return render(request, 'museum/highlight_detail.html', {
        'highlight': highlight,
        'similar_highlights': similar_highlights
    })

@login_required
def add_highlight(request):
    if request.method == 'POST':
        form = HighlightForm(request.POST, request.FILES)
        if form.is_valid():
            highlight = form.save()
            messages.success(request, f'Хайлайт "{highlight.title}" успешно добавлен!')
            return redirect('highlight_detail', highlight_id=highlight.id)
    else:
        form = HighlightForm()
    
    return render(request, 'museum/add_highlight.html', {'form': form})

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = VisitorCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('comments_list')
    else:
        form = VisitorCommentForm()
    
    return render(request, 'museum/add_comment.html', {'form': form})

@login_required
def comments_list(request):
    comments = VisitorComment.objects.all().order_by('-created_at')
    return render(request, 'museum/comments_list.html', {'comments': comments})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    return render(request, 'museum/logout_confirm.html')

def about(request):
    return render(request, 'museum/about.html')
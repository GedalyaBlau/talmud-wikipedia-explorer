from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, TalmudText, WikipediaArticle, Favorite, Highlight, Comment
from .forms import TextSearchForm
import requests
import requests
from django.shortcuts import render
from .forms import TextSearchForm

def get_talmudic_text(ref):
    url = f"https://www.sefaria.org/api/texts/{ref}?context=0"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data['hebrew_text'] = data['he']  # Add this line to store the Hebrew text
        return data
    else:
        return None

def get_wikipedia_article(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext&titles={title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        return page['extract']
    else:
        return None
from .models import TalmudText, WikipediaArticle

def home(request):
    form = TextSearchForm(request.GET or None)

    talmudic_texts = []
    wikipedia_articles = []

    if form.is_valid():
        talmudic_text_ref = form.cleaned_data['talmudic_text_ref']
        wikipedia_article_title = form.cleaned_data['wikipedia_article_title']

        if talmudic_text_ref:
            talmudic_text_data = get_talmudic_text(talmudic_text_ref)
            talmudic_text, created = TalmudText.objects.get_or_create(title=talmudic_text_data['title'],content=talmudic_text_data['text'],
            hebrew_content=talmudic_text_data['hebrew_text']  )
        talmudic_texts = [talmudic_text]


        if wikipedia_article_title:
            wikipedia_article_content = get_wikipedia_article(wikipedia_article_title)
            wikipedia_article, created = WikipediaArticle.objects.get_or_create(title=wikipedia_article_title,
                                                                                 content=wikipedia_article_content)
            wikipedia_articles = [wikipedia_article]

    context = {
        'form': form,
        'talmudic_texts': talmudic_texts,
        'wikipedia_articles': wikipedia_articles,
    }
    return render(request, 'explorer/home.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def add_favorite(request, talmud_text_id=None, wikipedia_article_id=None):
    if talmud_text_id:
        talmud_text = TalmudText.objects.get(id=talmud_text_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, talmud_text=talmud_text)
    elif wikipedia_article_id:
        wikipedia_article = WikipediaArticle.objects.get(id=wikipedia_article_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, wikipedia_article=wikipedia_article)
    return redirect('home')

@login_required
def add_highlight(request, talmud_text_id=None, wikipedia_article_id=None):
    if request.method == 'POST':
        selected_text = request.POST['selected_text']
        if talmud_text_id:
            talmud_text = TalmudText.objects.get(id=talmud_text_id)
            highlight = Highlight(user=request.user, talmud_text=talmud_text, highlighted_text=selected_text)  # Changed 'text' to 'highlighted_text'
        elif wikipedia_article_id:
            wikipedia_article = WikipediaArticle.objects.get(id=wikipedia_article_id)
            highlight = Highlight(user=request.user, wikipedia_article=wikipedia_article, highlighted_text=selected_text)  # Changed 'text' to 'highlighted_text'
        highlight.save()
    return redirect('home')

from .forms import CommentForm

@login_required
def add_comment(request, talmud_text_id=None, wikipedia_article_id=None):
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment_text = form.cleaned_data['comment_text']
        if talmud_text_id:
            talmud_text = TalmudText.objects.get(id=talmud_text_id)
            comment = Comment(user=request.user, talmud_text=talmud_text, content=comment_text)
       

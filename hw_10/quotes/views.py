from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    Q = Quote.objects.all()
    for quote in Q:
        quote_tags = Tag.objects.filter(quote=quote)
        quote.tags.set(quote_tags)

    per_page = 10
    paginator = Paginator(list(Q), per_page)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    # print(page_number)
    page_obj = paginator.get_page(page_number)
    try:
        quotes_on_page = paginator.page(page_number)
    except PageNotAnInteger:
        quotes_on_page = paginator.page(1)
    except EmptyPage:
        quotes_on_page = paginator.page(1)


    return render(request, "quotes/index.html",
                  context={"quotes": quotes_on_page,
                           'page_obj': page_obj})


def quotes_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    quote_list = Quote.objects.filter(tags=tag)
    paginator = Paginator(quote_list, 10)  # Show 10 quotes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quotes/quotes_by_tag.html', {'page_obj': page_obj, 'tag': tag})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/author_detail.html', {'author': author, 'quotes': quotes})


@login_required
def add_quote(request):
    form = QuoteForm(instance=Quote())
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            form.save()
            return redirect(to='index')
    return render(request, 'quotes/add_quote.html',
                  context={'title': 'Quotes to Scrape', 'form': form})


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            form.save()
            return redirect(to='index')
    return render(request, 'quotes/add_author.html',
                  context={'title': 'Great Quotes ', 'form': form})
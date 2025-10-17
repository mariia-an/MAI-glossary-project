from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Term, Category

def home(request):
    """Главная страница"""
    categories = Category.objects.all()[:8]
    recent_terms = Term.objects.filter(is_published=True).order_by('-created_at')[:10]
    popular_terms = Term.objects.filter(is_published=True).order_by('-created_at')[:5]
    
    context = {
        'categories': categories,
        'recent_terms': recent_terms,
        'popular_terms': popular_terms,
    }
    return render(request, 'glossary/home.html', context)

def category_list(request):
    """Список всех категорий"""
    categories = Category.objects.all()
    return render(request, 'glossary/category_list.html', {'categories': categories})

def category_detail(request, slug):
    """Детальная страница категории"""
    category = get_object_or_404(Category, slug=slug)
    terms = Term.objects.filter(category=category, is_published=True)
    
    context = {
        'category': category,
        'terms': terms,
    }
    return render(request, 'glossary/category_detail.html', context)

def term_list(request):
    """Список всех терминов"""
    terms = Term.objects.filter(is_published=True).order_by('title')
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        terms = terms.filter(category__slug=category_slug)
    
    # Поиск
    query = request.GET.get('q')
    if query:
        terms = terms.filter(
            Q(title__icontains=query) | 
            Q(definition__icontains=query) |
            Q(explanation__icontains=query)
        )
    
    context = {
        'terms': terms,
        'query': query,
    }
    return render(request, 'glossary/term_list.html', context)

def term_detail(request, slug):
    """Детальная страница термина"""
    term = get_object_or_404(Term, slug=slug, is_published=True)
    related_terms = Term.objects.filter(
        category=term.category, 
        is_published=True
    ).exclude(id=term.id)[:5]
    
    context = {
        'term': term,
        'related_terms': related_terms,
    }
    return render(request, 'glossary/term_detail.html', context)

def search(request):
    """Страница поиска"""
    query = request.GET.get('q', '')
    terms = Term.objects.filter(is_published=True)
    
    if query:
        terms = terms.filter(
            Q(title__icontains=query) | 
            Q(definition__icontains=query) |
            Q(explanation__icontains=query)
        )
    
    context = {
        'terms': terms,
        'query': query,
        'results_count': terms.count(),
    }
    return render(request, 'glossary/search.html', context)
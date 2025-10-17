from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.CharField(max_length=50, default='📚', verbose_name='Иконка')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Term(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Термин')
    slug = models.SlugField(unique=True, verbose_name='URL')
    definition = models.TextField(verbose_name='Определение')
    explanation = models.TextField(blank=True, verbose_name='Подробное объяснение')
    examples = models.TextField(blank=True, verbose_name='Примеры использования')
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='terms',
        verbose_name='Категория'
    )
    
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium',
        verbose_name='Сложность'
    )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Автор'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    
    class Meta:
        verbose_name = 'Термин'
        verbose_name_plural = 'Термины'
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('term_detail', kwargs={'slug': self.slug})

from django.db import models
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    CATEGORIES = [
        ('rockets', 'ракеты'),
        ('science', 'наука'),
    ]
    slug = models.SlugField(unique=True)
    google_doc_id = models.CharField('id гугл-документа', max_length=100, null=True,
                                     blank=True, db_index=True)
    category = models.CharField('категория', choices=CATEGORIES, max_length=20, blank=True, db_index=True)

    title = models.CharField('заголок', max_length=100)
    teaser_text = models.TextField('тизер', blank=True)
    teaser_image = models.ImageField('картинка тизера', blank=True)

    html = models.TextField('текст', help_text='HTML', blank=True)
    source_title= models.CharField('первоисточник', max_length=100, blank=True)
    source_link= models.URLField('ссылка на первоисточник', blank=True)
    published = models.DateField('опубликовано', null=True, blank=True, db_index=True,
                                 help_text='Оставьте пустым чобы скрыть из выдачи')

    def __str__(self):
        return self.slug
    def get_absolute_url(self):
        return reverse('post', kwargs={
            'slug': self.slug
        })



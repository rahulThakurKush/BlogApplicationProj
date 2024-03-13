from django import template
from blog_app.models import Category

register = template.Library()

@register.simple_tag
def show_categories():
    categories = Category.objects.all()
    return categories

   
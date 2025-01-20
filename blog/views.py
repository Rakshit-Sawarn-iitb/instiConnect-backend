from django.shortcuts import render
from .models import Blog

# List all blogs
def blog_list(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})



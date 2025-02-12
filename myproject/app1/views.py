from django.shortcuts import render, get_object_or_404
from . models import Blog, Category, Tag

# Create your views here.

def home(request):
    blogs = Blog.objects.all().order_by('-created_at')  # Show latest posts first
    query = request.GET.get('q', '')  # Get search term
    selected_category = request.GET.get('category', '')  # Fetch selected category
    tag_id = request.GET.get('tag', '')
    tags = Tag.objects.all()  # Fetch all tags
    categories = Category.objects.all()

    myblogs = Blog.objects.all()

    if selected_category:
        blogs = blogs.filter(category_id=selected_category)
    
    if query:
        blogs = blogs.filter(title__icontains=query)  # Search by title

    if tag_id:
        blogs = blogs.filter(tags__id=tag_id)
    
    context = {
        'myblogs': myblogs,
        'query': query,
        'categories': categories,
        'selected_category': selected_category,
        'blogs': blogs,
        'tags': tags,
        'selected_tag': tag_id
    }
    return render(request, 'app1/home.html' , context)

def about(request):
    return render(request, 'app1/about.html') # type: ignore

def contact(request):
    return render(request, 'app1/contact.html')

def app2_page(request):
    return render(request, 'app1/app2_page.html')

def app3_page(request):
    return render(request, 'app1/app3_page.html')

def details(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'app1/details.html', {'blog': blog})
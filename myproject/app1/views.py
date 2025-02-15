from django.shortcuts import render, get_object_or_404, redirect
from . models import Blog, Category, Tag, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import format_html
from .forms import CommentForm



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



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, "Password does not match!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

         # Send confirmation email
        subject = "🎉 Welcome to MyApp!"
        text_content = f"Hi {username},\n\nThank you for registering at MyApp. We're excited to have you on board!"

        # HTML Content with styling
        html_content = format_html(f"""
            <div style="font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #f4f4f4;">
                <div style="background: white; padding: 20px; border-radius: 10px; max-width: 500px; margin: auto;">
                    <img src="https://yourwebsite.com/static/logo.png" alt="MyApp Logo" width="100" style="margin-bottom: 20px;">
                    <h2 style="color: #007bff;">Welcome, {username}! 🎉</h2>
                    <p style="color: #555;">Thank you for joining <strong>MyApp</strong>. We're excited to have you with us!</p>
                    <a href="https://yourwebsite.com/login" style="display: inline-block; padding: 10px 20px; color: white; background: #007bff; text-decoration: none; border-radius: 5px; margin-top: 20px;">Login Now</a>
                    <p style="margin-top: 20px; color: #777;">If you have any issues, feel free to contact us at support@myapp.com</p>
                </div>
            </div>
        """)

        email_message = EmailMultiAlternatives(subject, text_content, 'mezie.nwaka@gmail.com', [email])
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        messages.success(request, "Account created successfully! Check your email for a confirmation.")
        return redirect('login')

    return render(request, 'app1/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            email = user.email
            print(email)
            # Send confirmation email
            subject = "Welcome to MyApp!"
            message = f"Hi {username},\n\nThank you for logging in to MyApp. We're excited to have you back!"
            from_email = 'mezie.nwaka@gmail.com'  # Must match EMAIL_HOST_USER in settings
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
            return redirect('/')  # Redirect to home page
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, 'app1/login.html')



def details(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all()  # Get all comments for this blog post

    if request.method == "POST":
        if request.user.is_authenticated:  # Ensure user is logged in
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = blog  # Link the comment to the blog post
                comment.user = request.user  # Assign the logged-in user
                comment.save()
                return redirect('details', blog_id=blog.id)  # Refresh the page after comment
        else:
            return redirect('login')  # Redirect to login if user isn't logged in
    else:
        form = CommentForm()

    context = {
        'blog': blog,
        'comments': comments,
        'form': form,
    }
    return render(request, 'app1/details.html', context)

    
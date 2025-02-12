{% extends 'app1/base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
<h1>All Blog Posts</h1>

<!-- Search and Filter Form -->
<form method="GET" action="">
    <input type="text" name="q" placeholder="Search blogs..." value="{{ query }}">

    <select name="category">
        <option value="">All Categories</option>
        {% for cat in categories %}
        <option value="{{ cat.id }}" {% if selected_category == cat.id|stringformat:"s" %}selected{% endif %}>
            {{ cat.name }}
        </option>
        {% endfor %}
    </select>

    <button type="submit">Search</button>
</form>


{% for blog in blogs %}
<div class="card mb-3">
    <div class="card-body">
        <p>Blog count: {{ blogs.count }}</p>
        <h2>{{ blog.title }}</h2>
        {% if blog.image %}
        <img src="{{ blog.image.url }}" alt="Blog Image" style="width: 100px; height: auto;">
        {% endif %}
        <p><strong>Category:</strong> {{ blog.category }}</p>
        <p>{{ blog.content|truncatewords:20 }}</p>
        <p><small>Posted on {{ blog.created_at }}</small></p>
        <a href="{% url 'blog_detail' blog.id %}">Read More</a>
    </div>
</div>
{% empty %}
<p>No blog posts found.</p>
{% endfor %}

{% endblock %}
from django.shortcuts import render, get_object_or_404, redirect

from .models import Blog, Author, Comment
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import CommentForm

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_blogs = Blog.objects.all().count()


    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_blogs': num_blogs,
        'num_authors': num_authors,
        'num_visits' : num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5
    
class BlogDetailView(generic.DetailView):
    model = Blog

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5
    
    
class AuthorDetailView(generic.DetailView):
    model = Author

class BlogCreate(PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'author', 'description']
    permission_required = 'catalog.add_blog'

@login_required
def add_comment(request, pk):
    """View function for adding a comment."""
    blog = get_object_or_404(Blog, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CommentForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            new_comment = form.save(commit=False)
             # Assign the current blog to the comment
            new_comment.blog = blog
            new_comment.author = request.user
            new_comment.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('blog-detail', kwargs={"pk": pk}))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CommentForm()

    context = {
        'form': form,
        'blog': blog,
    }

    return render(request, 'catalog/add_comment.html', context)
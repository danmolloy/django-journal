from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import EntryForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm



from .models import Entry

@method_decorator(login_required(login_url='accounts/login/'), name='dispatch')
class IndexView(generic.ListView):
    template_name = "journal/index.html"
    context_object_name = "all_entries"
    def get_queryset(self) -> QuerySet[Any]:
        return Entry.objects.filter(author=self.request.user).order_by("-pub_date")

class DetailView(generic.DetailView):
    model = Entry
    template_name = "journal/detail.html"


def create(request):
    if request.method == "POST":
        new_post = EntryForm(request.POST)
        if new_post.is_valid:
            entry = new_post.save(commit=False)
            entry.author = request.user  # Assign the user object directly
            entry.save()
            print(entry.author)
            return HttpResponseRedirect("/journal")

    else:
        form = EntryForm()
        return render(request, "journal/create.html", {"form": form})

def edit(request, entry_id):
    if request.method == "POST":
        print(request.POST.get("title"))
        edited_post = Entry.objects.get(id=entry_id)
        edited_post.title = request.POST.get("title")
        edited_post.body = request.POST.get("body")
        edited_post.save()
        return HttpResponseRedirect("/journal/" + str(edited_post.id))
        """ edited_detail = request.POST
        updated_post = EntryForm(edited_detail)
        updated_post.save()
        return HttpResponseRedirect("/journal/" + updated_post.id) """
        
    else:
        entry = Entry.objects.get(id=entry_id)
        return render(request, "journal/edit.html", {"entry": entry})


def delete(request, entry_id):
    if request.method == "POST":
        doomed_post = Entry.objects.get(id=entry_id)
        doomed_post.delete()
    return HttpResponseRedirect("/journal")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
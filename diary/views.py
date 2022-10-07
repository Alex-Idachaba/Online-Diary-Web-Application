from django.core import paginator
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from .models import Entry
from .forms import EntryForm
from django.db.models import Q
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

@login_required
def entry_list(request):
    entries = Entry.objects.filter(author=request.user).order_by('-date')

    paginator = Paginator(entries, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var
    }
    return render(request, 'entry_list.html', context)

@login_required
def create_entry(request):
    form = EntryForm()

    if request.method == 'POST':
        form_data = request.POST or None
        form = EntryForm(form_data)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.author = request.user
            form_instance.save()
            return redirect('entry_list')
    context = {
        'form': form
    }
    return render(request, 'entry_new.html', context)

@login_required
def entry_update(request, pk):
    entry = Entry.objects.get(id=pk)
    form = EntryForm(instance=entry)

    if request.method == 'POST':
        form_data = request.POST or None
        form = EntryForm(form_data, instance=entry)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.author = request.user
            form_instance.save()
            return redirect('entry_list')
    context = {
        'form': form
    }
    return render(request, 'entry_edit.html', context)

@login_required
def entry_delete(request, pk):
    entry = Entry.objects.get(id=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    context = {
        'entry':entry
    }
    return render(request, 'entry_delete.html', context)

login_required
def search(request):
    queryset = Entry.objects.filter(author=request.user)
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entry_detail.html'
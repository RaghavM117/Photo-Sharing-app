from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView , CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Photo

# Create your views here.

class PhotoListView(ListView):
    model = Photo
    template_name = 'photo/list.html'
    context_object_name = 'photos'
    
class PhotoTagListView(ListView):
    model = Photo
    template_name = 'photo/taglist.html'
    context_object_name = 'photos'
    
    def get_tag(self):
        return self.kwargs.get('tag')
    
    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"]=self.get_tag()
        return context
    
class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photo/detail.html'
    context_object_name = 'photo'
    
class PhotoCreateView(CreateView):
    model = Photo           
    fields = ['title','description','image','tags']
    template_name = 'photo/create.html'
    success_url = reverse_lazy('photo:list')
    
    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super().form_valid(form)
    
class UserIsSubmitter(UserPassesTestMixin):
    def get_photo(self):
        return get_object_or_404(Photo, pk = self.kwargs.get('pk'))
    
    def test_func(self):
        
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied("Sorry You're not allowed here")
        
class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photo/update.html'
    model = Photo
    fields = ['title','description','tags']
    success_url = reverse_lazy('photo:list')
    
class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photo/delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')
        
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .forms import CommentForm

from .models import Image

# Create your views here.
class UploadImageView(CreateView):
    template_name = "gallery/upload_image.html"
    model = Image
    fields = "__all__"
    success_url = "/"

class UserGalleryView(ListView):
    model = Image
    template_name = "gallery/user_gallery.html"

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

class ImageListView(ListView):
    model = Image
    template_name = "gallery/image_list.html"
    context_object_name = "images"

    def get_queryset(self):
        queryset = Image.objects.all()
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset

class ImageDetailView(FormView, DetailView):
    model = Image
    template_name = "gallery/image_detail.html"
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.image = self.get_object()
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("image-detail", kwargs={"pk": self.get_object().pk})
    
    def get(self, request, *args, **kwargs):
        image = self.get_object()

        # Store viewing history in session
        history = request.session.get('viewed_images', [])
        if image.id not in history:
            history.append(image.id)
        request.session['viewed_images'] = history

        return super().get(request, *args, **kwargs)

def viewing_history(request):
    history = request.session.get('viewed_images', [])
    images = Image.objects.filter(id__in=history)
    return render(request, "gallery/history.html", {"images": images})
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import FormView
from django.http import HttpResponse
from .models import PostAd
from .forms import PostAdForm
from django.utils import timezone
import requests
import json
from .apicaller import apiCaller

def post_list(request):
    l

def post_new(request):
    if request.method == "POST":
            form = PostAdForm(request.POST)
            post = form.save()
            post.created_date = timezone.now()
            post.save()
            posts2 = apiCaller(400,'uk','2017-12-03','2017-12-15')
            return render(request, 'polls/results.html', {'post': posts2})
    else:
        form = PostAdForm()
    return render(request, 'polls/post_ad.html', {'form': form})

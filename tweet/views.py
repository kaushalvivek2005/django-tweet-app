from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .serializers import TweetSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method =="POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

def tweet_delete(request, tweet_id):
    tweet= get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
         if request.method == 'POST':
             form= UserRegistrationForm(request.POST)
             if form.is_valid():
                 user =form.save(commit=False)
                 user.set_password(form.cleaned_data['password1'])
                 user.save()
                 login(request, user)
                 return redirect('tweet_list')
         else:
             form = UserRegistrationForm()
         return render(request, 'registration/register.html', {'form': form})

def tweet_detail_api(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    serializer = TweetSerializer(tweet)
    # json_data = JSONRenderer().render(serializer.data)
    # return HttpResponse(json_data, content_type='application/json')
    return JsonResponse(serializer.data)
def tweet_list_api(request):
    tweet = Tweet.objects.all()
    serializer = TweetSerializer(tweet, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def tweet_create_api(request):
    if request.method == 'POST':
        json_data = request.body
        stream =io.BytesIO(json_data)
        JSON_data = JSONParser().parse(stream)
        serializer = TweetSerializer(data=JSON_data)
        if serializer.is_valid():
            # serializer.save()
            serializer.save(user=request.user)
            msg = {'message': 'Tweet created successfully'}
            json_data = JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
            # return JsonResponse(msg, status=201)
        json_data = JSONRenderer().render(serializer.errors)
        return JsonResponse(serializer.errors)
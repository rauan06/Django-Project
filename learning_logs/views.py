from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic
from .forms import TopicForm
# Create your views here.
def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Show all topics"""
    topics = Topic.objects.all()
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show all Topics and Entries"""
    topics = Topic.objects.get(id = topic_id)
    entries = topics.entry_set.order_by('-date_added')
    context = {'topic': topics, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Add a new Topic"""
    if request.method != 'POST':
        """No topic was submitted, enter blank form"""
        form = TopicForm()
    else:
        """POST data submitted, proceed data"""
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs/topics.hmtl'))
    
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)

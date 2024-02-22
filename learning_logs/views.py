from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic
from .forms import TopicForm, EntryForm

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
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Add a new entry"""
    topic = Topic.objects.get(id = topic_id)

    if request.method != 'POST':
        """No entry was submitted, enter blank form"""
        form = EntryForm()
    else:
        """Succeffully recieved some data"""
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
        return HttpResponseRedirect(reverse('learning_logs:topic',
                                           args = [topic_id]))

    context = {'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/new_entry.html', context)


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')


@login_required
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


def edit_entry(request, entry_id):
    """Edit an entry"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if request.method != 'POST':
        """No data was recieved, return blank form"""
        form = EntryForm(instance=entry)
    else:
        """Succeffully recieved some data"""
        form = EntryForm(instance=entry, data=request.POST)
        form.save()
        if form.is_valid():
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))
        
    context = {'topic' : topic, 'form' : form, 'entry_id' : entry_id}
    return render(request, 'learning_logs/edit_entry.html', context)


def delete_topic(request, topic_id):
    """Deletes the topic"""
    topic = Topic.objects.get(id = topic_id)
    topic.delete()
    return HttpResponseRedirect(reverse('learning_logs:topics'))


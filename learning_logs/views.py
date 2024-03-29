from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
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
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show all Topics and Entries"""
    topic = Topic.objects.get(id = topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)



@login_required
def new_topic(request):
    """Add a new Topic"""
    if request.method != 'POST':
        """No topic was submitted, enter blank form"""
        form = TopicForm()
    else:
        """POST data submitted, proceed data"""
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry"""
    topic = Topic.objects.get(id = topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

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


@login_required
def edit_entry(request, entry_id):
    """Edit an entry"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

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


@login_required
def delete_topic(request, topic_id):
    """Deletes the topic"""
    topic = Topic.objects.get(id = topic_id)
    topic.delete()
    return HttpResponseRedirect(reverse('learning_logs:topics'))


@login_required
def delete_entry(request, entry_id):
    """Deletes an entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    entry.delete()
    return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic.id]))


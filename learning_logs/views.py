from django.shortcuts import render
from .models import Topic, Entry

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

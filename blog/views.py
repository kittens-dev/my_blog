from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import Topic, Entry, Comment
from .forms import TopicForm, EntryForm, CommentForm


def custom_page_not_found_view(request, exception):
   
    return render(request, "404.html", {})


def custom_error_view(request, exception=None):
    
    return render(request, "500.html", {})


# def custom_permission_denied_view(request, exception=None):
    
#     return render(request, "errors/403.html", {})


# def custom_bad_request_view(request, exception=None):
    
#     return render(request, "errors/400.html", {})


def index(request):

    entries = []
    topics = Topic.objects.all()
        
    for topic in topics:
        topic_entries = Entry.objects.filter(topic=topic)
        for entry in topic_entries:
            entries.append(entry)

    sorted_entries = sorted(entries, key=lambda item: item.date_added, reverse=True)

    context = {'entries':sorted_entries}

    return render(request, 'blog/index.html', context)
    # return render(request, 'blog/index.html')    


@login_required
def my_entries(request):

    entries = []
    topics = Topic.objects.filter(owner=request.user)
        
    for topic in topics:
        topic_entries = Entry.objects.filter(topic=topic)
        for entry in topic_entries:
            entries.append(entry)

    sorted_entries = sorted(entries, key=lambda item: item.date_added, reverse=True)

    context = {'entries':sorted_entries}

    return render(request, 'blog/my_entries.html', context)

    
@login_required
def topics(request):

    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}

    return render(request, 'blog/topics.html', context)


@login_required
def topic(request, topic_id):

    topic = get_object_or_404(Topic, id=topic_id)

    if not check_topic_owner(topic, request):
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}

    return render(request, 'blog/topic.html', context)


@login_required
def new_topic(request):

    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('blog:topics'))

    context = {'form':form}

    return render(request, 'blog/new_topic.html', context)


@login_required
def new_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)

    if not check_topic_owner(topic, request):
        raise PermissionDenied()

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('blog:topic', args=[topic_id]))

    context = {'topic':topic, 'form':form}

    return render(request, 'blog/new_entry.html', context)
    

@login_required
def edit_entry(request, entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if not check_topic_owner(topic, request):
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:topic', args=[topic.id]))

    context = {'entry':entry, 'topic':topic, 'form':form}

    return render(request, 'blog/edit_entry.html', context)


def entry(request, entry_id):

    entry = get_object_or_404(Entry, id=entry_id)

    comments = entry.comment_set.order_by('-date_added')
    
    if request.user.is_authenticated:
        if request.method != 'POST':
            form = CommentForm()
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.entry = entry
                new_comment.owner = request.user
                new_comment.save()
        context = {'entry':entry, 'comments':comments, 'form': form}
    else:
        context = {'entry':entry, 'comments':comments}

    return render(request, 'blog/entry.html', context)


def check_topic_owner(topic, request):

    return topic.owner == request.user



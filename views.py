from django.shortcuts import render_to_response 
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from u2u_messages.models import UserMessage
from forum.models import User

def _update_messages(new_messages):
    for message in new_messages:
        message.is_new = False
        message.save()
@login_required
def user(request, username=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    users = [user, request.user]
    messages = UserMessage.objects \
        .filter(user_to__in=users, user_from__in=users) \
        .order_by('send_date')
    new_messages = UserMessage.objects.filter(user_to=request.user, \
        user_from=user, is_new=True)
    _update_messages(new_messages)
    paginator = Paginator(messages, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        messages_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        messages_page = paginator.page(paginator.num_pages)
    return render_to_response('u2u_messages/user.html',
        { 'messages' : messages_page, 'user_to' : user },
        RequestContext(request)
    )

@login_required
def send(request):
    status = False
    if request.is_ajax():
        try:
            message = UserMessage()
            message.user_to = User.objects.get(pk=request.POST.get('user_id'))
            message.user_from = request.user
            message.text = request.POST.get('text')
            message.save()
            status = True
        except User.DoesNotExist:
            status = False
    response = {'status': status}
    json = simplejson.dumps(response, ensure_ascii=False)
    return HttpResponse(json, mimetype="application/json")

@login_required
def all(request, type=None):
    if type == 'inbox':
        messages = UserMessage.objects \
            .filter(user_to=request.user) \
            .order_by('send_date')
        new_messages = UserMessage.objects.filter(user_to=request.user, \
                is_new=True)
    elif type == 'send':
        messages = UserMessage.objects \
            .filter(user_from=request.user) \
            .order_by('send_date')
        new_messages = UserMessage.objects.filter(user_to=request.user, \
                is_new=True)
    else:
        messages = UserMessage.objects \
            .filter(Q(user_to=request.user) | Q(user_from=request.user)) \
            .order_by('send_date')
        new_messages = UserMessage.objects \
            .filter(Q(user_to=request.user) | Q(user_from=request.user)) \
            .filter(user_to=request.user, is_new=True)
    _update_messages(new_messages)
    paginator = Paginator(messages, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        messages_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        messages_page = paginator.page(paginator.num_pages)
    return render_to_response('u2u_messages/all.html',
        { 'messages' : messages_page },
        RequestContext(request)
    )

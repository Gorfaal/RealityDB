from django.shortcuts import *
from django.contrib.auth import *
from django.shortcuts import *
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from core.forms import *
from core.models import *
from django.contrib.auth.decorators import *
import time
import json
from django.core.context_processors import csrf
from forms import CreateAccountForm


def logout_view(request):
    """
    :param request: The HTTP request.
    :return: Logs the user out, then goes to the landing page.
    """
    logout(request)
    return redirect(home_view)


def login_view(request):
    """
    :param request: The HTTP request.
    :return: The landing page with the user.
    """
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            messages.error(request, 'Inactive account, please contact support to reactivate.')
    else:
        messages.error(request, 'Incorrect account. Please make an account, or contact support if you have forgotten your information.')
    return redirect(home_view)


def home_view(request):
    """
    :param request: The HTTP request.
    :return: The default web page
    """
    user = request.user
    categories = Category.objects.all()
    networks = Network.objects.all()
    form = ShowForm
    return render(request, 'home.html', {
        'user': user,
        'categories': categories,
        'networks': networks,
        'form': form})


def encode_date(date):
    """
    :param date: The string that represents a date in the format mm/dd/yyyy
    :return: The date formatted for the database
    """
    encoding_structure = time.strptime(date, "%m/%d/%Y")
    encoded = time.strftime("%Y-%m-%d", encoding_structure)
    return encoded


def create_show_view(request):
    """
    :param request: The HTTP request.
    :return: The landing page with an indication that the show was created
    """
    if not request.user.is_active:
        messages.warning(request, 'Please log on to add a show.')
        return redirect(home_view)
    if request.method == 'POST':
        name = request.POST['name']
        started = request.POST['started']
        ended = request.POST['started']
        network_ids = request.POST.getlist('networks')

        networks = []
        for network_id in network_ids:
            network = Network.objects.get(pk=network_id)
            networks.append(network)
        category_ids = request.POST.getlist('categories')

        categories = []
        for category_id in category_ids:
            category = Category.objects.get(pk=category_id)
            categories.append(category)

        thumbnail = request.FILES['thumbnail']
        user = request.user

        created = time.strftime("%Y-%m-%d")

        started_encoded = encode_date(started)
        ended_encoded = encode_date(ended)

        if user.is_superuser:
            show = Show(name=name, started=started_encoded, ended=ended_encoded, created=created, thumbnail=thumbnail)
            show.save()
            show.networks.add(*networks)
            show.categories.add(*categories)
            show.save()
            messages.success(request, 'Successfully created ' + name + '.')
        else:
            change = Changes(user=user, show=None, name=name, started=started_encoded, ended=ended_encoded, modified=created, thumbnail=thumbnail)
            change.save()
            change.networks.add(*networks)
            change.categories.add(*categories)
            change.save()
            messages.success(request,  name + ' has been submitted for review.')

    return redirect(home_view)


def change_log_view(request):
    """
    :param request: The HTTP request.
    :return: The change log view.
    """
    form = ShowForm
    new_suggestions = Changes.objects.filter(show=None).order_by('-modified')
    shows = Show.objects.all()
    return render(request, 'changes.html', {'form': form, 'new_suggestions': new_suggestions, 'shows': shows})


def accept_change_view(request, change_id):
    change = get_object_or_404(Changes, pk=change_id)

    if change.show is not None:
        show = change.show
        if change.name:
            show.name = change.name
        if change.started:
            show.started = change.started
        if change.ended:
            show.ended = change.ended
        if change.thumbnail:
            show.thumbnail = change.thumbnail
        show.save()
        show.networks = change.networks.all()
        show.categories = change.categories.all()
        show.save()
        change.accepted = True
        change.save()
        messages.success(request, 'Accepted the change to ' + show.name)
    else:
        show = Show(name=change.name, started=change.started, ended=change.ended, created=change.modified, thumbnail=change.thumbnail)
        show.save()
        show.networks = change.networks.all()
        show.categories = change.categories.all()
        show.save()
        change.accepted = True
        change.save()
        messages.success(request, 'Created the new show  ' + show.name)
    return redirect(change_log_view)


def filter_shows_view(request):
    name = request.POST['name']
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    try:
        network_ids = request.POST['networks[]']
    except MultiValueDictKeyError:
        network_ids = []
    try:
        category_ids = request.POST['categories[]']
    except MultiValueDictKeyError:
        category_ids = []
    networks = []
    for network_id in network_ids:
        network = get_object_or_404(Network, pk=network_id)
        networks.append(network)

    categories = []
    for category_id in category_ids:
        category = get_object_or_404(Category, pk=category_id)
        categories.append(category)

    filter_parameters = {}
    if name:
        filter_parameters['name__icontains'] = name
    if startDate:
        filter_parameters['started__gt'] = encode_date(startDate)
    if endDate:
        filter_parameters['ended__lt'] = encode_date(endDate)
    if networks:
        filter_parameters['networks__in'] = networks
    if categories:
        filter_parameters['categories__in'] = categories

    shows = Show.objects.all().filter(**filter_parameters)
    shows_json = []
    for show in shows:
        shows_json.append({'id': show.id, 'name': show.name, 'thumbnail': str(show.thumbnail)})
    return HttpResponse(json.dumps(shows_json), mimetype="application/json")


def create_account_view(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/successful')

    form = CreateAccountForm

    return render(request, 'create_account.html', {'form': form})
    #return render_to_response('create_account_view.html')


def account_successful_view(request):
    return render(request, 'account_successful.html')


def about_view(request):
    user = request.user
    form = ShowForm
    return render(request, 'about.html', {'user': user, 'form': form})


def suggest_change_view(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    user = request.user
    if user.is_active:
        if request.method == 'POST':
            form = ShowForm(request.POST, request.FILES)
            if user.is_superuser:
                show.name = request.POST['name']
                show.started = request.POST['started']
                show.ended = request.POST['ended']
                if 'thumbnail' in request.POST:
                    show.thumbnail = request.POST['thumbnail']
                show.save()
                show.networks = request.POST['networks']
                show.categories = request.POST['categories']
                show.save()
                messages.success(request, 'Successfully changed ' + show.name)
                return redirect(home_view)
            else:
                change = Changes()
                change.user = user
                change.show = show
                change.modified = time.strftime("%Y-%m-%d")
                change.name = request.POST['name']
                change.started = request.POST['started']
                change.ended = request.POST['ended']
                change.accepted = False
                if 'thumbnail' in request.POST:
                    change.thumbnail = request.POST['thumbnail']
                change.save()
                change.networks = request.POST['networks']
                change.categories = request.POST['categories']
                change.save()
                messages.success(request, 'Successfully added suggestion to ' + show.name)
                return redirect(home_view)
        else:
            form = ShowForm(
                initial={'name': show.name, 'started': show.started, 'ended': show.ended, 'created': show.created, 'networks': show.networks.all, 'categories': show.categories.all, 'thumbnail': show.thumbnail}
            )
        return render(request, 'suggest_change.html', {'form': form, 'show': show, 'user': user})
    else:
        return render(request, 'show_details.html', {'show': show})

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from datetime import datetime

#def index(request):
#    return HttpResponse('Rango says hello world! <br/> <a href="/rango/about/">About<a/>')
#
#def about(request):
#    return HttpResponse('Rango says here is the about page. <br/><a href="/rango/">Index<a/>')

#def index(request):
#    context_dict = {'boldmessage': "I am bold font from the context"}
#    return render(request, 'rango/index.html', context_dict)


def about(request):
#    return HttpResponse('Rango says here is the about page. <br/><a href="/rango/">Index<a/>')
    return render(request, 'rango/about.html')

#def index(request):
#    category_list = Category.objects.order_by('-likes')[:5]
#    page_list = Page.objects.order_by('-views')[:5]
#    context_dict = {'categories': category_list, 'pages': page_list, }
#
#
#    return render(request, 'rango/index.html', context_dict)

    
def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

        context_dict['category'] = category

        context_dict['category_name_slug'] = category.slug

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)
    

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):
    context_dict = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = cat.name
        context_dict['category_name_slug'] = category_name_slug

        context_dict['category'] = cat
        
        if request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
            else:
                print(form.errors)
        else:
            form = PageForm()

        context_dict['form'] = form

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/add_page.html', context_dict)

#def register(request):
#    registered = False
#
#    if request.method == 'POST':
#        user_form = UserForm(data=request.POST)
#        profile_form = UserProfileForm(data=request.POST)
#
#        if user_form.is_valid() and profile_form.is_valid():
#            user = user_form.save()
#    
#            user.set_password(user.password)
#            user.save()
#    
#            profile = profile_form.save(commit=False)
#            profile.user = user
#    
#            if 'picture' in request.FILES:
#                profile.picture = request.FILES['picture']
#    
#            profile.save()
#            
#            registered = True
#    
#        else:
#            print(user_form.errors, profile_form.errors)
#    else:
#        user_form = UserForm()
#        profile_form = UserProfileForm()
#
#    return render(request, 'rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered': registered} )
#
#def user_login(request):
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#
#        user = authenticate(username=username, password=password)
#
#        if user:
#            if user.is_active:
#                login(request, user)
#                return HttpResponseRedirect('/rango/')
#            else:
#                return HttpResponse("Your Rango account is disabled.")
#        else:
#            print("Invalid login details: {0}, {1}".format(username, password))   
#            return HttpResponse("Invalid login details supplied.")
#    else:
#        return render(request, 'rango/login.html', {})
#
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


#def index(request):
#
#    category_list = Category.objects.all()
#    page_list = Page.objects.order_by('-views')[:5]
#    context_dict = {'categories': category_list, 'pages': page_list}
#
#    # Get the number of visits to the site.
#    # We use the COOKIES.get() function to obtain the visits cookie.
#    # If the cookie exists, the value returned is casted to an integer.
#    # If the cookie doesn't exist, we default to zero and cast that.
#    visits = int(request.COOKIES.get('visits', '1'))
#
#    reset_last_visit_time = False
#    response = render(request, 'rango/index.html', context_dict)
#    # Does the cookie last_visit exist?
#    if 'last_visit' in request.COOKIES:
#        # Yes it does! Get the cookie's value.
#        last_visit = request.COOKIES['last_visit']
#        # Cast the value to a Python date/time object.
#        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
#
#        # If it's been more than a day since the last visit...
#        if (datetime.now() - last_visit_time).seconds > 2:
#            visits = visits + 1
#            # ...and flag that the cookie last visit needs to be updated
#            reset_last_visit_time = True
#    else:
#        # Cookie last_visit doesn't exist, so flag that it should be set.
#        reset_last_visit_time = True
#
#    context_dict['visits'] = visits
#    #Obtain our Response object early so we can add cookie information.
#    response = render(request, 'rango/index.html', context_dict)
#
#    if reset_last_visit_time:
#        response.set_cookie('last_visit', datetime.now())
#        response.set_cookie('visits', visits)
#
#    # Return response back to the user, updating any cookies that need changed.
#    return response
#

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    
    return HttpResponse(likes)

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__startswith=starts_with)

#    if cat_list and max_results > 0:
#        if len(cat_list) > max_results:
#            cat_list = cat_list[:max_results]

    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cat_list': cat_list })

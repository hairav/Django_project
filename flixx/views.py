from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
#from django.db.models import Q
from flixx.forms import LogIn, reviewing, search, SignUp
from flixx.models import movie, Genre, like, review
#from django.http import HttpResponse
import numpy
import random
from sklearn.tree import DecisionTreeClassifier
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User

likw=[]
dis=[]
movies = movie.objects.all()


def make(user):
    likw[:] = []
    dis[:] = []
    for i in like.objects.all():
        if i.user==user:
            if i.l==1:
                likw.append(i.movie)
            else:
                dis.append(i.movie)

def home(request):
    message = ''
    url = '/FliXx/'
    a = "LogIn"

    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            us = request.user
            #make(us)
            a = "logOut"
            return render(request, 'flixx/home.html',
                          {"lik": likw, "dis": dis, 'user': us, 'movies': movie.objects.order_by('-popularity')[:20],
                           's': a, 'message': message, 'url': url, 'action': "SignUp"})

        else:
            message="kata"
            form = SignUp()
            return render(request, 'flixx/home.html', {"lik":likw,"dis":dis, 'movies': movie.objects.order_by('-popularity')[:20], 's': a, 'url':url, 'message': message, 'form': form, 'action': "SignUp" })
    if request.user.is_authenticated():
        us = request.user
        # make(us)
        a = "logOut"
        return render(request, 'flixx/home.html',
                      {"lik": likw, "dis": dis, 'user': us, 'movies': movie.objects.order_by('-popularity')[:20],
                       's': a, 'message': message, 'url': url, 'action': "SignUp"})

    else:
        form = SignUp()
        return render(request, 'flixx/home.html', {"lik":likw,"dis":dis, 'movies': movie.objects.order_by('-popularity')[:20],'message':message,'url':url,'form':form,'action':"SignUp"})
def rogin(request):
    message = "Welcome back, please fill your credential ."
    url = '/FliXx/login/'
    a = "LogIn"
    gh=False
    if request.user.is_authenticated():
        auth_views.logout(request)
        return home(request)
    if request.method=='POST':
        form=LogIn(request.POST)
        if form.is_valid():
            username = request.POST['Username']
            password = request.POST['Password']
            user = authenticate( username=username, password=password)
            if user is not None:
                login(request, user)
                #make(user)
                a = 'LogOut'
                message = "Successful login. Welcome to FliXx " + str(user) + "."
                return render(request, 'flixx/home.html',
                              {"lik": likw, "dis": dis, 'user': user, 'movies': movie.objects.order_by('-dateofrelease')[:20],
                               's': a, 'message': message, 'url': url, 'action': "LogIn"})

            else:
                message = "Invalid Credentials."
                form = LogIn()
                gh=True
                return render(request, 'flixx/login.html',
                              {"gh":gh,"lik": likw, "dis": dis, 's': a, 'message': message, 'url': url, 'form': form,
                               'action': "LogIn"})
    else:
        form=LogIn()
        gh=True
        return render(request, 'flixx/login.html',
                      {'gh':gh,"lik": likw, "dis": dis, 's': a, 'message': message, 'url': url, 'form': form,
                       'action': "LogIn"})



def detailedview(request, id):
    mov=movie()
    form=''
    action = 'Review'
    message=''
    url = str(id)
    try:
        mov=movie.objects.get(id=id)
    except:
        message='You should not play with urls -_- .'
        mov=movie.objects.get(id=random.randint(100,4000))
    if request.user.is_authenticated():
        if request.method == "POST":
            form= reviewing(request.POST)
            if form.is_valid():
                r=form.cleaned_data['review']
                rev=review()
                rev.l=r
                rev.movie=mov
                rev.user=request.user
                rev.save()
        form=reviewing()


    g=[]
    te=[]
    for i in mov.genres.all():
        if i.Name not in te:
            g.append(i)
            te.append(i.Name)

    reviews=[]
    for i in review.objects.filter(movie=mov):
        reviews.append(i)
    return render(request,'flixx/Detailedview.html',
    {'movie':mov,'form':form,'url':url,'action':action,'message':message,'g':g,'reviews':reviews})

def lik(request,mi,uid):
    li=like()
    if request.user.is_authenticated():
        us=request.user
        try:
            for i in like.objects.filter(movie=movie.objects.get(id=int(mi))):
                if i.user == request.user:
                    i.delete()
        except:
            pass
        ti=like()
        ti.movie=movie.objects.get(id=mi)
        ti.user=request.user
        ti.l=int(uid)
        ti.save()
        print(ti)
        return detailedview(request, mi)
    else:
        return rogin(request)
def recommend(request):
    if not request.user.is_authenticated():
        return rogin(request)
    m = 'Hey '+str(request.user)+' Here are some movies we recommend based on your likes and dislikes  .'
    print(m)
    x=[]
    Y=[]
    for i in like.objects.filter(user=request.user):
        x.append(i.movie)
        Y.append(i.l)
    x1 = [i.getData() for i in x]
    X = []
    for i in x1:
        t = numpy.asarray(i,dtype=float)
        X.append(t)
    print(len(X))
    Y = numpy.asarray(Y,dtype=float)
    c = DecisionTreeClassifier()

    if len(X)==0:
        return home(request)
    c.fit(X, Y)
    T = []
    t = []
    for i in movie.objects.all():
        if i not in x:
            T.append(numpy.asarray(i.getData()))
            t.append(i)
    L = c.predict(T)
    print (len(movie.objects.all()))
    li = []
    print(len(T))
    for i in range(len(T)):
        if L[i] == 1:
            li.append(t[i])
    print(len([i for i in L if i ==0]))
    li.sort(key=lambda X:X.popularity)
    li.reverse()
    return render(request, 'flixx/recommendations.html', {"lik":likw,"dis":dis,'message': m, 'li': li[:20]})


def watchedmovies(request):
    if not request.user.is_authenticated():
        return rogin(request)
    us=request.user
    li = []
    di = []
    X = []
    Y = []
    for i in like.objects.filter(user=us):
        X.append(i.movie)
        Y.append(i.l)
        if i.l == 0:
            di.append(i.movie)
        else:
            li.append(i.movie)
    print(li)
    print(di)
    return render(request,'flixx/watchedmovies.html' ,{"lik":likw,"dis":dis,'li':li,'di':di})


def about_us(request):
    message='Hey ! '
    if request.user.is_authenticated():
        message+=str(request.user)
    return render(request,'flixx/about us.html',{"lik":likw,"dis":dis,'message':message})


def find(request):

    if request.method == "POST":
        form = search(request.POST,request.FILES)
        if form.is_valid():
            q = form.cleaned_data['Search']
            q = q.lower()
            t = set()
            mov = []
            for i in movies:
                w = q.split(' ')
                for r in w:
                    if r != '' and r in i.title.lower() or r in i.tag.lower() or r in i.overview.lower():
                        t.add(i)
            for i in t:
                mov.append(i)
            mov = sorted(mov,key=lambda x:x.popularity)
            mov.reverse()
            message = str(len(mov))+" results obtained as a result of your search "+q
            return render(request, 'flixx/explore.html',
                          {'movies': mov,'action':'Search','form':search(),'message':message})
        else:
            form = search()
            url = '/FliXx/Xplore/'
            action = 'Search'
            return render(request, 'flixx/explore.html',
                          {"lik":likw,"dis":dis,'movies': movies.order_by('-popularity')[:50], 'url': url, 'action': action, 'form': form})

    else:
        form = search()
        url = '/FliXx/Xplore/'
        action = 'Search'
        return render(request,'flixx/explore.html',{"lik":likw,"dis":dis,'movies':movies.order_by('-popularity')[:50],'url':url,'action':action,'form':form})

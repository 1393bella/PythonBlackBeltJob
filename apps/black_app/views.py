from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages

def index(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    else:
        return render(request, 'black_app/index.html')

def register(request):
    if request.method == 'POST':
        # validate form data
        print("///////////////////////////////")
        deervalid = User.objects.registerValidator(request.POST)
        # if valid:
        if deervalid['valid']:
            #   store user in session
            user = deervalid['user']
            request.session['id'] = user.id
            #   redirect to wall page
            return redirect('/dashboard')
            # else if invalid
            #   create error messages
            #   redirect to /
        else:
            for error in deervalid['errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('/')

def login(request):
    if request.method == 'POST':
        validation_response = User.objects.loginValidator(request.POST)
        if validation_response['valid']:
            user = validation_response['user']
            request.session['id'] = user.id
            return redirect('/dashboard')
        else:
            for error in validation_response['errors']:
                messages.add_message(request, messages.ERROR, error)
                return redirect('/')

def createJob(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        print(request.POST['title'])
        print(request.POST['description'])
        print(request.POST['location'])
        Job.objects.create(created_by=user, title=request.POST['title'], description=request.POST['description'], location=request.POST['location'])
        return redirect("/dashboard")
    return render(request, 'black_app/addJob.html')

def dashboard(request):
    user = User.objects.get(id=request.session['id'])
    all_jobs = Job.objects.all()
    my_jobs = all_jobs.filter(added_by=user)
    # esli ubrat nije 4 linii koda s 57 do 61 lines poluchitsya kogda dobavlyaew job,
    # job is still available in general list or table it will not automaticalyy removes from the table too, i rabotaet kak favorite , no ne udalyaet s general table.
    open_jobs = []
    for j in all_jobs:
        if not j.added_by:
            open_jobs.append(j)
    context = {
        "all_jobs": all_jobs,
        "user": user,
        "my_jobs": my_jobs,
        "open_jobs": open_jobs
        }
    return render(request,'black_app/dashboard.html', context)

def addJob(request, id):
    user = User.objects.get(id=request.session['id'])
    job = Job.objects.get(id=id)
    job.added_by=user
    job.save()
    return redirect('/dashboard')
    #takim obrazom здесь job v drugoi my list мы добавляем когда релайшн из one to many

def viewJob(request, num):
    user = User.objects.get(id=request.session['id'])
    job = Job.objects.get(id=num)
    context={
        'job': job,
        'signed_user': user,
        'took': job in user.added_jobs.all(),
        }
    
    return render(request, 'black_app/view.html', context)

def editJob(request, id):
    if request.method == "POST":
        edit = Job.objects.get(id=id)
        edit.title = request.POST['title']
        edit.description = request.POST['description']
        edit.location= request.POST['location']
        edit.save()
        return redirect('/dashboard')
    else:
        job = Job.objects.get(id=id)
        context = {
            "job" : job
        }
        return render (request,'black_app/edit.html',context)

def backtoDashboard(request):
    return redirect('/dashboard')

def deleteFromList(request,id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('/dashboard')

def deleteFromMyList(request,id):
    # user = User.objects.get(id=request.session['id'])
    # job_mylist = Job.objects.get(id=id)
    # user.added_jobs.remove(job_mylist)
    job = Job.objects.get(id=id)
    job.delete() 
    # this tho lines of code let the "delete button " to delete in my list and DB(database)odnovremenno , but i have uncomment 3 lines above 
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def backtoDashboard(request):
    return redirect('/dashboard')   

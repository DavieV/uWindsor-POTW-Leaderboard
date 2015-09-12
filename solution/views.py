from django.shortcuts import render
from student.models import Student
import student
from models import Solution
from problem.models import Problem
import problem.views
import errorpage

def add(request):
    if len(request.POST['submitcode']) == 0:
        return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
                "Please specify your submission code")
    if "source" not in request.FILES:
         return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
                "Please attach your source code")

    if "remember" in request.POST:
        request.session["submitcode"] = request.POST['submitcode']
    elif ("remember" not in request.POST) and ("submitcode" in request.session):
        del request.session["submitcode"]

    try:
        s = Student.objects.get(submit_code=request.POST['submitcode'])
    except:
         return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
                 "Invalid submission code")

    extra = ""
    try:
        sol = s.solution_set.get(year = request.POST['year'], week = request.POST['week'])
        sol.delete()
        extra = "<br />Your previous submission for this problem has been deleted"
    except:
        pass

    s.solution_set.create(year=request.POST['year'], week=request.POST['week'],
            source=request.FILES['source'], public = 'public' in request.POST)

    return problem.views.problem_stats(request, request.POST['year'], request.POST['week'],
            None, "Your code has been submitted for checking" + extra)

def show(request, solution_id):
    try:
        s = Solution.objects.get(pk=solution_id)
    except:
        return errorpage.views.index(request)
    recent_year = Problem.objects.filter(published=True).latest('year').year
    recent_week = Problem.objects.filter(published=True).latest('week').week
    context = {
        "solution":    s,
        "most_recent": s.year == recent_year and s.week == recent_week,
        "public":      s.public
    }
    return render(request, "solution/index.html", context)

def all(request):
    context = {
            "problems": Problem.objects.filter(published=True).order_by("-week")
    }
    return render(request, "solution/all.html", context)

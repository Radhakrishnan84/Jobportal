from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Category, Job, Application, SavedJob
from .forms import RegisterForm, LoginForm, ApplicationForm


def home(request):
    cats = Category.objects.all()
    latest = Job.objects.select_related("category").order_by("-posted_at")[:6]
    return render(request, "home.html", {"categories": cats, "latest_jobs": latest})


def jobs_list(request):
    category_slug = request.GET.get("category")
    location = request.GET.get("location", "").strip()
    jobs = Job.objects.select_related("category").all()
    if category_slug:
        jobs = jobs.filter(category__slug=category_slug)
    if location:
        jobs = jobs.filter(location__icontains=location)
    categories = Category.objects.all()
    return render(request, "jobs_list.html", {
        "jobs": jobs,
        "categories": categories,
        "current_category": category_slug,
        "current_location": location
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    form = ApplicationForm()
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Please login to apply.")
            return redirect(f"/auth/?next=/jobs/{pk}/")
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.user = request.user   # kept in DB only, not exposed
            app.save()
            messages.success(request, "Your application has been submitted.")
            return redirect("job_detail", pk=pk)
        else:
            messages.error(request, "There were errors. Please try again.")
    saved = False
    if request.user.is_authenticated:
        saved = SavedJob.objects.filter(user=request.user, job=job).exists()
    return render(request, "job_detail.html", {"job": job, "form": form, "saved": saved})


def auth_page(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "login":
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                messages.success(request, "Login successful.")
                return redirect(request.GET.get("next") or "home")
            register_form = RegisterForm()
            return render(request, "auth.html", {"login_form": form, "register_form": register_form})
        elif action == "register":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account created. Please login.")
                return redirect("login_register")
            login_form = LoginForm(request)
            return render(request, "auth.html", {"login_form": login_form, "register_form": form})
    return render(request, "auth.html", {"login_form": LoginForm(request), "register_form": RegisterForm()})


@login_required
def toggle_save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    obj, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        obj.delete()
        state = "removed"
    else:
        state = "saved"
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        from django.http import JsonResponse
        return JsonResponse({"status": state})
    return redirect(request.META.get("HTTP_REFERER", "jobs_list"))


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("home")

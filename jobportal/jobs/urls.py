from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("jobs/", views.jobs_list, name="jobs_list"),
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path("save/<int:pk>/", views.toggle_save_job, name="toggle_save_job"),
    path("auth/", views.auth_page, name="login_register"),
    path('logout/', views.logout_view, name="logout"),   # 👈 Added
]

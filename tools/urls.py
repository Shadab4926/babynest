from django.urls import path
from .views import (
    due_date_calculator,
    newborn_essentials_checklist,
    baby_vaccine_reminder,
    download_vaccine_pdf
)

app_name = "tools"

urlpatterns = [
    path("due-date-calculator/", due_date_calculator, name="due_date_calculator"),
    path("newborn-checklist/", newborn_essentials_checklist, name="newborn_checklist"),
    path("vaccine-reminder/", baby_vaccine_reminder, name="vaccine_reminder"),
    path("vaccine-reminder/pdf/", download_vaccine_pdf, name="download_vaccine_pdf"),
    path("test-pdf/", lambda r: download_vaccine_pdf(r), name="test_pdf"),  # Added comma here
    path("", due_date_calculator),
]
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BabyName
import csv
from io import TextIOWrapper
from django.utils.text import slugify


def generate_unique_slug(base_slug):
    slug = base_slug
    counter = 1
    while BabyName.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@admin.register(BabyName)
class BabyNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'religion', 'origin']
    change_list_template = "admin/names/babyname/change_list.html"  # ✅ for CSV upload button

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name="babyname_upload_csv"),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            if not csv_file or not csv_file.name.endswith(".csv"):
                messages.error(request, "Please upload a valid CSV file.")
                return redirect("..")

            try:
                reader = csv.DictReader(TextIOWrapper(csv_file.file, encoding='utf-8'))
                for row in reader:
                    name = row.get("name", "").strip()
                    if not name:
                        continue  # Skip blank names
                    
                    slug = generate_unique_slug(slugify(name))
                    
                    BabyName.objects.create(
                        name=name,
                        gender=row.get("gender", "").strip(),
                        meaning=row.get("meaning", "").strip(),
                        religion=row.get("religion", "").strip(),
                        origin=row.get("origin", "").strip(),
                        popularity=row.get("popularity", 0),
                        slug=slug
                    )
                messages.success(request, "CSV uploaded successfully!")
            except Exception as e:
                messages.error(request, f"Upload failed: {str(e)}")
            
            return redirect("..")

        return render(request, "admin/upload_csv.html")

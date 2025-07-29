from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, timedelta
from io import BytesIO

# Vaccine Reminder PDF Download
def download_vaccine_pdf(request):
    print("PDF generation view called")

    if request.method == "POST":
        dob_str = request.POST.get("dob")
        print("Received DOB:", dob_str)

        if not dob_str:
            return HttpResponse("Missing DOB", status=400)

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

            vaccine_schedule = [
                ("BCG", 0, False),
                ("Hepatitis B1", 0, False),
                ("OPV-0", 0, False),
                ("DTaP-1", 42, False),
                ("Hepatitis B2", 42, False),
                ("OPV-1", 42, False),
                ("Hib-1", 42, False),
                ("Rotavirus-1", 42, False),
                ("PCV-1", 42, False),
                ("DTaP-2", 70, False),
                ("Hib-2", 70, False),
                ("Rotavirus-2", 70, False),
                ("PCV-2", 70, False),
                ("DTaP-3", 98, False),
                ("Hib-3", 98, False),
                ("Hepatitis B3", 98, False),
                ("Rotavirus-3", 98, False),
                ("PCV-3", 98, False),
                ("MMR-1", 270, False),
                ("Varicella", 365, False),
                ("Hepatitis A-1", 365, False),
                ("Typhoid Conjugate", 365, False),
                ("DTaP Booster", 540, False),
                ("MMR-2", 540, False),
                ("Hepatitis A-2", 540, False),
                ("Typhoid Booster", 1095, True),
                ("Influenza (Annual)", 1095, True),
                ("DTP Booster", 1825, False),
                ("Tdap/Td", 3650, False),
                ("HPV Vaccine", 3650, True),
            ]

            schedule = [{
                "name": name + (" (Optional)" if optional else ""),
                "age_label": f"{days // 30} months" if days < 365 else f"{days // 365} years",
                "date": dob + timedelta(days=days)
            } for name, days, optional in vaccine_schedule]

            template = get_template("tools/vaccine_pdf_template.html")
            html = template.render({"schedule": schedule, "dob": dob})

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="vaccine_schedule.pdf"'

            pisa_status = pisa.CreatePDF(html, dest=response)

            if pisa_status.err:
                print("PDF generation error:", pisa_status.err)
                return HttpResponse("Error generating PDF", status=500)

            print("PDF generated successfully")
            return response

        except Exception as e:
            print("PDF generation failed:", e)
            return HttpResponse(f"Error: {e}", status=500)

    return HttpResponse("Invalid Request", status=400)


def due_date_calculator(request):
    due_date = None
    current_week = None
    trimester = None

    if request.method == "POST":
        lmp_str = request.POST.get('lmp')
        if lmp_str:
            try:
                # Parse LMP date from string
                lmp_date = datetime.strptime(lmp_str, "%Y-%m-%d").date()

                # Calculate due date: 280 days (40 weeks) after LMP
                due_date_obj = lmp_date + timedelta(days=280)
                due_date = due_date_obj.strftime("%B %d, %Y")  # Format nicely

                # Calculate current pregnancy week from today
                today = datetime.today().date()
                days_pregnant = (today - lmp_date).days
                if days_pregnant < 0:
                    # LMP date is in the future, invalid
                    current_week = "Invalid LMP date"
                    trimester = ""
                else:
                    current_week_num = days_pregnant // 7 + 1  # 1-based week count
                    current_week = f"{current_week_num}"

                    # Determine trimester
                    if current_week_num <= 12:
                        trimester = "First Trimester"
                    elif 13 <= current_week_num <= 27:
                        trimester = "Second Trimester"
                    elif current_week_num >= 28:
                        trimester = "Third Trimester"
                    else:
                        trimester = ""

            except ValueError:
                # Invalid date format
                current_week = "Invalid date format"
                trimester = ""

    context = {
        'due_date': due_date,
        'current_week': current_week,
        'trimester': trimester,
    }
    return render(request, 'tools/due_date_calculator.html', context)


from django.shortcuts import render

def newborn_essentials_checklist(request):
    checklist = []

    # Dummy master data — can be moved to DB or JSON for better management
    base_items = {
        '0-3': ['Onesies', 'Swaddle blankets', 'Diapers', 'Baby wipes', 'Newborn bottles'],
        '3-6': ['Teething toys', 'Socks & mittens', 'Soft books', 'Stroller blanket'],
        '6-12': ['Sippy cups', 'Feeding chair', 'Baby-proofing kit', 'Learning toys'],
    }

    seasonal_items = {
        'summer': ['Light cotton clothes', 'Sun hat', 'Baby sunscreen'],
        'winter': ['Thermal bodysuits', 'Woolen cap', 'Warm blankets'],
        'all': ['Cotton rompers', 'Diaper rash cream'],
    }

    preference_items = {
        'budget': ['Economy diaper pack', 'Basic baby monitor'],
        'travel': ['Portable changing mat', 'Travel bottle warmer'],
        'organic': ['Organic lotion', 'Organic cotton onesies'],
    }

    if request.method == "POST":
        age_range = request.POST.get('age_range')
        season = request.POST.get('season')
        preferences = request.POST.getlist('preferences')  # Multiple checkboxes

        # Start building checklist
        if age_range in base_items:
            checklist += base_items[age_range]

        if season in seasonal_items:
            checklist += seasonal_items[season]

        for pref in preferences:
            if pref in preference_items:
                checklist += preference_items[pref]

    context = {
        'checklist': checklist
    }
    return render(request, 'tools/newborn_checklist.html', context)


def baby_vaccine_reminder(request):
    schedule = []

    if request.method == "POST":
        dob_str = request.POST.get("dob")
        if dob_str:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

            vaccine_schedule = [
                ("BCG", 0, False),
                ("Hepatitis B1", 0, False),
                ("OPV-0", 0, False),
                ("DTaP-1", 42, False),
                ("Hepatitis B2", 42, False),
                ("OPV-1", 42, False),
                ("Hib-1", 42, False),
                ("Rotavirus-1", 42, False),
                ("PCV-1", 42, False),

                ("DTaP-2", 70, False),
                ("Hib-2", 70, False),
                ("Rotavirus-2", 70, False),
                ("PCV-2", 70, False),

                ("DTaP-3", 98, False),
                ("Hib-3", 98, False),
                ("Hepatitis B3", 98, False),
                ("Rotavirus-3", 98, False),
                ("PCV-3", 98, False),

                ("MMR-1", 270, False),
                ("Varicella", 365, False),
                ("Hepatitis A-1", 365, False),
                ("Typhoid Conjugate", 365, False),

                ("DTaP Booster", 540, False),
                ("MMR-2", 540, False),
                ("Hepatitis A-2", 540, False),

                ("Typhoid Booster", 1095, True),         # 3 years
                ("Influenza (Annual)", 1095, True),      # 3 years
                ("DTP Booster", 1825, False),            # 5 years
                ("Tdap/Td", 3650, False),                # 10 years
                ("HPV Vaccine", 3650, True),             # 10 years - Optional
            ]

            for name, days, is_optional in vaccine_schedule:
                schedule.append({
                    "name": name + (" (Optional)" if is_optional else ""),
                    "age_label": f"{days // 30} months" if days < 365 else f"{days // 365} years",
                    "date": dob + timedelta(days=days)
                })

    return render(request, "tools/vaccine_reminder.html", {"schedule": schedule})






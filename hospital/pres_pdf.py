from io import BytesIO
from urllib import response
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from doctor.models import Prescription
from doctor.models import  Prescription,Prescription_medicine,Prescription_test
from hospital.models import Patient
from datetime import datetime


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(html, content_type='text/html')
    return response




def prescription_pdf(request,pk):
 if request.user.is_patient:
    patient = Patient.objects.get(user=request.user)
    prescription = Prescription.objects.get(prescription_id=pk)
    prescription_medicine = Prescription_medicine.objects.filter(prescription=prescription)
    prescription_test = Prescription_test.objects.filter(prescription=prescription)
    # current_date = datetime.date.today()
    context={'patient':patient,'prescriptions':prescription,'prescription_test':prescription_test,'prescription_medicine':prescription_medicine}
    pres_html=render_to_pdf('prescription_pdf.html', context)
    if pres_html:
        return pres_html
    return HttpResponse("Not Found")

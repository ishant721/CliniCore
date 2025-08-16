from io import BytesIO
from urllib import response
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from .models import Report
from .models import  Report,Specimen,Test
from hospital.models import Patient
from datetime import datetime


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(html, content_type='text/html')
    return response




def report_pdf(request,pk):
 if request.user.is_patient:
    patient = Patient.objects.get(user=request.user)
    report = Report.objects.get(report_id=pk)
    specimen = Specimen.objects.filter(report=report)
    test = Test.objects.filter(report=report)
    # current_date = datetime.date.today()
    context={'patient':patient,'report':report,'test':test,'specimen':specimen}
    html_report=render_to_pdf('report_pdf.html', context)
    if html_report:
        return html_report
    return HttpResponse("Not Found")

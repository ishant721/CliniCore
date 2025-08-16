
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from doctor.models import Report, AutomatedAppointment
from doctor.appointment_automation import AppointmentAutomation

class Command(BaseCommand):
    help = 'Schedule follow-up appointments for completed lab reports'
    
    def handle(self, *args, **options):
        # Find reports completed in the last 24 hours that need follow-ups
        yesterday = timezone.now() - timedelta(days=1)
        
        # Get completed reports
        completed_reports = Report.objects.filter(
            status='completed',
            created_at__gte=yesterday
        )
        
        follow_ups_scheduled = 0
        
        for report in completed_reports:
            # Find the original appointment for this report
            try:
                # Assuming we can link report to appointment via patient and doctor
                from doctor.models import Appointment
                original_appointment = Appointment.objects.filter(
                    patient=report.patient,
                    doctor=report.doctor,
                    appointment_status='completed'
                ).order_by('-date').first()
                
                if original_appointment:
                    # Check if follow-up already scheduled
                    automated_apt = AutomatedAppointment.objects.filter(
                        original_appointment=original_appointment
                    ).first()
                    
                    if automated_apt and not automated_apt.follow_up_scheduled:
                        follow_up = AppointmentAutomation.schedule_follow_up(original_appointment)
                        if follow_up:
                            follow_ups_scheduled += 1
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Scheduled follow-up for {report.patient.name} with {report.doctor.name}'
                                )
                            )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error scheduling follow-up for report {report.report_id}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully scheduled {follow_ups_scheduled} follow-up appointments')
        )

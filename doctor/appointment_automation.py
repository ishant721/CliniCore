
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta, time
from .models import Doctor_Information, Appointment, DoctorSchedule, AutomatedAppointment
from hospital.models import Patient
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class AppointmentAutomation:
    
    @staticmethod
    def find_next_available_slot(doctor, preferred_date=None):
        """Find the next available appointment slot for a doctor"""
        if not preferred_date:
            preferred_date = timezone.now().date()
        
        # Look for available slots in the next 30 days
        for i in range(30):
            check_date = preferred_date + timedelta(days=i)
            day_name = check_date.strftime('%A').lower()
            
            try:
                schedule = DoctorSchedule.objects.get(
                    doctor=doctor, 
                    day_of_week=day_name, 
                    is_active=True
                )
                
                # Check how many appointments are already scheduled for this day
                existing_appointments = Appointment.objects.filter(
                    doctor=doctor,
                    date=check_date,
                    appointment_status__in=['pending', 'confirmed']
                ).count()
                
                if existing_appointments < schedule.max_patients:
                    # Find available time slot
                    available_time = AppointmentAutomation._find_time_slot(
                        doctor, check_date, schedule
                    )
                    if available_time:
                        return check_date, available_time
                        
            except DoctorSchedule.DoesNotExist:
                continue
        
        return None, None
    
    @staticmethod
    def _find_time_slot(doctor, date, schedule):
        """Find an available time slot within the doctor's schedule"""
        start_time = schedule.start_time
        end_time = schedule.end_time
        slot_duration = timedelta(minutes=30)  # 30-minute slots
        
        current_time = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        
        while current_time + slot_duration <= end_datetime:
            # Check if this time slot is available
            slot_taken = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=current_time.time(),
                appointment_status__in=['pending', 'confirmed']
            ).exists()
            
            if not slot_taken:
                return current_time.time()
            
            current_time += slot_duration
        
        return None
    
    @staticmethod
    def schedule_appointment(patient, doctor, appointment_type='consultation'):
        """Automatically schedule an appointment"""
        date, time_slot = AppointmentAutomation.find_next_available_slot(doctor)
        
        if not date or not time_slot:
            return None, "No available slots found"
        
        # Create the appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time_slot,
            appointment_status='confirmed',
            problem="Automated scheduling"
        )
        
        # Create automated appointment tracking
        AutomatedAppointment.objects.create(
            original_appointment=appointment,
            status='scheduled'
        )
        
        # Send confirmation email
        AppointmentAutomation.send_appointment_confirmation(appointment)
        
        return appointment, "Appointment scheduled successfully"
    
    @staticmethod
    def schedule_lab_appointment(original_appointment):
        """Schedule a lab appointment after doctor consultation"""
        try:
            automated_apt = AutomatedAppointment.objects.get(
                original_appointment=original_appointment
            )
            
            if not automated_apt.lab_appointment_scheduled:
                # Here you would integrate with lab scheduling system
                # For now, we'll mark it as scheduled
                automated_apt.lab_appointment_scheduled = True
                automated_apt.status = 'confirmed'
                automated_apt.save()
                
                # Send lab appointment notification
                AppointmentAutomation.send_lab_appointment_notification(original_appointment)
                
                return True
        except AutomatedAppointment.DoesNotExist:
            pass
        
        return False
    
    @staticmethod
    def schedule_follow_up(original_appointment):
        """Schedule follow-up appointment after lab results"""
        try:
            automated_apt = AutomatedAppointment.objects.get(
                original_appointment=original_appointment
            )
            
            if not automated_apt.follow_up_scheduled:
                # Schedule follow-up with the same doctor
                follow_up_date, follow_up_time = AppointmentAutomation.find_next_available_slot(
                    original_appointment.doctor
                )
                
                if follow_up_date and follow_up_time:
                    follow_up = Appointment.objects.create(
                        patient=original_appointment.patient,
                        doctor=original_appointment.doctor,
                        date=follow_up_date,
                        time=follow_up_time,
                        appointment_status='confirmed',
                        problem="Follow-up consultation - Lab results review"
                    )
                    
                    automated_apt.follow_up_appointment = follow_up
                    automated_apt.follow_up_scheduled = True
                    automated_apt.status = 'follow_up_needed'
                    automated_apt.save()
                    
                    # Send follow-up notification
                    AppointmentAutomation.send_follow_up_notification(follow_up)
                    
                    return follow_up
        except AutomatedAppointment.DoesNotExist:
            pass
        
        return None
    
    @staticmethod
    def send_appointment_confirmation(appointment):
        """Send appointment confirmation email"""
        subject = "Appointment Confirmed - HealthStack"
        patient_email = appointment.patient.email
        patient_name = appointment.patient.name
        doctor_name = appointment.doctor.name
        
        context = {
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'appointment_date': appointment.date,
            'appointment_time': appointment.time,
        }
        
        html_message = render_to_string('appointment_confirmation_mail.html', context)
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject, 
                plain_message, 
                'healthstack@gmail.com', 
                [patient_email], 
                html_message=html_message, 
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending confirmation email: {e}")
    
    @staticmethod
    def send_lab_appointment_notification(appointment):
        """Send lab appointment notification"""
        subject = "Lab Tests Scheduled - HealthStack"
        patient_email = appointment.patient.email
        patient_name = appointment.patient.name
        
        context = {
            'patient_name': patient_name,
            'doctor_name': appointment.doctor.name,
        }
        
        html_message = render_to_string('lab_appointment_mail.html', context)
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject, 
                plain_message, 
                'healthstack@gmail.com', 
                [patient_email], 
                html_message=html_message, 
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending lab notification email: {e}")
    
    @staticmethod
    def send_follow_up_notification(follow_up_appointment):
        """Send follow-up appointment notification"""
        subject = "Follow-up Appointment Scheduled - HealthStack"
        patient_email = follow_up_appointment.patient.email
        patient_name = follow_up_appointment.patient.name
        
        context = {
            'patient_name': patient_name,
            'doctor_name': follow_up_appointment.doctor.name,
            'appointment_date': follow_up_appointment.date,
            'appointment_time': follow_up_appointment.time,
        }
        
        html_message = render_to_string('follow-up-appointment-mail.html', context)
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject, 
                plain_message, 
                'healthstack@gmail.com', 
                [patient_email], 
                html_message=html_message, 
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending follow-up notification email: {e}")


from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def handle_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

def handle_500(request):
    """Custom 500 error handler"""
    logger.error(f"500 error occurred: {request.path}")
    return render(request, '500.html', status=500)

class ErrorHandlerMixin:
    """Mixin to add error handling to views"""
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {str(e)}")
            messages.error(request, "An error occurred. Please try again.")
            return self.handle_error(request, e)
    
    def handle_error(self, request, exception):
        """Override this method to customize error handling"""
        if request.is_ajax():
            return JsonResponse({'error': 'An error occurred'}, status=500)
        return render(request, 'error.html', {'error': str(exception)})

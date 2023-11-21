from django.http import Http404
from django.shortcuts import redirect, render

from customersatisfactionmetrics.forms.survey_form import SurveyForm
from customersatisfactionmetrics.models import Question, Response, Survey


def survey_view(request, survey_id=None, slug=None):
    # Fetch the survey by ID or slug
    if survey_id:
        survey = Survey.objects.get(pk=survey_id)
    elif slug:
        survey = Survey.objects.get(slug=slug)
    else:
        raise Http404("Survey not found")

    if request.method == 'POST':
        form = SurveyForm(request.POST, survey_id=survey_id, slug=slug)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if key.startswith('question_'):
                    question_id = int(key.split('_')[1])
                    question = Question.objects.get(pk=question_id)

                    # Determine response type based on the survey type
                    response_type = survey.survey_type

                    client_ip = get_client_ip(request)

                    response = Response(
                        user=request.user if request.user.is_authenticated else None,
                        question=question, 
                        text=value, 
                        response_type=response_type,
                        ip_address=client_ip,
                        user_agent=request.META.get('HTTP_USER_AGENT')
                    )
                    response.save()
            return redirect('thank_you')  # Redirect to a thank you page or similar
    else:
        form = SurveyForm(survey_id=survey_id, slug=slug)

    return render(request, 'survey_form.html', {'form': form, 'survey': survey})

def get_client_ip(request):
    """ Get the client's IP address from a Django request. """
    headers = [
        'X-REAL-IP',  # Alternative real IP header
        'CF-Connecting-IP',  # Cloudflare header
        'HTTP_X_FORWARDED_FOR', 
        'HTTP_CLIENT_IP',
        'HTTP_X_REAL_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_VIA',
    ]

    for header in headers:
        ip = request.META.get(header)
        if ip:
            # In the case of 'X-Forwarded-For', take the first IP in the list
            if header == 'HTTP_X_FORWARDED_FOR':
                ip = ip.split(',')[0]
            return ip.strip()

    return request.META.get('REMOTE_ADDR')  # Default to REMOTE_ADDR if none of the headers are present

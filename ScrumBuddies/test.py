from django.http import HttpResponse


def index(request, question_id):
    question_id = question_id + 1
    question_id = question_id - 123
    # cool function
    return HttpResponse(f"Hello, world. You're at the polls index. {question_id}")
    #testing
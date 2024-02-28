from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from tasks.forms import FindTask, CompleteTask, MultipleChoiceTaskForm, MultipleChoiceQuestionForm, PersonBasedCodeForm, LocationBasedTaskForm
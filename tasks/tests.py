# ------- Luke START -------

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from tasks.forms import *
from gamekeepers.forms import *

class TaskTesting(TestCase):
    def testMCQCompletion(self):
        # creates a client to be interacted and a test user
        client = Client()
        
        User.objects.create_superuser(username='testUser', password='testPassword', is_staff=True)
        # gets the user and the associated profile to check if the points have been updated
        createdUser = User.objects.last()
        createdProfile = createdUser.profile

        loginData = {
            'username' : 'testUser',
            'password' : 'testPassword'
        }
        response = client.post(reverse('login_user'), data=loginData)
        
        MCQinput = {
            'location' : 'Forum',
            'description' : 'Example Description',
            'question' : 'Example Question',
            'choice1' : 'A',
            'choice2' : 'B',
            'choice3' : 'C',
            'choice4' : 'D',
            'correct_answer' : '1',
            'points' : '10',
        }

        # creates the question from the test data
        form = MultipleChoiceTaskForm(MCQinput)
        createResponse = client.post(reverse('create_multiple_choice_question'), data = form.data)
        createdTask = MultipleChoiceChallenge.objects.last()

        # ensures that the number of points the profile stores is initially 0
        self.assertEquals(createdProfile.points, 0)
        # attempts to complete the question on the user's behalf
        responseOne = client.post(reverse('MCQchallenge', kwargs={'code': createdTask.code}), {'choice': '2'})
        createdProfile.refresh_from_db()
        # compares the number of points with the initial number of points
        self.assertEquals(createdProfile.points, 0)
        responseTwo = client.post(reverse('MCQchallenge', kwargs={'code': createdTask.code}), {'choice': '1'})
        createdProfile.refresh_from_db()
        # compares the number of points with the initial number of points
        self.assertEquals(createdProfile.points, 10)

    def testPBCCompletion(self):
        client = Client()
        User.objects.create_superuser(username='testUser', password='testPassword', is_staff=True)
        # gets the user and the associated profile to check if the points have been updated
        createdUser = User.objects.last()
        createdProfile = createdUser.profile

        loginData = {
            'username' : 'testUser',
            'password' : 'testPassword'
        }
        response = client.post(reverse('login_user'), data=loginData)

        PBCinput = {
            'name' : 'testName',
            'location' : 'testLocation',
            'expertise' : 'testExpertise',
            'points' : '10'
        }
        
        # creates the challenge from the test data
        form = PersonBasedCodeForm(PBCinput)
        creation = client.post(reverse('create_person_based_code'), data=form.data)
        createdTask = PersonBasedCodeChallenge.objects.last()

        # ensures that the number of points the profile stores is initially 0
        self.assertEquals(createdProfile.points, 0)
        # attempts to enter the code on the user's behalf
        responseOne = client.post(reverse('submit_code'), data={'code' : createdTask.code})
        createdProfile.refresh_from_db()
        # compares the number of points with the initial number of points
        self.assertEquals(createdProfile.points, 10)
        # attempts to enter the code on the user's behalf to make sure that they cannot enter the code again
        responseTwo = client.post(reverse('submit_code'), data={'code' : createdTask.code})
        createdProfile.refresh_from_db()
        # compares the number of points with the initial number of points to make sure that it has not increased
        self.assertEquals(createdProfile.points, 10)
# ------- Luke END -------
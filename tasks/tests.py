# ------- Luke START -------

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from tasks.forms import FindTask, CompleteTask, MultipleChoiceTaskForm, MultipleChoiceQuestionForm, PersonBasedCodeForm, LocationBasedTaskForm, MultipleChoiceChallenge

class TaskTesting(TestCase):
    def testMCQCreation(self):
        # creates a client to be interacted and a test user
        client = Client()
        test_user = User.objects.create_user(username='testUser', password='testPassword', is_staff=True)

        loginData = {
            'username' : 'testUser',
            'password' : 'testPassword'
        }
        response = client.post(reverse('login_user'), data=loginData)

        # gets the initial number of multiple choice questions stored in the database
        initialMCQs = MultipleChoiceChallenge.objects.count()

        # test data for the multiple choice questions
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

        # attempts to submit the form of the questions and validates said form
        form = MultipleChoiceTaskForm(MCQinput)
        self.assertTrue(form.is_valid(), form.errors)
        # attempts to add the question into the data base using the form data
        response = client.post(reverse('create_multiple_choice_question'), data = form.data)
        # compares the number of questions in the database with what was initially in there
        self.assertEquals(MultipleChoiceChallenge.objects.count(), initialMCQs + 1)

        # gets the task that has just been created and checks the attributes are correct
        createdTask = MultipleChoiceChallenge.objects.last()
        self.assertEquals(createdTask.question, 'Example Question')


    def testMCQDeletion(self):
        # creates a client to be interacted and a test user
        client = Client()
        
        test_user = User.objects.create_user(username='testUser', password='testPassword', is_staff=True)
        createdUser = User.objects.last()

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

        # since the tasks are added this does not need to be tested again
        form = MultipleChoiceTaskForm(MCQinput)
        initialResponse = client.post(reverse('create_multiple_choice_question'), data = form.data)

        # gets the number of questions once the test question has been added
        initialMCQs = MultipleChoiceChallenge.objects.count()
        createdTask = MultipleChoiceChallenge.objects.last()
        # attempts to delete the question that has just been created
        newResponse = client.post(reverse('delete_multiple_choice_question', kwargs={'question_id': createdTask.id}))

        # compares the number of questions in the database to what was in there before the attempted deletion
        self.assertEquals(MultipleChoiceChallenge.objects.count(), initialMCQs - 1)

    def testMCQCompletion(self):
        # creates a client to be interacted and a test user
        client = Client()
        
        test_user = User.objects.create_user(username='testUser', password='testPassword', is_staff=True)
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
        responseOne = client.post(reverse('MCQchallenge', kwargs={'code': createdTask.code}), {'choice': '1'})
        createdProfile.refresh_from_db()
        # compares the number of points with the initial number of points
        self.assertEquals(createdProfile.points, 10)
        responseTwo = client.post(reverse('MCQchallenge', kwargs={'code': createdTask.code}), {'choice': '2'})
        createdProfile.refresh_from_db()
        # compares the number of points with the initial number of points
        self.assertEquals(createdProfile.points, 10)
        
# ------- Luke END -------
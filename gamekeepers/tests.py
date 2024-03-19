from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from gamekeepers.forms import *
from tasks.forms import *

class TaskManagementTesting(TestCase):
    def testMCQCreationAndDeletion(self):
        # creates a client to be interacted and a test user
        client = Client()
        User.objects.create_superuser(username='testUser', password='testPassword')

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
        creation = client.post(reverse('create_multiple_choice_question'), data = form.data)
        self.assertEqual(creation.status_code, 302)
        # compares the number of questions in the database with what was initially in there
        self.assertEquals(MultipleChoiceChallenge.objects.count(), initialMCQs + 1)

        # gets the task that has just been created and checks the attributes are correct
        createdTask = MultipleChoiceChallenge.objects.last()
        self.assertEquals(createdTask.question, 'Example Question')
        
        # attempts to delete the question that has just been created
        deletion = client.post(reverse('delete_multiple_choice_question', kwargs={'question_id': createdTask.id}))
        self.assertEqual(creation.status_code, 302)
        # ensures that the number of questions in the database is what it originally was
        self.assertEquals(MultipleChoiceChallenge.objects.count(), initialMCQs)

    def testPBCCreationAndDeletion(self):
        client = Client()
        User.objects.create_superuser(username='testUser', password='testPassword')

        loginData = {
            'username' : 'testUser',
            'password' : 'testPassword'
        }
        response = client.post(reverse('login_user'), data=loginData)

        initialPBCs = PersonBasedCodeChallenge.objects.count()

        PBCinput = {
            'name' : 'testName',
            'location' : 'testLocation',
            'expertise' : 'testExpertise',
            'points' : '100'
        }
        
        form = PersonBasedCodeForm(PBCinput)
        self.assertTrue(form.is_valid(), form.errors)

        creation = client.post(reverse('create_person_based_code'), data=form.data)
        self.assertEqual(creation.status_code, 302)
        self.assertEquals(PersonBasedCodeChallenge.objects.count(), initialPBCs + 1)

        createdTask = PersonBasedCodeChallenge.objects.last()
        self.assertEquals(createdTask.name, 'testName')

        deletion = client.post(reverse('delete_person_based_code', kwargs={'code_id': createdTask.id}))
        self.assertEqual(deletion.status_code, 302)



class AccountManagementTesting(TestCase):
    def testRemoveAccount(self):
        client = Client()
        User.objects.create_superuser(username='testAdmin', password='testPassword')
        User.objects.create_user(username='testUser', password='testPassword')

        loginData = {
            'username' : 'testAdmin',
            'password' : 'testPassword'
        }
        response = client.post(reverse('login_user'), data=loginData)

        initialAccounts = User.objects.count()
        createdUser = User.objects.last()

        deletion = client.post(reverse('remove_account', kwargs={'username': createdUser.username}))
        self.assertEquals(User.objects.count(), initialAccounts - 1)

    def testCreateGamekeeper(self):
        client = Client()
        User.objects.create_superuser(username='testAdmin', password='testPassword')

        loginData = {
            'username' : 'testAdmin',
            'password' : 'testPassword'
        }
        response = client.post(reverse('login_user'), data=loginData)

        testUserData = {
            'username' : 'testUser',
            'password1' : 'testPassword',
            'password2' : 'testPassword',
        }

        form = RegisterGamekeeperForm(testUserData)
        self.assertTrue(form.is_valid(), form.errors)

        creation = client.post(reverse('create_gamekeeper'), data=form.data)
        self.assertEqual(creation.status_code, 302)

        createdUser = User.objects.last()
        self.assertTrue(createdUser.is_superuser)
        self.assertEquals(createdUser.username, 'testUser')
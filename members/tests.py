from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from members.forms import RegisterUserForm, UpdateUserForm, addPronounsForm, bioForm

# ------- CODING BY WILLIAM SMITH -------
class UserAuthenticationTesting(TestCase):
    def testUserCreation(self):
        client = Client() # <- client is like a fake website we can interact with 
        
        initialUserCount = User.objects.count()

        userDataForm ={ #creates details for a fake user for tests 
            'username': 'testUser',
            'password1': 'testPassword',
            'password2' : 'testPassword'
        }
        form = RegisterUserForm(userDataForm)
        self.assertTrue(form.is_valid(), form.errors)

        response = client.post(reverse('register_user'), data = form.data) #asks the client to create the user

        self.assertEqual(User.objects.count(), initialUserCount + 1) # checks the user count has gone up by one
        
        createdUser = User.objects.last() # stores new user

        self.assertEquals(createdUser.username, 'testUser') #Checks the username is correct
        self.assertEquals(response.status_code, 302) # Checks the status code
        self.assertRedirects(response, reverse('profile_user'))#checks user is redirected to user profile page


    def testUserLogin(self):
        client = Client()

        test_user = User.objects.create_user(username='testUser', password='testPassword') #creates new user

        loginData = { #data for login to user
            'username' : 'testUser',
            'password' : 'testPassword'
        }
        response = client.post(reverse('login_user'), data=loginData) #logs in
        self.assertEquals(response.status_code, 302) #checks login is succesful

    def testUserLogout(self): #same as login but logs out instead and tests if hidden pages can be accessed
        client = Client()
        User.objects.create_user(username='testUser', password='testPassword')
        loginData = {
            'username' : 'testUser',
            'password' : 'testPassword'
        }
        client.post(reverse('login_user'), data=loginData)

        response = client.post(reverse('logout_user'))

        self.assertEquals(response.status_code, 302)

# ------- END -------

# ------- CODING BY LUKE HALES -------
    def testUserDelete(self):
        client = Client()
        User.objects.create_user(username='testUser', password='testPassword')
        initialUserCount = User.objects.count()
        loginData = {
            'username' : 'testUser',
            'password' : 'testPassword'
        }
        client.post(reverse('login_user'), data=loginData)

        response = client.post(reverse('delete_user'))

        self.assertEquals(User.objects.count(), initialUserCount - 1)

    def testUserUpdate(self):
        client = Client()
        User.objects.create_user(username='testUser', password='testPassword')
        createdUser = User.objects.last()
        createdProfile = createdUser.profile
        loginData = {
            'username' : 'testUser',
            'password' : 'testPassword'
        }

        client.post(reverse('login_user'), data=loginData)

        updatedUserData = {
            'username' : 'testUser',
            'first_name' : 'John',
            'last_name' : 'Doe'
        }
        updatedPronounData = {
            'pronouns' : 'He/Him'
        }
        updatedBioData = {
            'bio' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
        }

        self.assertEquals(createdUser.first_name, '')
        self.assertEquals(createdUser.last_name, '')
        self.assertEquals(createdProfile.pronouns, None)
        self.assertEquals(createdProfile.bio, None)

        userForm = UpdateUserForm(updatedUserData, instance=createdUser)
        self.assertTrue(userForm.is_valid(), userForm.errors)
        pronounForm = addPronounsForm(updatedPronounData, instance=createdProfile)
        self.assertTrue(pronounForm.is_valid(), pronounForm.errors)
        BioForm = bioForm(updatedBioData, instance=createdProfile)
        self.assertTrue(BioForm.is_valid(), bioForm.errors)

        userResponse = client.post(reverse('update_user'), data = userForm.data)
        self.assertEquals(userResponse.status_code, 302)
        self.assertEquals(createdUser.first_name, 'John')
        self.assertEquals(createdUser.last_name, 'Doe')

        pronounResponse = client.post(reverse('update_user'), data = pronounForm.data)
        self.assertEquals(pronounResponse.status_code, 200)
        self.assertEquals(createdProfile.pronouns, 'He/Him')

        bioResponse = client.post(reverse('update_user'), data = BioForm.data)
        self.assertEquals(bioResponse.status_code, 200)
        self.assertEquals(createdProfile.bio, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.')

# ------- END -------

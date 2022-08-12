from django.test import TestCase, Client
from django.db.models import Max

from .models import Post, Like, Follower, User

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        # create users
        u1 = User.objects.create(username="erwsmith", email="erwsmith@gmail.com")
        u2 = User.objects.create(username="user2", email="user2@gmail.com")
        u3 = User.objects.create(username="user3", email="user3@gmail.com")
        # create posts
        p1 = Post.objects.create(user=u1, body="Post A", id=1)
        p2 = Post.objects.create(user=u2, body="Post B", id=2)
        # create likes
        Like.objects.create(post=p1, user=u1, liked=True)
        Like.objects.create(post=p2, user=u2, liked=True)
        Like.objects.create(post=p2, user=u1, liked=True)
        Like.objects.create(post=p2, user=u3, liked=True)
        # create followers
        f1 = Follower.objects.create(user=u1) 
        f1.following.add(u2)
        f2 = Follower.objects.create(user=u2)
        f2.following.add(u1)
        f3 = Follower.objects.create(user=u3)
        f3.following.add(u1)
        f3.following.add(u2)

    def test_likes_count_1(self):
        p = Post.objects.get(pk=1)
        self.assertEqual(p.likes.count(), 1)
    
    def test_likes_count_2(self):
        p = Post.objects.get(pk=2)
        self.assertEqual(p.likes.count(), 3)
    
    def test_valid_follower(self):
        u1 = User.objects.get(username="erwsmith")
        f = Follower.objects.get(user=u1)
        self.assertTrue(f.is_valid_follower())

    # Count total number of followers
    def test_followers_count_0(self):
        self.assertEqual(Follower.objects.count(), 3)
    
    def test_followers_count_1(self):
        u = User.objects.get(username="erwsmith")
        self.assertEqual(u.followers.count(), 2)

    def test_followers_count_2(self):
        u = User.objects.get(username="user2")
        self.assertEqual(u.followers.count(), 2)

    def test_followers_count_3(self):
        u = User.objects.get(username="user3")
        self.assertEqual(u.followers.count(), 0)

    def test_following_count_1(self):
        u1 = User.objects.get(username="erwsmith")
        f1 = Follower.objects.get(user=u1).following.count()
        self.assertEqual(f1, 1)

    def test_following_count_2(self):
        u2 = User.objects.get(username="user2")
        f2 = Follower.objects.get(user=u2).following.count()
        self.assertEqual(f2, 1)

    def test_following_count_3(self):
        u3 = User.objects.get(username="user3")
        f3 = Follower.objects.get(user=u3).following.count()
        self.assertEqual(f3, 2)

    # is user2 following erwsmith? True
    def test_following_0(self):
        active_user = User.objects.get(username="user2")
        u1 = User.objects.get(username="erwsmith")
        active_user_as_follower = Follower.objects.get(user=active_user)
        self.assertTrue(u1 in active_user_as_follower.following.all())

    # is erwsmith following user2? True
    def test_following_1(self):
        active_user = User.objects.get(username="erwsmith")
        u2 = User.objects.get(username="user2")
        active_user_as_follower = Follower.objects.get(user=active_user)
        self.assertTrue(u2 in active_user_as_follower.following.all())

    # is user3 following erwsmith and user2? True
    def test_following_2(self):
        active_user = User.objects.get(username="user3")
        u1 = User.objects.get(username="erwsmith")
        u2 = User.objects.get(username="user2")
        active_user_as_follower = Follower.objects.get(user=active_user)
        self.assertTrue(u1 in active_user_as_follower.following.all())
        self.assertTrue(u2 in active_user_as_follower.following.all())

    # is erwsmith following and user3? False
    def test_following_3(self):
        active_user = User.objects.get(username="erwsmith")
        u3 = User.objects.get(username="user3")
        active_user_as_follower = Follower.objects.get(user=active_user)
        self.assertFalse(u3 in active_user_as_follower.following.all())


    # def test_index(self):
    #     c = Client()
    #     response = c.get("/flights/")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context["flights"].count(), 3)
    
    # def test_valid_flight_page(self):
    #     a1 = Airport.objects.get(code="AAA")
    #     f = Flight.objects.get(origin=a1, destination=a1)

    #     c = Client()
    #     response = c.get(f"/flights/{f.id}")
    #     self.assertEqual(response.status_code, 200)

    # def test_flight_page_passengers(self):
    #     f = Flight.objects.get(pk=1)
    #     p = Passenger.objects.create(first="Alice", last="Adams")
    #     f.passengers.add(p)
        
    #     c = Client()
    #     response = c.get(f"/flights/{f.id}")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context["passengers"].count(), 1)

    # def test_flight_page_non_passengers(self):
    #     f = Flight.objects.get(pk=1)
    #     p = Passenger.objects.create(first="Alice", last="Adams")
        
    #     c = Client()
    #     response = c.get(f"/flights/{f.id}")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context["non_passengers"].count(), 1)


    # def test_invalid_flight_page(self):
    #     max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

    #     c = Client()
    #     response = c.get(f"/flights/{max_id + 1}")
    #     self.assertEqual(response.status_code, 404)
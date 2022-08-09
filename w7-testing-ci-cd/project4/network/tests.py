from django.test import TestCase, Client
from django.db.models import Max

from .models import Post, Like, Follower, User

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        # create users
        u1 = User.objects.create(username="erwsmith", email="erwsmith@gmail.com")
        u2 = User.objects.create(username="user2", email="user2@gmail.com")
        # create posts
        p1 = Post.objects.create(user=u1, body="Post A", id=1)
        p2 = Post.objects.create(user=u2, body="Post B", id=2)
        # create likes
        Like.objects.create(post=p1, user=u1, liked=True)
        Like.objects.create(post=p2, user=u2, liked=True)
        Like.objects.create(post=p2, user=u1, liked=True)
        # create followers
        f1 = Follower.objects.create(user=u1) 
        f1.following.add(u2)
        f2 = Follower.objects.create(user=u2)
        f2.following.add(u1)

    def test_likes_count_1(self):
        p = Post.objects.get(pk=1)
        self.assertEqual(p.likes.count(), 1)
    
    def test_likes_count_2(self):
        p = Post.objects.get(pk=2)
        self.assertEqual(p.likes.count(), 2)

    def followers_count(self):
        p = User.objects.get(username="erwsmith")
        self.assertEqual(p.followers.count(), 1)

    # def test_valid_flight(self):
    #     a1 = Airport.objects.get(code="AAA")
    #     a2 = Airport.objects.get(code="BBB")
    #     f = Flight.objects.get(origin=a1, destination=a2, duration=100)
    #     self.assertTrue(f.is_valid_flight())
    
    # def test_invalid_flight_destination(self):
    #     a1 = Airport.objects.get(code="AAA")
    #     f = Flight.objects.get(origin=a1, destination=a1)
    #     self.assertFalse(f.is_valid_flight())

    # def test_invalid_flight_duration(self):
    #     a1 = Airport.objects.get(code="AAA")
    #     a2 = Airport.objects.get(code="BBB")
    #     f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
    #     self.assertFalse(f.is_valid_flight())

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
__author__ = 'Jableader'

from django.test import TestCase
import test_suite
from golfsite import models

class TestTestingFramework(TestCase):

    def test_newWithTestData(self):
        model = test_suite.new(models.Sponsor) #Sponsor is the simplest
        self.assertIsNotNone(model.name)
        self.assertIsNotNone(model.website)
        self.assertIsNotNone(model.logo)

    def test_newWithDependancies(self):
        model = test_suite.new(models.Question)
        self.assertIsNotNone(model.sponsor)
        self.assertIsNotNone(model.sponsor.name)

    def test_newWithOptions(self):
        sponsor = test_suite.new(models.Sponsor, name="MickySoft")
        question = test_suite.new(models.Question, sponsor=sponsor)
        self.assertEqual("MickySoft", question.sponsor.name)

    def test_user_dependancy(self):
        self.assertIsNotNone(test_suite.new(models.Profile).user)
from rest_framework.test import APITestCase
from django.urls import reverse
from .views import *
from django.http import HttpRequest

class AssertDataChecker():

    def get_data_by_name(self):
        return [{
        "id": 8661032861909884224,
        "url": "http://127.0.0.1:8000/api/match/8661032861909884224",
        "name": "Real Madrid vs Barcelona",
        "start_time": "2018-05-21T05:30:00Z"
    }]

    def get_data_by_ordering(self):
        return [
        {
        "id": 3451032861909885675,
        "url": "http://127.0.0.1:8000/api/match/3451032861909885675",
        "name": "Sevilla vs Valencia",
        "start_time": "2015-10-10T12:30:00Z"
    },
    {
        "id": 2121032861909885786,
        "url": "http://127.0.0.1:8000/api/match/2121032861909885786",
        "name": "Eiber vs Espanyol",
        "start_time": "2017-01-05T09:30:00Z"
    },
    {
        "id": 8661032861909884224,
        "url": "http://127.0.0.1:8000/api/match/8661032861909884224",
        "name": "Real Madrid vs Barcelona",
        "start_time": "2018-05-21T05:30:00Z"
    },
    {
        "id": 3211032861909885564,
        "url": "http://127.0.0.1:8000/api/match/3211032861909885564",
        "name": "Manchester United vs Chelesa",
        "start_time": "2020-03-15T06:30:00Z"
    },
    {
        "id": 3211032861909885654,
        "url": "http://127.0.0.1:8000/api/match/3211032861909885654",
        "name": "Manchester City vs Arsenal",
        "start_time": "2020-09-10T01:30:00Z"
    }
        ]


class TestSetUp(APITestCase):

    def setUp(self):
        self.listmatch_url = reverse('listmatch')
        self.match_id = '3451032861909885675'
        self.match_url = reverse('match',kwargs={'id':self.match_id})
        self.request = HttpRequest()
        self.request.method = 'get'

    def test_listview_all_matches(self):
        """test for list view of all matches"""
        res = self.client.get(self.listmatch_url)
        self.assertEqual(res.status_code, 200)

    def test_get_match_details(self):
        """test for single match data"""
        res = self.client.get(self.match_url)
        self.assertEqual(res.status_code, 200)

    def test_get_match_details_by_name(self):
        """test for getting data by name"""
        kwargs = {"name": "Real Madrid vs Barcelona"}
        res = self.client.get(retriveMatch(self.request,**kwargs))
        return_val = res[0]['name']
        check_val = AssertDataChecker().get_data_by_name()[0]['name']
        # import pdb
        # pdb.set_trace()
        self.assertEqual(return_val, check_val)

    def test_get_match_details_by_ordering(self):
        """test for getting data by sport and ordering"""
        kwargs = {"sport": "football", "ordering": "start_time"}
        res = self.client.get(retriveMatch(self.request,**kwargs))
        return_val = res[0]['start_time']
        check_val = AssertDataChecker().get_data_by_name()[0]['start_time']
        self.assertEqual(return_val, check_val)


if __name__ == "__main__":
    unittest.main()

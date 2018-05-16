from django.test import TestCase, Client
from .models import Doctor, Review
from datetime import datetime
from json import loads



class LivesearchAPI(TestCase):

    def setUp(self):
        Doctor.objects.create(name="Иван", second_name='Хартман', third_name='Алексеев', birth_date=datetime.now(), phone='+375291234567')
        Doctor.objects.create(name="Алексей", second_name='Прокофьев', third_name='Максимович', birth_date=datetime.now(), phone='+375291234567')
        Doctor.objects.create(name="Иван", second_name='Гордон', third_name='Сергеевич', birth_date=datetime.now(), phone='+375291234567')
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')


    def test_normal_request_second_name(self):
        r = self.c.get('/doctors/api/livesearch', {'q': 'Хар'})
        data = loads(r.content)

        self.assertEqual(1, len(data))
        self.assertEqual(Doctor.objects.get(second_name='Хартман').id, data[0]['id'])

    def test_normal_request_name(self):
        r = self.c.get('/doctors/api/livesearch', {'q': 'Иван'})
        data = loads(r.content)

        self.assertEqual(2, len(data))
        self.assertEqual(Doctor.objects.get(second_name='Хартман').id, data[0]['id'])
        self.assertEqual(Doctor.objects.get(second_name='Гордон').id, data[1]['id'])

    def test_normal_request_name_plus_second_name_letter(self):
        r = self.c.get('/doctors/api/livesearch', {'q': 'Иван Г'})
        data = loads(r.content)

        self.assertEqual(1, len(data))
        self.assertEqual(Doctor.objects.get(second_name='Гордон').id, data[0]['id'])

    def test_normal_request_one_letter(self):
        r = self.c.get('/doctors/api/livesearch', {'q': 'а'})
        data = loads(r.content)

        self.assertEqual(3, len(data))
        self.assertEqual(Doctor.objects.get(second_name='Хартман').id, data[0]['id'])
        self.assertEqual(Doctor.objects.get(second_name='Прокофьев').id, data[1]['id'])
        self.assertEqual(Doctor.objects.get(second_name='Гордон').id, data[2]['id'])

    def test_english_letters_plus_unused_parameter(self):
        r = self.c.get('/doctors/api/livesearch', {'q': 'XY', 'foo': 'bar'})
        data = loads(r.content)

        self.assertEqual(0, len(data))

    def test_no_parameters(self):
        r = self.c.get('/doctors/api/livesearch')
        data = loads(r.content)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing or invalid parameter')


class GetAppointmentDateInfoAPI(TestCase):

    def setUp(self):
        Doctor.objects.create(name="Иван", second_name='Хартман', third_name='Алексеев', birth_date=datetime.now(), phone='+375291234567')
        Doctor.objects.create(name="Алексей", second_name='Прокофьев', third_name='Максимович', birth_date=datetime.now(), phone='+375291234567')
        Doctor.objects.create(name="Иван", second_name='Гордон', third_name='Сергеевич', birth_date=datetime.now(), phone='+375291234567')
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')


    def test_normal_request(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = self.c.get('/doctors/api/get_appointment_date_info', {'doc_id': 1, 'date': '15 may, 2018'})
        data = loads(r.content)

        self.assertNotIn('error', data)
        self.assertTrue((all([v for k, v in data.items()])))

    def test_no_date_parameter(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = self.c.get('/doctors/api/get_appointment_date_info', {'doc_id': 2})
        data = loads(r.content)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing or invalid date parameter')

    def test_invalid_date_parameter(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = self.c.get('/doctors/api/get_appointment_date_info', {'doc_id': 2})
        data = loads(r.content)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing or invalid date parameter')

    def test_no_doc_id_parameter(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = self.c.get('/doctors/api/get_appointment_date_info', {'date': '15 may, 2018'})
        data = loads(r.content)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing or invalid doc_id parameter')

    def test_invalid_doc_id_parameter(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = self.c.get('/doctors/api/get_appointment_date_info', {'doc_id': 'kkk', 'date': '15 may, 2018'})
        data = loads(r.content)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing or invalid doc_id parameter')

    def test_non_existent_doc_id(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = self.c.get('/doctors/api/get_appointment_date_info', {'doc_id': 5, 'date': '15 may, 2018'})
        data = loads(r.content)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Doctor not found')

    def test_post_request(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        r = self.c.post('/doctors/api/get_appointment_date_info', {'doc_id': 5, 'date': '15 may, 2018'})
        data = loads(r.content)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'get_appointment_date_info accepts only GET requests')


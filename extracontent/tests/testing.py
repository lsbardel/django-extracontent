import os
from django.test import TestCase

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

from extracontent import content
from extracontent.tests.models import MainModelForm, ExtraData1, ExtraData2


class TestExtraContent(TestCase):
    
    def get_form(self, data = None, instance = None):
        return MainModelForm(data = data, instance = instance)
    
    def testAddWithNoExtraContent(self):
        '''Add a new equity instrument. Testing the all process.'''
        data = {}
        form = self.get_form(data = data)
        self.assertFalse(form.is_valid())
        cf   = form.content_form()
        self.assertTrue(cf is None)
        data.update({'name':'Luca'})
        form = self.get_form(data = data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.content_form() is None)
        elem = form.save()
        self.assertTrue(elem.id)
        self.assertTrue(elem.extra_content() is None)
        
        
    def testAddWithExtraContent(self):
        '''Add a new equity instrument. Testing the all process.'''
        data = {'content_type':content('extradata1').id}
        form = self.get_form(data = data)
        self.assertFalse(form.is_valid())
        cf   = form.content_form()
        self.assertTrue(cf)
        html = cf.as_table()
        self.assertTrue('id_description' in html)
        data.update({'name':'Luca'})
        form = self.get_form(data = data)
        self.assertFalse(form.is_valid())
        data.update({'description':'this is a test'})
        form = self.get_form(data = data)
        self.assertTrue(form.is_valid())
        elem = form.save()
        self.assertTrue(elem.id)
        self.assertTrue(isinstance(elem.extra_content(),ExtraData1))
        self.assertTrue(elem.extra_content().id)
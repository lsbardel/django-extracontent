import os
from datetime import date

os.environ['DJANGO_SETTINGS_MODULE'] = 'extracontent.tests.settings'
from django.conf import settings
from django.test import TestCase

from extracontent import content
from extracontent.tests.models import MainModel, MainModel2, ExtraData1, ExtraData2
from extracontent.tests.models import MainModelForm, MainModelForm2


class TestExtraContent(TestCase):
    
    def get_form(self, data = None, instance = None, one2one = False):
        if one2one:
            return MainModelForm2(data = data, instance = instance)
        else:
            return MainModelForm(data = data, instance = instance)
    
    def _AddWithNoExtraContent(self, one2one = False):
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
        
    def _AddWithExtraContent(self, one2one = False):
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
        
    def _EditNoContent2Content(self, one2one = False):
        '''Add a new equity instrument. Testing the all process.'''
        elem = self.get_form(one2one = one2one,
                             data = {'name':'Luca'}).save()
        self.assertTrue(elem.id)
        self.assertTrue(elem.extra_content() is None)
        self.assertEqual(elem.name,'Luca')
        form = self.get_form(one2one = one2one,
                             instance = elem,
                             data = {'name':'Joshua',
                                     'content_type':content('extradata2').id,
                                     'dt':date.today()})
        self.assertTrue(form.is_valid())
        elem2 = form.save()
        self.assertEqual(elem.id,elem2.id)
        elem = MainModel.objects.get(id = elem.id)
        self.assertEqual(elem.name, 'Joshua')
        self.assertTrue(isinstance(elem.extra_content(),ExtraData2))
        self.assertTrue(elem.extra_content().id)
    
    def _EditContent2NoContent(self, one2one = False):
        '''Add a new equity instrument. Testing the all process.'''
        elem = self.get_form(one2one = one2one,
                             data = {'name':'Luca',
                                     'content_type':content('extradata2').id,
                                     'dt':date.today()}).save()
        self.assertTrue(elem.id)
        self.assertTrue(isinstance(elem.extra_content(),ExtraData2))
        self.assertEqual(elem.name,'Luca')
        form = self.get_form(one2one = one2one,
                             instance = elem,
                             data = {'name':'Joshua',
                                     'dt':date.today(),
                                     'content_type':''})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.content_form() is None)
        elem2 = form.save()
        self.assertEqual(elem.id,elem2.id)
        elem = MainModel.objects.get(id = elem.id)
        self.assertEqual(elem.name, 'Joshua')
        self.assertTrue(elem.extra_content() is None)
        
    def _EditContent2Content(self, one2one = False):
        '''Add a new equity instrument. Testing the all process.'''
        elem = self.get_form(one2one = one2one,
                             data = {'name':'Luca',
                                     'content_type':content('extradata2').id,
                                     'dt':date.today()}).save()
        self.assertTrue(elem.id)
        self.assertTrue(isinstance(elem.extra_content(),ExtraData2))
        self.assertEqual(elem.name,'Luca')
        form = self.get_form(one2one = one2one,
                             instance = elem,
                             data = {'name':'Joshua',
                                     'description':'bla bla bla',
                                     'content_type':content('extradata1').id})
        self.assertTrue(form.is_valid())
        cf = form.content_form()
        self.assertTrue(cf)
        elem2 = form.save()
        self.assertEqual(elem.id,elem2.id)
        elem = MainModel.objects.get(id = elem.id)
        self.assertEqual(elem.name, 'Joshua')
        self.assertTrue(isinstance(elem.extra_content(),ExtraData1))
        
    def _Signal(self, one2one = False):
        data = {'name':'Luca',
                'content_type':content('extradata2').id,
                'dt':date.today()}
        elem = self.get_form(data = data, one2one = one2one).save()
        obj = elem.extra_content()
        self.assertTrue(isinstance(obj,ExtraData2))
        elem.delete()
        N = ExtraData2.objects.filter(id = obj.id).count()
        if one2one:
            self.assertEqual(N,0)
        else:
            self.assertEqual(N,1)        
        
    def testAddWithNoExtraContent(self):
        self._AddWithNoExtraContent()
        self._AddWithNoExtraContent(one2one = True)
        
    def testEditContent2NoContent(self):
        self._EditContent2NoContent()
        self._EditContent2NoContent(one2one = True)
        
    def testEditNoContent2Content(self):
        self._EditNoContent2Content()
        self._EditNoContent2Content(one2one = True)
        
    def testEditContent2Content(self):
        self._EditContent2Content()
        self._EditContent2Content(one2one = True)
        
    def testSignal(self):
        self._Signal()
        self._Signal(one2one = True)
        
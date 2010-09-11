
A django abstract model and form for handling extra content in a model.



Let's say we have a model ``MyData`` which can refers to different underlying
data types::
	
	from django.db import models
	from extracontent.models import ExtraContent
	from extracontent.forms import ExtraContentForm
	
	class DataModel1(models.Model):
		value = models.TextField()
		
	class DataModel2(models.Model):
		dt = models.DateField()
		
	class MyData(ExtraContent):
		 name = models.CharField(max_length = 20)
	
	class MyDataForm(ExtraContentForm):
		class Meta:
		model = MyData
	
	
Then we can do this::

	>>> from extracontent import content
	>>> elem = MyDataForm({'content_type':content('datamodel1'),
	... 'value':'this is a test', name:'a data object'}).save()
	>>> elem.extra_content()
	<DataModel1: DataModel1 object>
	>>> elem.extra_content().value
	'this is a test'
	
	

Running Tests
====================
Once installed::

	>>>from extracontent.tests import run
	>>>run()
	
or from within the ``tests`` directory::

	python runtests.py
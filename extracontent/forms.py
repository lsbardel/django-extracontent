from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory


class ExtraContentForm(forms.ModelForm):
    '''This model form handles extra content from a content type field
    The model must be an instance of :class:`ExtraContentModel`.
    '''    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance',None)
        if instance:
            initial_extra = instance.extra_content()
        else:
            initial_extra = None
        super(ExtraContentForm,self).__init__(*args, **kwargs)
        kwargs['instance'] = initial_extra
        self._args = args
        self._kwargs = kwargs
        
    def is_valid(self):
        vi = super(ExtraContentForm,self).is_valid()
        cf = self.content_form()
        if cf:
            vi = cf.is_valid() and vi
            if vi:
                self.cleaned_data.update(cf.cleaned_data)
            else:
                self.errors.update(cf.errors)
        return vi
    
    def content_form(self):
        instance = self.instance
        ct  = instance.content_type
        #data = dict(self.data.items())
        #ctt  = data.get('content_type',self.initial.get('content_type',None))
        #if ctt:
        #    ct = ContentType.objects.get(id = int(ctt))
        if ct:
            #pre_content   = kwargs.pop('instance',None)
            content_model = ct.model_class()
            #if isinstance(pre_content,content_model):
            #    kwargs['instance'] = pre_content 
            content_form  = modelform_factory(content_model)
            return content_form(*self._args, **self._kwargs)
        else:
            return None
    
    def save(self, commit = True):
        obj = super(ExtraContentForm,self).save(commit = False)
        cf = self.content_form()
        if cf:
            obj.object_id = cf.save(commit = True).id
        else:
            obj.object_id = 0
        if commit:
            return super(ExtraContentForm,self).save(commit = commit)
        else:
            return obj
    

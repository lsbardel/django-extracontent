from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory


class ExtraContentForm(forms.ModelForm):
    '''This model form handles extra content from a content type field
    The model must be an instance of :class:`ExtraContentModel`.
    '''    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance',None)
        super(ExtraContentForm,self).__init__(*args, **kwargs)
        instance = instance or self.instance
        kwargs['instance'] = instance.extra_content()
        self.content_form = self.get_content_form(*args, **kwargs)
        
    def is_valid(self):
        vi = super(ExtraContentForm,self).is_valid()
        if self.content_form:
            vi = self.content_form.is_valid() and vi
            if vi:
                self.cleaned_data.update(self.content_form.cleaned_data)
            else:
                self.errors.update(self.content_form.errors)
        return vi
    
    def get_content_form(self, *args, **kwargs):
        instance = self.instance
        ct = instance.content_type
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
            return content_form(*args, **kwargs)
        else:
            return None
    
    def save(self, commit = True):
        obj = super(ExtraContentForm,self).save(commit = False)
        if self.content_form:
            obj._denormalize(self.content_form.instance)
            obj._new_content = self.content_form.save(commit = False)
        return super(ExtraContentForm,self).save(commit = commit)
    

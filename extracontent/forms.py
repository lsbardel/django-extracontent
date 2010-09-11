from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory


class ExtraContentForm(forms.ModelForm):
    '''This model form handles extra content from a content type field
    The model must be an instance of :class:`ExtraContentModel`.
    '''    
    def __init__(self, data=None, **kwargs):
        instance = kwargs.get('instance',None)
        self.initial_extra = None if not instance else instance.extra_content
        super(ExtraContentForm,self).__init__(data=data, **kwargs)
        
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
        cf = getattr(self,'_content_form',False)
        if cf is False:
            instance = self.instance
            ct  = instance.content_type
            if ct:
                model = ct.model_class()
                content_form  = modelform_factory(model)
                data  = self.data
                instance = self.initial_extra
                if instance and not isinstance(instance,model):
                    opts = content_form._meta
                    initial_extra = forms.model_to_dict(instance, opts.fields, opts.exclude)
                    initial_extra.pop(model._meta.pk.attname,None)
                    initial_extra.update(data)
                    data = initial_extra
                    instance = None
                cf = content_form(data = data, instance = instance)
            else:
                cf = None
            setattr(self,'_content_form',cf)
        return cf
    
    def save(self, commit = True):
        obj = super(ExtraContentForm,self).save(commit = False)
        cf = self.content_form()
        new_extra = None if not cf else cf.save()
        obj.set_content(new_extra,self.initial_extra)
        if commit:
            return super(ExtraContentForm,self).save(commit = commit)
        else:
            return obj
    

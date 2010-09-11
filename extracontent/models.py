from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class ExtraContentBase(models.Model):
    '''Abstract Model class for models with a dynamic content_type.
    '''
    extra_content_one2one = False
    object_id      = models.PositiveIntegerField(default = 0, editable = False)
    _extra_content = generic.GenericForeignKey('content_type', 'object_id')
    
    def __init__(self, *args, **kwargs):
        super(ExtraContentBase,self).__init__(*args, **kwargs)
    
    class Meta:
        abstract = True
        
    def extra_content(self):
        try:
            return self._extra_content
        except:
            return None
    
    @property
    def type(self):
        if self.content_type:
            return self.content_type.name
        else:
            return ''
        
    def _denormalize(self):
        return False
        
    def save(self, **kwargs):
        super(ExtraContentBase,self).save(**kwargs)
        if self._denormalize():
            self.extra_content().save()
        
    @classmethod
    def delete_extra_content(cls, instance = None, **kwargs):
        if isinstance(instance,cls):
            obj = instance.extra_content()
            if obj:
                obj.delete()
    
    @classmethod
    def register_one2one(cls):
        '''Use this class method to register a one-to-one relationship with extra content'''
        from django.db.models import signals
        signals.pre_delete.connect(cls.delete_extra_content, sender = cls)
        
        
class ExtraContent(ExtraContentBase):
    '''Abstract Model class for models with a dynamic content_type.
    '''
    content_type   = models.ForeignKey(ContentType, blank=True, null=True)
    
    class Meta:
        abstract = True


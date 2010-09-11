from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class ExtraContentModel(models.Model):
    '''Abstract Model class for models with a dynamic content_type.
    '''
    content_type   = models.ForeignKey(ContentType, blank=True, null=True)
    object_id      = models.PositiveIntegerField(default = 0, editable = False)
    _extra_content = generic.GenericForeignKey('content_type', 'object_id')
    
    def __init__(self, *args, **kwargs):
        super(ExtraContentModel,self).__init__(*args, **kwargs)
        self._new_content = None
    
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
        
    def _denormalize(self, ec = None):
        pass
        
    def save(self, **kwargs):
        nc = self._new_content
        if nc:
            ec = self.extra_content()
            if ec and ec != nc:
                ec.delete()
            self.content_type = ContentType.objects.get_for_model(nc)
            if nc.id:
                self.object_id = nc.id
        if not self.object_id:
            self.object_id = 0
        super(ExtraContentModel,self).save(**kwargs)
        if nc:
            self._denormalize()
            nc.save()
            if self.object_id != nc.id:
                self.object_id = nc.id
                super(ExtraContentModel,self).save(**kwargs)
        self._extra_content = nc
        
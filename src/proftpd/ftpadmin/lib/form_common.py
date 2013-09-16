#coding=utf-8

from django.db.models.fields import BLANK_CHOICE_DASH, BLANK_CHOICE_NONE
from django import forms
from django.forms.util import ErrorList
from django.db.models import Q

from proftpd.ftpadmin.lib.common import initlog


logger2 = initlog()


def set_select_choice( choices=None, select_choice=None):
    new_choices = []
    for (choice_value, choice_name) in choices:
        if choice_value != select_choice:
            new_choices.append((choice_value, choice_name))
        else:
            new_choices.insert(0, (choice_value, choice_name))
    return  new_choices

def get_year_list(*args):
    begin_year = args[0]
    end_year = args[1] + 1
    years = []
    for i in range(begin_year, end_year):
        years.append(i)
    return years

EXPIRATION_YEAR_CHOICES = get_year_list(2010, 2110)


class DynamicAddFormAttr(type):
    def __new__(cls, name, bases, attr):
        attr['one'] = 'test_signal'
        if attr.get('username', 'None'):
            logger2.info("metaclass test1")
        return type.__new__(cls, name, bases, attr)

    def __init__(cls, name, bases, attr):

        super(DynamicAddFormAttr, cls).__init__(name, bases, attr) 



#class newBaseModelForm(forms.Form):
class newModelForm(forms.Form):

    def __init__(self, *args, **kwargs):
        files=None
        auto_id='id_%s'
        prefix=kwargs.get('prefix', None)
        self.instance = kwargs.get('instance', None)
        self.model = kwargs.get('model', None)
        if self.model == None:
            raise 
        if self.instance == None:
            instance = self.instance
            object_data = None
        else:
            instance = self.instance
            object_data = self.get_object_data(instance)
        self.data = kwargs.get('data', None)
        data = self.data
        error_class=ErrorList
        label_suffix=':'
        empty_permitted=False
        super(newModelForm, self).__init__(data, files, auto_id, prefix, object_data,
                                            error_class, label_suffix, empty_permitted)
        self.init_field()
        



    def init_field(self):
        if self.instance:
            self.id = forms.CharField(max_length=255, label='ID', widget=forms.HiddenInput())
            self.init_edit_form()
        self.init_choices_and_foreign_field()
        self.init_after()

    def init_edit_form(self):
        pass


    def init_after(self):
        pass


    def init_choices_and_foreign_field(self):
        #对choices 及外键的field进行初始化数据
        self.local_field_objects = self.get_local_field_objects(model=self.model)
        for field in self.local_field_objects:
            if hasattr(field, 'choices') and len(field.choices) > 0 :
                if self.instance :
                    self.fields[field.name].choices =  self.get_choices(choices_type='choices', select_choice=getattr(self.instance, field.name), field_object=field) 
                else:
                    if field.has_default():
                        self.fields[field.name].choices = self.get_choices(choices_type='choices', select_choice=field.get_default(), field_object=field)
                    else:
                        self.fields[field.name].choices = field.get_choices()
            elif hasattr(field, 'related'):
                if self.instance :
                    self.fields[field.name].choices =  self.get_choices(choices_type='foreign_key', select_choice=getattr(self.instance, field.name), field_object=field)
                else:
                    self.fields[field.name].choices = self.get_choices(choices_type='foreign_key', select_choice='', field_object=field)
            elif hasattr(field, 'default'):
                if self.instance :
                    self.fields[field.name].initial = getattr(self.instance, field.name)
                else:
                    self.fields[field.name].initial = field.get_default()
        


    def get_local_field_objects(self, model=None):
        local_field_objects = []
        if model:
            local_field_objects = [ y[0] for y in model._meta.get_fields_with_model() if y[0].name in self.fields.keys() ]
        return local_field_objects




    def get_choices(self, choices_type='choices', select_choice=None, field_object=None):
        new_CHOICES = []
        if choices_type == 'foreign_key'  and field_object:
            pk_list = [ pk_value[0] for pk_value in field_object.related.parent_model.objects.all().values_list('id') ]
            #外键模型modle里必须有方法__unicode__ ，要不然会报错！
            related_instance_choices = [ (pk_value, field_object.related.parent_model.objects.get( pk=pk_value).__unicode__() ) for pk_value in pk_list ]
            if select_choice:
                new_CHOICES = set_select_choice( choices=related_instance_choices, select_choice=select_choice.id)
            else:
                related_instance_choices = BLANK_CHOICE_DASH + list(related_instance_choices) 
                new_CHOICES = set_select_choice( choices=related_instance_choices, select_choice='')

        elif choices_type == 'choices'  and field_object:
            if select_choice:
                new_CHOICES = set_select_choice( choices=field_object.choices, select_choice=select_choice)
            else:
                new_CHOICES = set_select_choice( choices=BLANK_CHOICE_DASH+list(field_object.choices), select_choice='')

        return  new_CHOICES



    def get_object_data(self, model_instance=None):
        #related_fields = [ x.var_name for x in model_instance._meta.get_all_related_objects() ]
        #model_fields = [ k for k in model_instance._meta.get_all_field_names() if  k not in  related_fields ]
        model_fields = [ y[0].name for y in model_instance._meta.get_fields_with_model() ] #这种方法更简便！！
        data = {}
        for keys in model_fields:
            data[keys] = getattr(model_instance, keys)
        return data


    def check_field_value_unique(self, field_name=None):
        try:
            self.model.objects.get(eval( "Q(%s=\"%s\")" % (field_name, self.cleaned_data[field_name]) ))
        except self.model.DoesNotExist:
            return self.cleaned_data[field_name]
        raise forms.ValidationError("This %s (%s) is already in use. Please choose another." % (field_name, self.cleaned_data[field_name]) )

    def check_field(self, field_name=None):
        if field_name and self.instance == None : 
            if self.cleaned_data.has_key(field_name) and self.cleaned_data[field_name] !='' :
                return self.check_field_value_unique(field_name=field_name)
            else:
                raise forms.ValidationError("The field [%s] can not be empty! " % field_name)
        elif field_name:
            if self.cleaned_data[field_name] !='' and (self.cleaned_data[field_name] !=getattr(self.instance, field_name) ):
                return self.check_field_value_unique(field_name=field_name)
            else:
                return getattr(self.instance, field_name)

    def clean_before(self):
        pass

    def clean_after(self):
        pass

    def clean(self):
        self.clean_before()
        for field in self.local_field_objects:
            if field.name != 'id' and hasattr(field, 'unique') and field.unique and hasattr(field, 'editable') and field.editable != False:
                self.cleaned_data[field.name] = self.check_field(field_name=field.name)
        self.clean_after()
        return self.cleaned_data


    def get_save_data(self, model=None):
        field_objects = [ y[0] for y in model._meta.get_fields_with_model() ] #取得model中的全部field 对象
        save_dict = {}
        for field in field_objects:
            
            if hasattr(field, 'related') and field.name in self.fields.keys():  #判断是否为外键，然后取得该外键对象。 同时判断该field是否在本类中定义。
                pk_value = self.cleaned_data.get(field.name)
                related_instance = field.related.parent_model.objects.get(pk=pk_value)
                save_dict[field.name] = related_instance
    
            elif hasattr(field, 'editable') and field.editable == True and field.name in self.fields.keys():  #判断此field是否可编辑！ 同时判断该field是否在本类中定义。
                save_dict[field.name] = self.cleaned_data.get(field.name)
    
            elif (self.instance != None ) : #如果是作为修改表单，则那些不可编辑的field值将仍是在数据库里头
                save_dict[field.name] = getattr(self.instance, field.name)
    
        return save_dict


            

    def save(self):
        save_args = self.get_save_data(self.model)
        new_instance = self.model( **save_args )
        new_instance.save()
        return new_instance




#class newModelForm(newBaseModelForm):
#    #__metaclass__ = DynamicAddFormAttr

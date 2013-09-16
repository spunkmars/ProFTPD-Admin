#coding=utf-8

from proftpd.ftpadmin.lib.common import initlog

#logger2=initlog()

def get_model_all_field_objects(model=None):
    field_objects = []
    if model is not None:
        field_objects = [ y[0] for y in model._meta.get_fields_with_model() ]
    return field_objects


def get_model_relate_field(model=None):
    field_objects = get_model_all_field_objects(model=model) #取得model中的全部field 对象
    relate_field = {}
    for field in field_objects:
        if hasattr(field, 'related') :  #判断是否为外键。
            relate_field[field.name] = field.related.parent_model
    return relate_field


def get_model_valid_fields(model=None, invalid_fields=[]):
    valid_fields = []
    field_objects = get_model_all_field_objects(model=model)
    for field in field_objects:
        single_field = {}
        if field.editable == False or field.unique == True :    #过滤 不允许修改, 不允许重复  的field 
            continue
        if field.has_default():
            field_init = field.default
        else:
            field_init = None
        #if field.verbose_name:
        #    field_name = field.verbose_name
        #else:
        #    field_name = field.name
        field_name = field.name
        single_field['name'] = field_name
        single_field['init'] = field_init
        single_field['obj'] = field
        if len(single_field) >= 3 and single_field['name'] not in invalid_fields:
            valid_fields.append(single_field)
    return valid_fields


def mult_save(model=None, mult_ids=None, save_args={}):

    if model is not None and mult_ids is not None:
        relate_field = {}
        relate_field = get_model_relate_field(model=model)
        modify_items = model.objects.filter(pk__in=mult_ids.split(','))
        for obj_item in modify_items:
            for arg_name in save_args.keys():
                #logger2.info(dir(obj_item))
                if  arg_name in relate_field.keys():
                    related_instance = relate_field[arg_name].objects.get(pk=save_args[arg_name])
                    setattr(obj_item, arg_name, related_instance)
                else:
                    setattr(obj_item, arg_name, save_args[arg_name])
            obj_item.save()

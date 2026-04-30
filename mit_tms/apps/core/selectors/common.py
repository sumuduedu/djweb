# core/selectors/common.py
def get_object_by_id(model, id):
    return model.objects.get(id=id)

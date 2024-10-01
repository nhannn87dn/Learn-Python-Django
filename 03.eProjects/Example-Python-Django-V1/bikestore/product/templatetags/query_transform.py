from django import template

register = template.Library()


# Để mục đích phân trang, nối tham số page vào url đã có
# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/#simple-tags

@register.simple_tag
def query_transform(request, **kwargs):
    query_params = request.GET.copy()
    for k, v in kwargs.items():
        if v == '':
            del query_params[k]
        else:
            query_params[k] = v

    return query_params.urlencode()




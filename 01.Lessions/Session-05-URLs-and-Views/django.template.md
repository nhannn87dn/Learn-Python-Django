# The Django template language

## Sử dụng biến

Biến đơn:

```django
<p>My first name is {{ first_name }}. My last name is {{ last_name }}.</p>
```

Hoặc một object:

```django
{{ my_dict.key }}
{{ my_object.attribute }}
{{ my_list.0 }}
```

## Sử dụng Tags

Trong Django, **tags** là một phần quan trọng của ngôn ngữ template. Chúng cho phép bạn thực hiện các logic lập trình như thực thi các câu lệnh if và vòng lặp for. Để thực thi các tags, chúng ta bao quanh chúng trong dấu `{% %}`.


Dưới đây là một số ví dụ về cách sử dụng các tags phổ biến trong Django:

1. **Tag `if`**: Được sử dụng để kiểm tra một điều kiện².

```html
{% if user.is_authenticated %}
    <p>Xin chào, {{ user.username }}!</p>
{% else %}
    <p>Xin chào, khách!</p>
{% endif %}
```

2. **Tag `for`**: Được sử dụng để lặp qua một danh sách².

```html
<ul>
{% for item in item_list %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

3. **Tag `block` và `extends`**: Được sử dụng để tạo ra sự kế thừa template².

```html
<!-- base.html -->
<html>
<head>
    <title>{% block title %}Trang chủ{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- home.html -->
{% extends "base.html" %}
{% block title %}Trang chủ{% endblock %}
{% block content %}
    <h1>Xin chào!</h1>
{% endblock %}
```

4. **Tag `autoescape`**: Được sử dụng để kiểm soát việc tự động thoát HTML².

```html
{% autoescape off %}
    {{ body }}
{% endautoescape %}
```

5. **Tag `csrf_token`**: Được sử dụng để bảo vệ form khỏi tấn công CSRF².

```html
<form method="post">
    {% csrf_token %}
    <!-- Các trường form ở đây -->
</form>
```

6. **Tag `comment`**: Được sử dụng để bỏ qua mọi thứ giữa `{% comment %}` và `{% endcomment %}`².

```html
{% comment "Optional note" %}
    <p>Đoạn văn bị bình luận</p>
{% endcomment %}
```

7. **Tag `cycle`**: Sản xuất một trong các đối số của nó mỗi khi gặp tag này².

```html
{% for o in some_list %}
    <tr class="{% cycle 'row1' 'row2' %}">
        ...
    </tr>
{% endfor %}
```

Lưu ý: Trong các ví dụ trên, giả định rằng các biến như `user`, `item_list`, và `body` đã được truyền vào context khi render template.

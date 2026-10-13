{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.name }}
{% endblock %}

{% block html %}
http://localhost:8000/accounts/api/v1/activation/confirm/{{token}}
{% endblock %}
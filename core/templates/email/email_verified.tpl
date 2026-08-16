{% extends "mail_templated/base.tpl" %}

{% block subject %}
Email Verification
{% endblock %}

{% block html %}
<h1>Hello {{ username }}</h1>
<h2> Your email address: </h2>
<h2>{{ user_email }}</h2>
<p>Your verification token:</p>

<p>http://localhost:8000/api/v1/activation/confirm/{{ token }}</p>
{% endblock %}
{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Password
{% endblock %}

{% block html %}

<h1>Forgot Password?</h1>

<p>Hello {{ username }}</p>

<p>
    We received a request to reset your password.
</p>

<p>
    Click the link below to create a new password:
</p>

<a href="{{ reset_url }}">
    Reset Password
</a>

<p>
    Or copy this link into your browser:
</p>

<p>
    {{ reset_url }}
</p>

<p>
    If you did not request a password reset,
    you can safely ignore this email.
</p>

{% endblock %}
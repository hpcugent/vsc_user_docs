test1: OS_IF
{% if OS == windows %}
test1
{% endif %}

test2: OS_IF in NON_OS_IF
{% if site == Gent %}
test2
{% if OS == windows %}
test2
{% endif %}
{% endif %}

test3: OS_IF with else
{% if OS == linux %}
test3
{% else %}
test3
{% endif %}

test4: OS_IF with wrong syntax
{ if OS == macos }
test4
{ endif }

test5: OS_IF in OS_IF
{% if OS == windows %}
test5
{% else %}
{% if OS == linux %}
test5
{% else %}
test5
{% endif %}
test5
{% endif %}

test6: NON_OS_IF in OS_IF
{% if OS == macos %}
test6
{% if site == Gent %}
test6
{% endif %}
test6
{% endif %}

test7: weird spacing and dashes
	{%if OS == windows %}
	test7
{%- else%}
	test7
		{% if OS == linux%}
test7
	{%-endif %}
{%endif%}
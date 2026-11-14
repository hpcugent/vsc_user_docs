test7: weird spacing and dashes
	{%if OS == windows %}
	test7
{%- else%}
	test7
		{% if OS == linux%}
test7
	{%-endif %}
{%endif%}
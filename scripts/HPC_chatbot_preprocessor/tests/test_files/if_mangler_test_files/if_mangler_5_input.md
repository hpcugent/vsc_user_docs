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
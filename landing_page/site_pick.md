{% macro sitepick(ant_home_url, gent_home_url, brussel_home_url, leuven_home_url) %}
# Please select your site:

{%- if ant_home_url %}
[Antwerpen]({{ant_home_url}}){ .md-button }
{%- endif %}
{%- if gent_home_url %}
[Gent]({{gent_home_url}}){ .md-button }
{%- endif %}
{%- if brussel_home_url %}
[Brussel]({{brussel_home_url}}){ .md-button }
{%- endif %}
{%- if leuven_home_url %}
[Leuven]({{leuven_home_url}}){ .md-button }
{%- endif %}
{% endmacro %}

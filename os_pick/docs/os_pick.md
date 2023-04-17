{% macro ospick(linuxURL, windowsURL, macosURL) %}
# Please select your operating system:

[Linux]({{linuxURL}}){ .md-button }
[macOS]({{macosURL}}){ .md-button }
[Windows]({{windowsURL}}){ .md-button }
{% endmacro %}

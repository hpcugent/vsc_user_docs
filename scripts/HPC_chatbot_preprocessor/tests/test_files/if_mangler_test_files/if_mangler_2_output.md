test2: OS_IF in NON_OS_IF
{% if site == Gent %}
test2
{-if-% if OS == windows %-if-}
test2
{-if-% endif %-if-}
{% endif %}
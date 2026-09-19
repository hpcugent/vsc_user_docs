test1: OS_IF
{-if-% if OS == windows %-if-}
test1
{-if-% endif %-if-}

test2: OS_IF in NON_OS_IF
{% if site == Gent %}
test2
{-if-% if OS == windows %-if-}
test2
{-if-% endif %-if-}
{% endif %}

test3: OS_IF with else
{-if-% if OS == linux %-if-}
test3
{-if-% else %-if-}
test3
{-if-% endif %-if-}

test4: OS_IF with wrong syntax
{ if OS == macos }
test4
{ endif }

test5: OS_IF in OS_IF
{-if-% if OS == windows %-if-}
test5
{-if-% else %-if-}
{-if-% if OS == linux %-if-}
test5
{-if-% else %-if-}
test5
{-if-% endif %-if-}
test5
{-if-% endif %-if-}

test6: NON_OS_IF in OS_IF
{-if-% if OS == macos %-if-}
test6
{% if site == Gent %}
test6
{% endif %}
test6
{-if-% endif %-if-}

test7: weird spacing and dashes
	{-if-%if OS == windows %-if-}
	test7
{-if-%- else%-if-}
	test7
		{-if-% if OS == linux%-if-}
test7
	{-if-%-endif %-if-}
{-if-%endif%-if-}
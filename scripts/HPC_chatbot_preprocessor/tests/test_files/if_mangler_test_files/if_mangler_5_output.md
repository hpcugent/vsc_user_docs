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
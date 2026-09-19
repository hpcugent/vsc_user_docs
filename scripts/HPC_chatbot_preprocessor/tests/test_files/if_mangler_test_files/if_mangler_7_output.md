test7: weird spacing and dashes
	{-if-%if OS == windows %-if-}
	test7
{-if-%- else%-if-}
	test7
		{-if-% if OS == linux%-if-}
test7
	{-if-%-endif %-if-}
{-if-%endif%-if-}
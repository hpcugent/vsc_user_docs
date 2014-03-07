pdf: clean example.pdf

example.pdf: example.md ../scripts/filter.hs
	VSC_SITE=$(site) pandoc --number-sections --filter ../scripts/filter.hs example.md -o example_$(site).pdf -f markdown+header_attributes+simple_tables+table_captions+grid_tables+multiline_tables

gent: site := gent
leuven: site := leuven
antwerpen: site := antwerpen

gent leuven antwerpen: example.pdf

clean:
	rm -f example_*.pdf

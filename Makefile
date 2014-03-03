all: clean documentation.pdf

documentation.pdf: documentation.md scripts/filter.hs
	VSC_SITE=$(site) pandoc --filter scripts/filter.hs documentation.md -o documentation.pdf -f markdown+header_attributes+simple_tables+table_captions+grid_tables+multiline_tables

gent: site := gent
gent: all

leuven: site := leuven
leuven: all

antwerpen: site := antwerpen
antwerpen: all

clean:
	rm -f documentation.pdf

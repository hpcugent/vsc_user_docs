all: example.pdf

example.pdf: example.md scripts/filter.hs
	VSC_SITE=$(site) pandoc --filter scripts/filter.hs example.md -o example.pdf -f markdown+header_attributes

gent: site := gent
gent: all

leuven: site := leuven
leuven: all

antwerpen: site := antwerpen
antwerpen: all

clean:
	rm example.pdf

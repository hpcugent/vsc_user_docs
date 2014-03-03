all: example.pdf

example.pdf: example.md filter.hs
	VSC_SITE=$(site) pandoc --filter ./filter.hs example.md -o example.pdf -f markdown+header_attributes

gent: site := gent
gent: all

leuven: site := leuven
leuven: all

antwerpen: site := antwerpen
antwerpen: all


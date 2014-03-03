all: example.pdf

example.pdf: example.md filter.hs
	pandoc --filter ./filter.hs example.md -o example.pdf -f markdown+header_attributes

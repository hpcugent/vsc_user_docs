defines = ""

all_os = linux mac windows
all_site = antwerp brussel gent leuven
all_doc = intro-HPC


# http://stackoverflow.com/questions/18136918/how-to-get-current-directory-of-your-makefile
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY = all


default:
ifdef OS
	make all
else ifdef SITE
	make all
else ifdef DOC
	make all
else
	@echo "One or more of the following variables must be set, unless 'make all' is used to build everything:"
	@echo "    DOC: $(all_doc)"
	@echo "    OS: $(all_os)"
	@echo "    SITE: $(all_site)"
	@echo "Example: 'make OS=windows SITE=gent'"
endif


ifndef OS
OS=$(all_os)
endif
ifndef SITE
SITE=$(all_site)
endif
ifndef DOC
DOC=$(all_doc)
endif

all:
	@for os in $(OS) ; do \
		for doc in $(DOC) ; do \
			cd $(ROOT_DIR)/$$doc ; \
			for site in $(SITE) ; do \
				jobname="$$doc-$$os-$$site" ; \
				latexcommand="pdflatex -interaction nonstopmode -jobname $$jobname \"\def\is$$os{1}\def\is$$site{1}\input{HPC.tex}\" " ; \
				$$latexcommand | grep 'Fatal error' > /dev/null && echo "$$jobname" failed, see log in $$doc/$$jobname.log && continue; \
			  makeglossaries $$jobname > /dev/null 2>&1; \
				$$latexcommand | grep 'Fatal error' > /dev/null && echo "$$jobname" failed, see log in $$doc/$$jobname.log && continue; \
			done ; \
		done ;  \
	done ;

style-guide: style-guide.pdf

style-guide.pdf: style-guide.tex
	pdflatex style-guide.tex
	pdflatex style-guide.tex

clean:
	rm -f *.log *.aux *.fdb_latexmk *.listing *.fls *.toc *.out *.glg *.glo *.gls *.ist *.ind *.ilg *.idx

defines = ""

all_os = linux mac windows
all_site = antwerpen brussel gent leuven
all_doc_os = intro-HPC intro-Linux intro-OpenStack
all_doc_noos = perfexpert


# http://stackoverflow.com/questions/18136918/how-to-get-current-directory-of-your-makefile
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY = all


default:
ifdef OS
	make all_os all_noos
else ifdef SITE
	make all_os all_noos
else ifneq (,$(findstring $(DOC),$(all_doc_noos)))
	make all_noos
else ifneq (,$(findstring $(DOC),$(all_doc_os)))
	make all_os
else
	@echo "One or more of the following variables must be set, unless 'make all' is used to build everything:"
	@echo "    DOC: $(all_doc_os) $(all_doc_noos)"
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
DOCOS=$(all_doc_os)
DOCNOOS=$(all_doc_noos)
else
ifneq (,$(findstring $(DOC),$(all_doc_os)))
DOCOS=$(DOC)
endif
ifneq (,$(findstring $(DOC),$(all_doc_noos)))
DOCNOOS=$(DOC)
endif
endif

all: all_os all_noos

all_os:
	@for os in $(OS) ; do \
		for doc in $(DOCOS) ; do \
			cd $(ROOT_DIR)/$$doc ; \
			for site in $(SITE) ; do \
				jobname="$$doc-$$os-$$site" ; \
				latexmk -pdf -verbose -r ../latexmkrc -jobname="$$jobname" -pdflatex="pdflatex -halt-on-error --file-line-error %O \"\def\is$$os{1}\def\is$$site{1}\input{%S}\" " $$doc.tex || \
				exit 1 && \
				echo ./$$doc/$$jobname.pdf created ; \
			done ; \
		done ; \
	done ;

all_noos:
	@for doc in $(DOCNOOS) ; do \
		cd $(ROOT_DIR)/$$doc ; \
		for site in $(SITE) ; do \
			jobname="$$doc-$$site" ; \
			latexmk -pdf -verbose -r ../latexmkrc -jobname="$$jobname" -pdflatex="pdflatex -halt-on-error --file-line-error %O \"\def\is$$os{1}\def\is$$site{1}\input{%S}\" " $$doc.tex || \
			exit 2 && \
			echo ./$$doc/$$jobname.pdf created ; \
		done ; \
	done ; \

style-guide: style-guide.pdf

style-guide.pdf: style-guide.tex macros.tex
	latexmk -pdf -r latexmkrc -pdflatex="pdflatex -halt-on-error --file-line-error %O %S" style-guide.tex

clean:
	@for doc in $(all_doc_os) $(all_doc_noos) ; do \
		cd $(ROOT_DIR)/$$doc ; \
		rm -f *.log *.aux *.fdb_latexmk *.listing *.fls *.toc *.out *.glg *.glo *.gls *.ist *.ind *.ilg *.idx shellcmds.sh; \
	done ;

mrproper: clean
	@for doc in $(all_doc_os) $(all_doc_noos) ; do \
		cd $(ROOT_DIR)/$$doc ; \
		rm -f $$doc-*.pdf ; \
	done ;

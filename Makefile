defines = ""

all_os = linux mac windows
all_site = antwerp brussel gent leuven
all_doc = intro-HPC

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
	for os in $(OS) ; do \
		for doc in $(DOC) ; do \
			cd $$doc ; \
			for site in $(SITE) ; do \
				jobname="$$doc-$$os-$$site" ; \
				latexcommand="pdflatex -jobname $$jobname \"\def\is$$os{1}\def\is$$site{1}\input{HPC.tex}\"" ; \
				echo $$latexcommand ; \
				$$latexcommand ; \
			  makeglossaries $$jobname ; \
				$$latexcommand ; \
			done ; \
			cd - ; \
		done ;  \
	done ;

style-guide: style-guide.pdf

style-guide.pdf: style-guide.tex macros.tex
	pdflatex style-guide.tex
	pdflatex style-guide.tex

clean:
	rm -f *.log *.aux *.fdb_latexmk *.listing *.fls *.toc *.out *.glg *.glo *.gls *.ist *.ind *.ilg *.idx

defines = ""

all_os = linux mac windows
all_site = antwerp brussel gent leuven
all_doc = intro-HPC
document_pdf = $(jobname).pdf

.PHONY = all

ifndef OS
OS=$(all_os)
endif
ifndef SITE
SITE=$(all_site)
endif
ifndef DOC
DOC=$(all_doc)
endif


default: complain

complain:
	echo "Please set OS, SITE and DOC variables. e.g. make OS=mac SITE=gent DOC=intro-HPC"

all: $(document_pdf)

$(document_pdf):
	for os in $(OS) ; do \
		for doc in $(DOC) ; do \
			for site in $(SITE) ; do \
				echo $$doc $$os $$site ; \
				jobname="$$doc-$$os-$$site" ; \
				latexcommand="pdflatex -jobname $$jobname \"\def\is$$os{1}\def\is$$site{1}\input{HPC.tex}\"" ; \
				cd $$doc ; \
				$$latexcommand ; \
			  makeglossaries $$jobname ; \
				$$latexcommand ; \
			done ; \
		done ;  \
	done ;

style-guide: style-guide.pdf

style-guide.pdf: style-guide.tex
	pdflatex style-guide.tex
	pdflatex style-guide.tex

clean:
	rm -f *.log *.aux *.fdb_latexmk *.listing *.fls *.toc *.out *.glg *.glo *.gls *.ist *.ind *.ilg *.idx

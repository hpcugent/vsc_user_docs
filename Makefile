defines = ""
jobname = HPC_$(OS)_$(SITE)
latex_command = pdflatex -jobname $(jobname) "\def\is$(OS){1}\def\is$(SITE){1}\input{HPC.tex}"

all_os = linux mac windows
all_site = antwerp brussel gent leuven
document_pdf = $(jobname).pdf

.PHONY = all

ifndef OS
OS=""
endif
ifndef SITE
SITE=""
endif

ifeq ($(strip $(OS)),"") 
$(error "OS must be set to one of $(all_os)")
endif
ifeq ($(strip $(SITE)),"")
$(error "SITE must be set to one of $(all_site)")
endif


all: $(document_pdf)

$(document_pdf): ch_*.tex HPC.tex
	$(latex_command)
	makeglossaries $(jobname)
	$(latex_command)

style-guide: style-guide.pdf

style-guide.pdf: style-guide.tex
	pdflatex style-guide.tex
	pdflatex style-guide.tex

clean:
	rm -f *.log *.aux *.fdb_latexmk *.listing *.fls *.toc *.out *.glg *.glo *.gls *.ist

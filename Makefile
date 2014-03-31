defines = ""
jobname = "HPC_$(OS)_$(SITE)"
latex_command = pdflatex -jobname $(jobname) "\def\is$(OS){1}\def\is$(SITE){1}\input{HPC.tex}"

pdf: ch_*.tex HPC.tex
ifeq ($(strip $(OS)),"")
	echo OS has not been set!
	exit 1
endif
ifeq ($(strip $(SITE)),"")
	echo "SITE has not been set!"
	exit 1
endif
	$(latex_command)
	makeglossaries $(jobname)
	$(latex_command)

style-guide: style-guide.tex
	pdflatex style-guide.tex
	pdflatex style-guide.tex

mac-leuven: OS=mac
mac-leuven: SITE=leuven

mac-gent: OS=mac
mac-gent: SITE=gent

mac-antwerpen: OS=mac
mac-antwerpen: SITE=antwerpen

mac-brussel: OS=mac
mac-brussel: SITE=brussel

mac-hasselt: OS=mac
mac-hasselt: SITE=brussel
mac-leuven mac-gent mac-hasselt mac-brussel mac-antwerpen: pdf

windows-leuven: OS=windows
windows-leuven: SITE=leuven

windows-gent: OS=windows
windows-gent: SITE=gent

windows-antwerpen: OS=windows
windows-antwerpen: SITE=antwerpen

windows-brussel: OS=windows
windows-brussel: SITE=brussel

windows-hasselt: OS=windows
windows-hasselt: SITE=hasselt
windows-leuven windows-gent windows-antwerpen windows-brussel windows-hasselt: pdf

linux-leuven: OS=linux
linux-leuven: SITE=leuven

linux-gent: OS=linux
linux-gent: SITE=gent

linux-antwerpen: OS=linux
linux-antwerpen: SITE=antwerpen

linux-brussel: OS=linux
linux-brussel: SITE=brussel

linux-hasselt: OS=linux
linux-hasselt: SITE=hasselt
linux-leuven linux-gent linux-antwerpen linux-brussel linux-hasselt: pdf

leuven:
	make mac-leuven
	make windows-leuven
	make linux-leuven

gent:
	make mac-gent
	make windows-gent
	make linux-gent

brussel:
	make mac-brussel
	make windows-brussel
	make linux-brussel

antwerpen:
	make mac-antwerpen
	make windows-antwerpen
	make linux-antwerpen

hasselt:
	make mac-hasselt
	make windows-hasselt
	make linux-hasselt

windows:
	make windows-leuven
	make windows-antwerpen
	make windows-hasselt
	make windows-brussel
	make windows-gent

mac:
	make mac-leuven
	make mac-antwerpen
	make mac-hasselt
	make mac-brussel
	make mac-gent

linux:
	make linux-leuven
	make linux-antwerpen
	make linux-hasselt
	make linux-brussel
	make linux-gent

all:
	make leuven
	make antwerpen
	make hasselt
	make brussel
	make gent

clean:
	rm -f *.log *.aux *.fdb_latexmk *.listing *.fls *.toc *.out *.glg *.glo *.gls *.ist

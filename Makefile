defines = ""
jobname = "HPC_$(OS)_$(SITE)"
latex_command = pdflatex -jobname $(jobname) "\def\is$(OS){1}\def\is$(SITE){1}\input{HPC.tex}"

pdf: *.tex HPC.tex
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

leuven:
	make mac-leuven
	make mac-gent

gent:
	make mac-gent
	make windows-gent

brussel:
	make mac-brussel
	make windows-brussel

antwerpen:
	make mac-antwerpen
	make windows-antwerpen

hasselt:
	make mac-hasselt
	make windows-hasselt

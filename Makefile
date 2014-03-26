defines = ""
latex_command = pdflatex "$(defines)\input{HPC.tex}"

pdf: ch*.tex HPC.tex
	$(latex_command)
	$(latex_command)

style-guide: style-guide.tex
	pdflatex style-guide.tex
	pdflatex style-guide.tex

mac-leuven: defines = \def\ismac{1}\def\isleuven{1}
mac-leuven: pdf

mac-gent: defines = "\def\ismac{1}\def\isgent{1}"
mac-gent: pdf

mac-antwerpen: defines = "\def\ismac{1}\def\isantwerpen{1}"
mac-antwerpen: pdf

mac-brussel: defines = "\def\ismac{1}\def\isbrussel{1}"
mac-brussel: pdf

mac-hasselt: defines = "\def\ismac{1}\def\ishasselt{1}"
mac-hasselt: pdf

windows-leuven: defines = "\def\iswindows{1}\def\isleuven{1}"
windows-leuven: pdf

windows-gent: defines = "\def\iswindows{1}\def\isgent{1}"
windows-gent: pdf

windows-antwerpen: defines = "\def\iswindows{1}\def\isantwerpen{1}"
windows-antwerpen: pdf

windows-brussel: defines = "\def\iswindows{1}\def\isbrussel{1}"
windows-brussel: pdf

windows-hasselt: defines = "\def\iswindows{1}\def\ishasselt{1}"
windows-hasselt: pdf

leuven: defines = \def\ismac{1}\def\iswindows{1}\def\isleuven{1}
leuven: pdf

gent: defines = "\def\ismac{1}\def\iswindows{1}\def\isgent{1}"
gent: pdf

antwerpen: defines = "\def\ismac{1}\def\iswindows{1}\def\isantwerpen{1}"
antwerpen: pdf

brussel: defines = "\def\ismac{1}\def\iswindows{1}\def\isbrussel{1}"
brussel: pdf

hasselt: defines = "\def\ismac{1}\def\iswindows{1}\def\ishasselt{1}"
hasselt: pdf

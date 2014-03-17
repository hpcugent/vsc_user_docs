pdf: ch*.tex HPC.tex
	latexmk -xelatex HPC.tex

style-guide: style-guide.tex
	latexmk -xelatex style-guide.tex

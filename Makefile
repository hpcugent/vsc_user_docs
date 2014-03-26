pdf: ch*.tex HPC.tex
	pdflatex HPC.tex && makeglossaries HPC && pdflatex HPC.tex

style-guide: style-guide.tex
	pdflatex style-guide.tex && pdflatex style-guide.tex

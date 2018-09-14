@echo off
SET /p site="Enter site (leuven, antwerpen, gent, brussel): "
SET /p os="Enter OS (windows, linux, mac): "
SET /p document="Enter document (intro-Linux, intro-HPC, perfexpert): "

SET root=%~dp0
CD %root%%document%
ECHO %cd%

:forever
latexmk -pdf -verbose -r ../latexmkrc -jobname="%document%-%os%-%site%" -pdflatex="pdflatex -halt-on-error --file-line-error %%O \"\def\is%os%{1}\def\is%site%{1}\input{%%S}\" " %document%.tex
pause
GOTO forever

#!/bin/bash

ec=0

result=$(find . -type f -name "*.tex" | xargs -n1 ./find_white_in_terminal.py)
if [[ $result ]]; then
    echo "Found one or more LaTeX commands in prompt environment, please close them with {}"
    echo "$result"
    ec=1
fi

# Style guide can use \verb to say it's not okay to use \verb
result=$(grep -R --include=\*.tex '\\verb\W' . | grep -v style-guide)
if [[ $result ]]; then
    echo "Found a \\verb command, please use \\lstinline instead"
    echo "$result"
    ec=1
fi

# make sure all chapter in HPC intro have a reference in title.tex
chapter_check_fails=0;
for chapter in $(grep "\label{ch:" intro-HPC/ch*tex | cut -f2- -d: | cut -c7-);
do
 cnt=$(grep $chapter intro-HPC/title.tex|wc -l);
 if [[ $cnt -ne 1 ]]; then
    echo $chapter;
    ((chapter_check_fails+=1));
 fi;
done
if [[ $chapter_check_fails -ne 0 ]]; then
    echo "Chapter label for one or more chapters not found in title.tex (see above)!"
    ec=$chapter_check_fails
fi

if [[ "$ec" -eq 0 ]]; then
    echo "All checks passed"
fi

exit $ec

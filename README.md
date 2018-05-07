VSC User Documentation
======================

VSC user training material and documentation

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img
alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work
is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons
Attribution-ShareAlike 4.0 International License</a>.

All site specific items go under `sites/<SITENAME>`.

The resulting PDFs can be found at https://hpcugent.github.io/vsc_user_docs/


Building
=============
On Mac os:

brew cask install mactex
brew install latex-mx

make all

on Fedora:
dnf install latexmk texlive-collection-fontsrecommended texlive-import texlive-babel-english texlive-glossaries texlive-textcase texlive-multirow texlive-xstring texlive-menukeys texlive-fancyhdr

make all


Development
============
When making changes, run `./check-version.sh <dir (e.g. intro-HPC)>` to update to new version before making a pr.

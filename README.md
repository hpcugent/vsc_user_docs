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
On macOS:

```
brew cask install mactex
brew install latex-mx

make all
```

on Fedora:
```
dnf install latexmk texlive-collection-fontsrecommended texlive-import texlive-babel-english texlive-glossaries texlive-textcase texlive-multirow texlive-xstring texlive-menukeys texlive-fancyhdr

make all
```

on Windows:
1. Install MiKTeX and Strawberry Perl
2. In the MiKTeX console, install  the `latexmk` package
3. Open `intro-Linux/intro-Linux.tex` in TeXworks (MiKTeX' editor) and press the green "play" button. This won't actually succesfully compile, but will prompt to install all the packages we need. Click "Yes" for all packages.
4. To compile your document, double-click `compile.bat` and fill in your build details. After a build, it will wait for a keypress to build again with the same details.

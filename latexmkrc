# This shows how to use the glossary package
# (http://www.ctan.org/tex-archive/macros/latex/contrib/glossary) and
# the glossaries package
# (http://www.ctan.org/tex-archive/macros/latex/contrib/glossaries)
# with latexmk.  Note that there are important differences between
# these two packages, so you should take careful note of the comments
# below.


# 4. If you use the glossaries package and have the makeglossaries
#    script installed, then you can do something simpler:

add_cus_dep('glo', 'gls', 0, 'makeglossaries');
add_cus_dep('acn', 'acr', 0, 'makeglossaries');
sub makeglossaries {
    if ( $silent ) {
        system( "makeglossaries -q \"$_[0]\"" );
    }
    else {
        system( "makeglossaries \"$_[0]\"" );
    };
}

push @generated_exts, 'glo', 'gls', 'glg';
push @generated_exts, 'acn', 'acr', 'alg';
$clean_ext .= ' %R.ist %R.xdy';

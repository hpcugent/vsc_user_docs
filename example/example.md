% Example documentation
% Toon Willems
  Kenneth Hoste
% March 7, 2014

# Introduction

This documents demos sample documentation to serve as a demo for a common documentation format
in the Flemish Supercompute Centre (VSC).

The document was originally created in `markdown` format, and converted to its current form using `pandoc`.

## Site-specific section

This section contains site-specific information below.

# {#site-specific include="ch1_section1.md"}

# Job submission

Simple example of job submission:

~~~~{#site-specific include="ch1_codeblock1.sh"}
~~~~

# Example features

## Lists

1. Item 1
2. Item 2
    * Nested 1
        * Nested nested
    * Nested 2

## Tables

  Right    Left     Center     Default
-------    ------ ----------   -------
    12     12        12            12
   123     123       123          123
     1     1          1             1

## Images

![PuTTy](images/putty.jpg)

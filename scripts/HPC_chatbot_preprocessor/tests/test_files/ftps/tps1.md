# Main title

This is the first paragraph of text. It is non-os-specific, however it does contain [a link](generic.md).
It also contains some `other` *Markdown* _syntax_ and an
```shell
example code block.
```
This intro needs to be sufficiently long as will be explained in the following section (we want to hit the minimum
character limit for a section).

## OS specific sections

This is the second section, it is the start of some {% if OS == windows %} text specific to windows.
In this section it is probably no longer needed to test the Markdown syntax again, however I will make it somewhat longer 
to make sure we get a long section that is over the minimum required length for the next newline character to be 
classified as the end of this section. I am doing this because for the next sections I want to test whether they will be
grouped together if they are not long enough to reach the minimum paragraph length on their own. Also, before I forget, 
let's add [a link](windows.md) in this section as well.

### Windows specific section

Like this.

And this.

And also this.

These section should all be grouped together under the windows specific section of the output. The addition of this long
section at the end should make sure the combination of sections comes to an end here.
{% else %}
text specific to OSes that aren't windows. I feel like there is no need to make this section very long, however I will
still add [a link](linuxmacos.md).

### Non Windows section

Whereas the Windows version of this section had a lot of unnecessary newlines, this one will just be a short and concise
section that ends right here.
{% endif %}

## Conclusion

Coming up with what to write in test texts is very hard. I think I got the most important test cases in there, but I 
might add to this if needed.

# Frequently Asked Questions 

## When will my job start?

{% if site == gent%}
See the explanation about how jobs get prioritized in [When will my job start](../running_batch_jobs/#when-will-my-job-start). 

{% else %}

In practice it's
impossible to predict when your job(s) will start, since most currently
running jobs will finish before their requested walltime expires, and
new jobs by may be submitted by other users that are assigned a higher
priority than your job(s). You can use the `showstart` command. For more
information, see .

{% endif %}

## Can I share my account with someone else?

**NO.** You are not allowed to share your VSC account with anyone else, it is
strictly personal. 
{% if site == gent %}
See
<https://helpdesk.ugent.be/account/en/regels.php>. 
{% endif %}
{% if site == leuven %}
For KU Leuven, see
<https://admin.kuleuven.be/personeel/english_hrdepartment/ICT-codeofconduct-staff#section-5>.
For Hasselt University, see <https://www.uhasselt.be/intra/IVC>. 
{% endif %}
{% if site == brussel %}
See <http://www.vub.ac.be/sites/vub/files/reglement-gebruik-ict-infrastructuur.pdf>.
{% endif %}
{% if site == antwerpen %}
See <https://pintra.uantwerpen.be/bbcswebdav/xid-23610_1> 
{% endif %}
{% if site == gent %}
If you want to share data, there are alternatives (like a shared directories in VO
space, see [Virtual organisations](../running_jobs_with_input_output_data/#virtual-organisations)).
{% endif %}

## Can I share my data with other {{hpc}} users?

Yes, you can use the `chmod` or `setfacl` commands to change permissions
of files so other users can access the data. For example, the following
command will enable a user named "otheruser" to read the file named
`dataset.txt`. See

<pre><code>$ <b>setfacl -m u:otheruser:r dataset.txt</b>
$ <b>ls -l dataset.txt</b>
-rwxr-x---+ 2 {{userid}} mygroup      40 Apr 12 15:00 dataset.txt
</code></pre>

For more information about `chmod` or `setfacl`, see [the section on
chmod in chapter 3 of the Linux intro
manual](https://hpcugent.github.io/vsc_user_docs/linux-tutorial/manipulating_files_and_directories/#changing-permissions-chmod).
<!-- % \section{I no longer work for \university, can I transfer my data to another researcher working at \university}
% See https://github.com/hpcugent/vsc_user_docs/issues/230 -->

## Can I use multiple different SSH key pairs to connect to my VSC account?

Yes, and this is recommended when working from different computers.
Please see [Adding multiple SSH public keys](../account/#adding-multiple-ssh-public-keys-optional) on how to do this.

## I want to use software that is not available on the clusters yet 

{% if site == gent %}

Please fill out the details about the software and why you need it in
this form:
<https://www.ugent.be/hpc/en/support/software-installation-request>.
When submitting the form, a mail will be sent to {{hpcinfo}} containing all the
provided information. The HPC team will look into your request as soon
as possible you and contact you when the installation is done or if
further information is required. 
{% else %}
Please send an e-mail to {{hpcinfo}} that includes:

-   What software you want to install and the required version

-   Detailed installation instructions

-   The purpose for which you want to install the software
  
{% endif %}

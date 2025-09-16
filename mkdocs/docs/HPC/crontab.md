# Cron scripts

## Cron scripts configuration

It is possible to run automated cron scripts as regular user on the
Ugent login nodes. Due to the high availability setup users should add
their cron scripts on the same login node to avoid any cron job script
duplication.

In order to create a new cron script first login to HPC-UGent login node
as usual with your vsc user's account (see section
[Connecting](../connecting/#connecting-to-the-hpc-infrastructure)).

Check if any cron script is already set in the current login node with:

<pre><code>$ <b>crontab -l</b>
</code></pre>

At this point you can add/edit (with `vi` editor) any cron script
running the command:

<pre><code>$ <b>crontab -e</b>
</code></pre>

**Warning**: **During maintenance it is possible that your crontab will be wiped. It is recommended to have a back-up of the content in your crontab.**

#### Example cron job script

<pre><code> 15 5 * * * ~/runscript.sh >& ~/job.out
</code></pre>

where `runscript.sh` has these lines in this example:

<center>-- runscript.sh --</center>
```bash
{% include "./examples/Cron-scripts/runscript.sh" %}
```

In the previous example a cron script was set to be executed every day
at 5:15 am. More information about crontab and cron scheduling format at
<https://www.redhat.com/sysadmin/automate-linux-tasks-cron>.

Please note that you should login into the same login node to edit your
previously generated crontab tasks. If that is not the case you can
always jump from one login node to another with:

<pre><code>$ <b>ssh gligar&lt;id&gt;</b>
</code></pre>

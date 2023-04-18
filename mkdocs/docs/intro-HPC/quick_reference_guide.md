# HPC Quick Reference Guide

Remember to substitute the usernames, login nodes, file names, ...for
your own.

<table>
    <tr>
        <td colspan="2">
            <center><b>Login</b></center>
        </td>
    </tr>
    <tr>
        <td colspan="1">
          Login
        </td>
        <td colspan="1">
          <tt>ssh {{userid}}@{{loginnode}}</tt>
        </td>
    </tr>
    <tr>
      <td colspan ="1">
        Where am I?
      </td>
      <td colspan="1">
        <tt>hostname</tt>
      </td>
    </tr>
    <tr>
      <td>
        Copy to {{hpc}}
      </td>
      <td>
        <tt>scp foo.txt {{userid}}@{{loginnode}}:</tt>
      </td>
    </tr>
    <tr>
      <td>
        Copy from {{hpc}}
      </td>
      <td> 
        <tt>scp {{userid}}@{{loginnode}}:foo.txt</tt>
      </td>
    </tr>
    <tr>
      <td>
        Setup ftp session
      </td>
      <td>
        <tt>sftp {{userid}}@{{loginnode}}</tt>
      </td>
    </tr>
</table>


<table>
    <tr>
        <td colspan="2">
            <center><b>Modules</b></center>
        </td>
    </tr>
    <tr>
        <td colspan="1">
          List all available modules
        </td>
        <td colspan="1">
         Module avail
        </td>
    </tr>
    <tr>
      <td colspan ="1">
        List loaded modules
      </td>
      <td colspan="1">
        module list
      </td>
    </tr>
    <tr>
      <td>
        Load module
      </td>
      <td>
        module load example
      </td>
    </tr>
    <tr>
      <td>
        Unload module
      </td>
      <td> 
        module unload example
      </td>
    </tr>
    <tr>
      <td>
        Unload all modules
      </td>
      <td>
        module purge
      </td>
    </tr>
    <tr>
      <td>
        Help on use of module
      </td>
      <td>
        module help
      </td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="2">
            <center><b>Jobs</b></center>
        </td>
    </tr>
    <tr>
        <td colspan="1">
          Submit job with job script <tt>script.pbs</tt>
        </td>
        <td colspan="1">
          <tt>qsub script.pbs</tt>
        </td>
    </tr>
    <tr>
      <td colspan ="1">
        Status of job with ID 12345
      </td>
      <td colspan="1">
        <tt>qstat 12345</tt>
      </td>
    </tr>
{% if site != (gent or brussel) %}
    <tr>
      <td colspan ="1">
        Possible start time of job with ID 12345 (not available everywhere)
      </td>
      <td colspan="1">
        <tt>showstart 12345</tt>
      </td>
    </tr>
    <tr>
      <td colspan ="1">
        Check job with ID 12345 (not available everywhere)
      </td>
      <td colspan="1">
        <tt>checkjob 12345</tt>
      </td>
    </tr>
{% endif %}
    <tr>
      <td>
        Show compute node of job with ID 12345
      </td>
      <td>
        <tt>qstat -n 12345</tt>
      </td>
    </tr>
    <tr>
      <td>
        Delete job with ID 12345
      </td>
      <td> 
        <tt>qdel 12345</tt>
      </td>
    </tr>
    <tr>
      <td>
        Status of all your jobs
      </td>
      <td>
        <tt>qstat</tt>
      </td>
    </tr>
    <tr>
      <td>
        Detailed status of your jobs + a list nodes they are running on
      </td>
      <td>
        <tt>qstat -na</tt>
      </td>
    </tr>
{% if site != (gent or brussel) %}
    <tr>
      <td>
        Show all jobs on queue (not available everywhere)
      </td>
      <td>
        <tt>showq</tt>
      </td>
    </tr>
{% endif %}
    <tr>
      <td>
        Submit Interactive job
      </td>
      <td>
        <tt>qsub -I</tt>
      </td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="2">
            <center><b>Disk quota</b></center>
        </td>
    </tr>
{% if site == gent %}
    <tr>
        <td colspan="1">
          Check your disk quota
        </td>
        <td colspan="1">
          see <a href="https://account.vscentrum.be">https://account.vscentrum.be</a>
        </td>
    </tr>
{% else %}
    <tr>
        <td colspan="1">
          Check your disk quota
        </td>
        <td colspan="1">
          <tt>mmlsquota</tt>
        </td>
    </tr>
    <tr>
        <td colspan="1">
          Check your disk quota nice
        </td>
        <td colspan="1">
          <tt>show_quota.py</tt>
        </td>
    </tr>
{% endif %}
    <tr>
      <td colspan ="1">
        Disk usage in current directory (<tt>.<tt>)
      </td>
      <td colspan="1">
        <tt>du -h</tt>
      </td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="2">
            <center><b>Worker Framework</b></center>
        </td>
    </tr>
    <tr>
        <td colspan="1">
          Load worker module
        </td>
        <td colspan="1">
         <tt> module load worker/1.6.8-intel-2018a</tt>  Don't forget to specify a version. To list available versions, use <tt>module avail worker/</tt>
        </td>
    </tr>
    <tr>
      <td colspan ="1">
        Submit parameter sweep
      </td>
      <td colspan="1">
        <tt>wsub -batch weather.pbs -data data.csv</tt>
      </td>
    </tr>
    <tr>
      <td>
        Submit job array
      </td>
      <td>
        <tt>wsub -t 1-100 -batch test_set.pbs</tt>
      </td>
    </tr>
    <tr>
      <td>
        Submit job array with prolog and epilog
      </td>
      <td> 
        <tt>wsub -prolog pre.sh -batch test_set.pbs -epilog post.sh -t 1-100</tt>
      </td>
    </tr>
</table>

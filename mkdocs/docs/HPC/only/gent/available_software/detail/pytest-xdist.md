---
hide:
  - toc
---

pytest-xdist
============


xdist: pytest distributed testing pluginThe pytest-xdist plugin extends pytest with some unique test execution modes:    * test run parallelization: if you have multiple CPUs or hosts you      can use those for a combined test run. This allows to speed up      development or to use special resources of remote machines.    * --looponfail: run your tests repeatedly in a subprocess. After        each run pytest waits until a file in your project changes and        then re-runs the previously failing tests. This is repeated        until all tests pass after which again a full run is        performed.    * Multi-Platform coverage: you can specify different Python      interpreters or different platforms and run tests in parallel on      all of them.Before running tests remotely, pytest efficiently “rsyncs” yourprogram source code to the remote place. All test results are reportedback and displayed to your local terminal. You may specify differentPython versions and interpreters.

https://github.com/pytest-dev/pytest-xdist
# Available modules


The overview below shows which pytest-xdist installations are available per HPC-UGent Tier-2cluster, ordered based on software version (new to old).

To start using pytest-xdist, load one of these modules using a `module load` command like:

```shell
module load pytest-xdist/3.3.1-GCCcore-12.3.0
```

*(This data was automatically generated on Thu, 07 Mar 2024 at 18:35:40 CET)*  

| |accelgor|doduo|donphan|gallade|joltik|skitty|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|pytest-xdist/3.3.1-GCCcore-12.3.0|x|x|x|x|x|x|
|pytest-xdist/2.5.0-GCCcore-11.3.0|x|x|x|x|x|x|
|pytest-xdist/2.5.0-GCCcore-11.2.0|x|-|x|-|x|-|
|pytest-xdist/2.3.0-GCCcore-10.3.0|x|x|x|x|x|x|
|pytest-xdist/2.3.0-GCCcore-10.2.0|x|x|x|x|x|x|


### pytest-xdist/3.3.1-GCCcore-12.3.0

This is a list of extensions included in the module:

apipkg-3.0.2, execnet-2.0.2, pytest-xdist-3.3.1

### pytest-xdist/2.5.0-GCCcore-11.3.0

This is a list of extensions included in the module:

apipkg-1.5, execnet-1.9.0, pytest-forked-1.4.0, pytest-xdist-2.5.0

### pytest-xdist/2.5.0-GCCcore-11.2.0

This is a list of extensions included in the module:

apipkg-1.5, execnet-1.9.0, pytest-forked-1.4.0, pytest-xdist-2.5.0

### pytest-xdist/2.3.0-GCCcore-10.3.0

This is a list of extensions included in the module:

apipkg-1.5, execnet-1.9.0, pytest-forked-1.3.0, pytest-xdist-2.3.0

### pytest-xdist/2.3.0-GCCcore-10.2.0

This is a list of extensions included in the module:

apipkg-1.5, execnet-1.9.0, pytest-forked-1.3.0, pytest-xdist-2.3.0
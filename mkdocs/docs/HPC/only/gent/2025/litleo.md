# New Tier-2 cluster: `litleo`

!!! warning
    The `litleo` cluster is currently only available to members of the `gpilot` user group.


In December 2024, a new cluster was added to the HPC-UGent Tier-2 infrastructure: `litleo`.

If you have any questions on using `litleo`, you can [contact the {{ hpcteam }}]({{ hpc_support_url }}).

For software installation requests, please use the [request form](https://www.ugent.be/hpc/en/support/software-installation-request).

---

## `litleo`: GPU cluster

`litleo` is a new GPU cluster.

It adds GPU capacity to existing clusters `joltik` and `accelgor`.

It is only intended for ***single GPU*** compute use.

This cluster consists of 8 workernodes, each with:

* 1x 48 core AMD EPYC 9454P (Genoa @ 2.75 GHz) processor;
* ~315 GiB of RAM memory;
* 1.4TB local NVMe disk;
* NDR-200 InfiniBand interconnect;
* RHEL9 as operating system;
* 2x NVIDIA H100 NVL (96GB VRAM)

To start using this cluster from a terminal session, first run:
```
module swap cluster/.litleo
```

You can also start (interactive) sessions on `litleo` using the [HPC-UGent web portal](../../../web_portal.md).

### Difference compared to `joltik` and `accelgor`.

The main difference between `litleo` and the other GPU clusters is that *jobs are limited to using only one GPU per job*.
The motivation comes from historical analysis of GPU usage on the `joltik` and `accelgor` clusters that show a very
high utilisation of a single GPU per job; combined with cost of the GPUs in 2024. It allowed us get the most out of the
budget.

---

## Shinx pilot phase (24/01/2025-01/03/2025)

As usual with any pilot phase, you need to be member of the `gpilot` group, and to start using this cluster run:

```
module swap cluster/.litleo
```

Shortly after the Tier-2 maintenance in February 2025, the cluster will enter production, without any significant changes.

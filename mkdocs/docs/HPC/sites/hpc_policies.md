# HPC Policies

{% if site == gent %}

## Access
Everyone can get access and use the HPC-UGent supercomputing infrastructure and services.
The conditions that apply depend on your affiliation.

### Access for staff and academics

#### Researchers and staff affiliated with Flemish university associations

-   Includes externally funded researchers registered in the
    personnel database (FWO, SBO, VIB, IMEC, etc.).

-   Includes researchers from all VSC partners.

-   Usage is free of charge.

-   Use your account credentials at your affiliated university
    to request a VSC-id and connect.

-   See [Getting a HPC Account](../../account).

#### Researchers and staff affiliated with other Flemish or federal research institutes

-   HPC-UGent promotes using the [Tier1 services of the VSC](https://www.vscentrum.be/compute).

-   HPC-UGent can act as a liason.

#### Students

-   Students can also use HPC-UGent (Bachelor or Master,
    enrolled in an institute mentioned above).

-   Same conditions apply, free of charge for all Flemish university associations.

-   Use your university account credentials to request a VSC-id and connect.

### Access for industry

Researchers and developers from industry can use the services and infrastructure tailored to industry from VSC.

#### Our offer

-   [VSC has a dedicated service geared towards industry](https://www.vscentrum.be/getaccess).

-   HPC-UGent can act as a liason to the VSC services.

#### Research partnership:

-   Interested in collaborating in supercomputing with a UGent research group?

-   We can help you look for a collaborative partner. Contact {{ hpcinfo }}.



## Data access retention

Users are advised to strictly adhere to the [Ghent University policy framework on research data](https://codex.ugent.be?regid=REG000092&lang=en)
and invest in [Research Data Management](https://www.ugent.be/en/research/openscience/datamanagement) throughout the life time of their scientific project.

Researchers, students, staff, ... that no longer have a valid contract ('statuut') with Ghent University will lose access to the data of their VSC account.

### Actions to take before leaving university

**WELL BEFORE** leaving university, users should offload their data.
Users are requested to:

- delete files that are no longer relevant from all storage locations in their account
    - this includes $VSC_HOME, $VSC_DATA, $VSC_SCRATCH, $VSC_DATA_VO and $VSC_SCRATCH_VO directories, ...
- transfer data to coworkers and/or promotor
    - make sure to provide sufficient metadata, explaining how to use/interpret data etc.
- take personal backups if needed

**All user data will no longer be accessible after a user has left university.**


### Possible actions after a user left university

When a user does not offload data before leaving university, user data might remain on HPC storage locations without a direct owner.
If access to this data is for some reason still needed (by the former user, promotor, ...), the following actions could be possible:

#### Request access as voluntary employee

A former user, in accord with the promotor, can request to become a [voluntary employee or unpaid postdoctoral staff member](https://ugentbe.sharepoint.com/:u:/r/sites/intranet-personeelszaken/SitePages/en/Vrijwillig-medewerker-en-postdoctoraal-onbezoldigd-medewerker.aspx).
Please note that the budget holder will be charged an annual fee for every voluntary employee.
Once the voluntary employee contract is in order, HPC staff can then reinstate the VSC account and restore access to remaining data.

#### Data transfer by HPC staff

As a very last resort measure, HPC staff can initiate a data transfer to another VSC account when requested by a VO moderator or promotor.
Please be aware that this is a non-trivial operation for HPC-UGent staff:

- it is an entirely manual process
- it is error-prone
- it has risks for the storage integrity
Hence our helpdesk staff needs to be able to dedicate sufficient time and focus to complete this task.

This is extremely time consuming and dangerous to the storage integrity.
If user was in a VO, we will assume all the data is owned by the VO (including HOM/DATA direcotires)



We will assume a VO moderator and/or promotor 

{% endif %}

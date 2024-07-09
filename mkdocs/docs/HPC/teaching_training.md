# Teaching and training

The HPC infrastructure can be used for teaching and training purposes, and
HPC-UGent provides support for getting you organized.

As a reminder, both Bachelor and Master students are allowed to use the HPC infrastructure,
and it is also possible to organize trainings (or workshops).
But in either case we do recommend preparing a fallback plan in case the HPC infrastructure becomes unavailable,
e.g. because of an unexpected power failure.

In general, we advise the use of the HPC webportal in combination with the
[interactive cluster](interactive_debug.md)
for teaching and training, but deviations are possible upon request.

In order to prepare things, make a _teaching request_ by [contacting the {{ hpcteam }}]({{ hpc_support_url }})
with the following information (explained further below):

- Title and nickname
- Start and end date for your course or training
- VSC-ids of all teachers/trainers
- Participants based on UGent Course Code and/or list of VSC-ids
- Optional information
    - Additional storage requirements
        - Shared folder
        - Groups folder for collaboration
        - Quota
    - Reservation for resource requirements beyond the interactive cluster
    - Ticket number for specific software needed for your course/training
    - Details for a custom Interactive Application in the webportal

In addition, it could be beneficial to set up a short Teams call with HPC-UGent team members,
especially if you are using a complex workflow for your course/workshop.

Please make these requests well in advance, several weeks before the start of your course/workshop.


## Title and nickname

The title of the course or training can be used in e.g. reporting.

The nickname is a single (short) word or acronym that the students or participants can easily
recognise, e.g. in the directory structure. In case of UGent courses, this is used next to the
course code to help identify [the course directory](./#dedicated-storage) in the list of all courses one might follow.

When choosing the nickname, try to make it unique, but this is not enforced nor checked.

## Start and end date

The start date (and time) is used as a target for the HPC-UGent team to set up your course requirements.
But note that this target is best-effort, depending on the load of the support team and the complexity of your requirements.
Requests should be made well in advance, at least several weeks before the actual start of your course.
The sooner you make the request, the better.

The end date is used to automatically perform a cleanup when your course/workshop has finished, 
as described in the [course data policy](./#course-data-policy):

- Course group and subgroups will be deactivated
- Residual data in the course directories will be archived or deleted
- Custom Interactive Applications will be disabled


## Teachers and trainers

A _course group_ is created with all students or participants, and the teachers or trainers are
the group moderators (and also member of this group).

This course group and the moderators group are used to manage the different privileges:
moderators have additional privileges over non-moderator members
e.g. they have read/write access in specific folders, can manage subgroups, ....

Provide us with a list of all the VSC-ids for the teachers or trainers to indentify the moderators.


## Participants

The management of the list of students or participants depends if this is a UGent course or a training/workshop. 

### UGent Courses

Based on the Course Code, we can create VSC accounts for all UGent students that have officially enrolled
in your UGent course (if they do not have an account already).
Students will then no longer have to take steps themselves to request a VSC account.
The students do need to be officially enrolled, so that they are linked to your UGent Course Code.

The created VSC accounts will be accounts without an ssh-key.
This allows the students to use e.g. the portal, but if they require ssh access to the infrastructure,
they will have to [add an SSH key](account.md#adding-multiple-ssh-public-keys-optional) themselves.

Additionally, for external, non-UGent students the _teaching request_ must contain the list
of their VSC-ids, so they can be added to the course group.

A course group will be automatically created for your course, with all VSC accounts of registered students as member.
Typical format `gcourse_<coursecode>_<year>`, e.g. `gcourse_e071400_2023`.
Teachers are [moderator of this course group](./#teachers-and-trainers), but will not be able to add unregistered students or moderators.
VSC accounts that are not linked to the Course Code will be automatically removed from the course group.
To get a student added to the course group, make sure that the student becomes officially enrolled in your course.

### Trainings and workshops

(Currently under construction:)
For trainings, workshops or courses that do not have a Course Code, you need to provide us with the list of all VSC-ids.
A group will be made, based on the name of the workshop, with all VSC-ids as member.
Teachers/trainers will be able to add/remove VSC accounts from this course group.
But students will have to follow the [procedure to request a VSC account](account.md) themselves.
There will be no automation.


## Dedicated storage

For every course, a dedicated course directory will be created on the _DATA_ filesystem
under `/data/gent/courses/<year>/<nickname>_<coursecode>` (e.g. `/data/gent/courses/2023/cae_e071400`).

This directory will be accessible by all members of your course group.
(Hence, it is no longer necessary to set up dangerous workarounds e.g. invite course members to your virtual organization.)

Every course directory will always contain the folders:

- `input`
    - ideally suited to distribute input data such as common datasets
    - moderators have read/write access
    - group members (students) only have read access
- `members`
    - this directory contains a personal folder for every student in your course `members/vsc<01234>`
    - only this specific VSC-id will have read/write access to this folder
    - moderators have read access to this folder


### Shared and groups

Optionally, we can also create these folders:

- `shared`
    - this is a folder for sharing files between any and all group members
    - all group members and moderators have read/write access
    - beware that group members will be able to alter/delete each others files in this folder if they set
      permissions in specific/non-default ways
- `groups`
    - a number of `groups/group_<01>` folders are created under the `groups` folder
    - these folders are suitable if you want to let your students collaborate closely in smaller groups
    - each of these `group_<01>` folders are owned by a dedicated group
    - teachers are automatically made moderators of these dedicated groups
    - moderators can populate these groups with VSC-ids of group members in the VSC accountpage
      or ask the students to invite themselves via [group edit](https://account.vscentrum.be/django/group/edit).
      When students invite them self, moderators still need to [approve the group invites](https://account.vscentrum.be/django/group/approve).
    - only these VSC-ids will then be able to access a `group_<01>` folder, and will have read/write access.


If you need any of these additional folders, do indicate under _Optional storage requirements_
of your _teaching request_:

- `shared`: `yes`
- `subgroups`: `<number of (sub)groups>`

### Course Quota

There are 4 quota settings that you can choose in your _teaching request_ in the case the defaults are not sufficient:

- overall quota (defaults *10 GB volume* and *20k files*) are for the moderators and can be used for e.g. the `input` folder.
- member quota (defaults *5 GB volume* and *10k files*) are per student/participant

The course data usage is not accounted for any other quota (like VO quota). It is solely dependent on these settings.


### Course data policy

The data policy for the dedicated course storage is the following:
on the indicated end date of your course, the course directory will be made read-only to the moderators
(possibly on the form of an archive zipfile).
One year after the end date it will be permanently removed.
We assume that teachers/trainers always have an own copy of the course data as a starting point for a next course.


## Resource requirements beyond the interactive cluster

We assume that your course requirements are such that the [interactive cluster](interactive_debug.md) can be used.
If these resources are insufficient, you will need to request and motivate a reservation.

Indicate which cluster you would need and the number of nodes, cores and/or GPUs.
Also, clearly indicate when you would need these resources, i.e. the dates and times of each course session.

Be aware that students will have no access to the reservation outside the course sessions.
This might be relevant when requesting a custom application.

Reservations take away precious resources for all HPC users, so only request this when it is really needed for your course.
In our experience, the [interactive cluster](interactive_debug.md) is more than sufficient for the majority of cases.


## Specific software

In case you need software for your course/workshop that is unavailable or that needs to be updated,
make a separate [software installation request](https://www.ugent.be/hpc/en/support/software-installation-request).
Add the OTRS ticket number in your _teaching request_.

We will try to make the software available before the start of your course/workshop.
But this is always best effort, depending on the load of the support team and the complexity of your software request.
Typically, software installation requests must be made at least one month before the course/workshop starts.

Ideally, courses/workshops rely on software that is already in use (and thus also well tested).


## Custom Interactive Application in the webportal


HPC-UGent can create a custom interactive application in the web portal for your course/workshop.
Typically, this is a generic interactive application such as cluster desktop, Jupyter notebook, ...
in which a number of options are preset or locked down:
e.g. the number of cores, software version, cluster selection, autostart code, etc.
This could make it easier for teachers and students, since students are less prone to making mistakes
and do not have to spend time copy-pasting specific settings.

A custom interactive application will only be available to the members of your course group.
It will appear in the `Interactive Apps` menu in the webportal, under the section `Courses`.
After the indicated end date of your course, this application will be removed.

If you would like this for your course, provide more details in your _teaching request_, including:

- what interactive application would you like to get launched (cluster desktop, Jupyter Notebook, ...)

- which cluster you want to use

- how many nodes/cores/GPUs are needed

- which software modules you are loading

- custom code you are launching (e.g. autostart a GUI)

- required environment variables that you are setting

- ...

We will try to make the custom interactive application available before the start of your course/workshop,
but this is always best effort, depending on the load of the support team and the complexity of your request.

A caveat for the teacher and students is that students do not learn to work with the generic application,
and do not see the actual commands or customization code.
Therefore, per custom interactive application, HPC-UGent will make a dedicated section in the
[web portal chapter of the HPC user documentation](web_portal.md#custom-apps).
This section will briefly explain what happens under the hood of the interactive application.
We would recommend that you as a teacher take some time to show and explain this to the students.
Note that the custom interactive application will disappear for students after the indicated end of your course,
but the section in the web portal will remain there for several years, for reference.

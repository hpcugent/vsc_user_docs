# Teaching and training

The HPC infrastructure can be used for teaching and training pruposes, and
we provide support with getting you organised.

We assume that the course requirements are such that the interactive cluster
can be used. If these are insufficient, you will need to request a reservation.

[^TODO]: insert some links to the interactvie cluster?

In order to help you out, you need to provide following pieces of information
when you [contact the {{ hpcteam }}]({{ hpc_support_url }}):

* Group moderators and optional UGent course id
* Start and end date
* Optional
  * Share
  * Reservation
  * Software
  * Portal app

## Group moderators

To organise teachers and students, groups are used. Typically the teachers map
to the role of moderator(s), and students are regular members.

The moderator can invite
students as member via their vsc account (the students have to accept the invite);
or the students can invite themself to the group (and moderator has to approve the invites).

You provide us with the vsc account(s) for the moderator(s),
the moderators can manage the members and moderators themself afterwards.

[^TODO]: do we support initial list of participants?

[^TODO]: we control the groupname prefix? or have them all use the same one (unprotected). incl some convntion like academci year


### UGent course id

[^TODO]: check terminology

When teaching a registered UGent course, we can offload the management of the vsc accounts from the students and
the teachers. We do this by creating a vsc account for each registered student that is linked to the course id
(if they do not have an account already). And we then populate the group with the vsc accounts of the students
and the list of moderators. Using this method, you cannot manage the members or moderators yourself:
group members unknown to the course will be considered unregistered students and will be removed from the group.

The created accounts will be accounts without an ssh-key. This allows the students to use e.g. the portal, but if
they require ssh access to the infrastructure, they will have to add one themself.

[^TODO]: what does the sync do? can moderators add moderators themself?

## Start and end date

We require an end date to perform any required cleanup of groups and optional data, apps or reservations.

[^TODO]: can we do some automated cleanup for ugent courses? when the course disappears from AD?

[^TODO]: we need a maximum enddate? max one year after the request?

The start date will be `best-effort`, based on the load of the support team and the requirements you have.
The sooner you make the request, the better.

[^TODO]: do we mention some actual ETA here? like one month upfront?

[^TODO]: when do course of the next academic year appear?

## Share

When required, we can create a directory that is writeable by the moderators and accessible by all
members and moderators. This directory can be used to share e.g. input files with the students.

The data policy for this share is the following: on the enddate, the directory will be made unaccessible
nby anyone, and one year after the enddate it will be removed. When the moderators require anything from
this expired share, they will have to make a request via the support page. We assume that you always have
your own copy of the course data as a starting point for a next course.

[^TODO]: to avoid extra support tickets, we can also make the dir readonly and only accessible by the moderators.

## Reservation

When the resources offered by the interactive cluster are not sufficient for the course, you will need to request
a reservation as well. Indicate the number of nodes and which cluster you need and when you need them
(e.g. the dates of each course). Be aware that students will have no access to the reservation outside the courses.
This might be relevant when requesting a custom application.

## Software

In case the course needs software that is unavailable or needs to be updated,
make a software installation request (see ...), and mention mention the ticket number.

We will try to make sure the software is available as soon as possible, but ideally the courses
rely on software that is already in use (and thus also well tested).

## Portal app

We can create a custom interactive application on the web portal to make the course easier for teachers and students.
The customisation typically locks down the number of options to select for the students, so they don't make mistakes
and slow down the course by e.g. trying to run some application on the wrong cluster.

This custom application is only available to the members of the group.

After the end date this application is removed.

The caveat for the teacher and students is that they don't learn to work with the generic application.
It might be interesting that the generic application form is briefly shown.


# Orchestration Using Heat {#cha:orch-using-heat}

[Heat]{acronym-label="Heat" acronym-form="singular+short"} is the name
of the OpenStack orchestration engine, which can manage complete
configurations of all servers, volumes, users, networks and routers that
make up a cloud application. Instead of managing every component
separately, we can create, start, stop or clean up our complete
application in a single step. In OpenStack, such a collection of
resources is called a [stack]{acronym-label="stack"
acronym-form="singular+short"}.

[Heat]{acronym-label="Heat" acronym-form="singular+short"} has its own
dashboard interface, which you can find under the tab. Official
documentation for Heat and its dashboard interface can be found at the
following locations:

-   [https://docs.openstack.org/heat/\\osversion](https://docs.openstack.org/heat/\osversion){.uri}

-   [https://docs.openstack.org/heat-dashboard/\\osversion](https://docs.openstack.org/heat-dashboard/\osversion){.uri}

## [Heat Orchestration Template]{acronym-label="Heat Orchestration Template" acronym-form="singular+short"}s {#sec:glsh-orch-templ}

A [stack]{acronym-label="stack" acronym-form="singular+short"}'s
resources and their mutual dependencies can be specified in a text file,
called a
[Heat Orchestration Template]{acronym-label="Heat Orchestration Template"
acronym-form="singular+short"} ([hot]{.smallcaps}). The syntax of these
templates conforms to the [yaml]{acronym-label="yaml"
acronym-form="singular+short"} standard, for which many text editors
provide specialized editing modes. The '[Template
Guide](https://docs.openstack.org/heat/\osversion/template_guide)' in
the Heat documentation contains a specification of the [hot]{.smallcaps}
format, as well as information on how to describe the various types of
resources in a template.

[vsc]{.smallcaps} provides some example templates at
[github.com/hpcugent/openstack-templates](https://github.com/hpcugent/openstack-templates),
which can serve as a starting point for your own templates, or as
examples.

The following example describes a stack consisting of a single VM:

::: code
heat_template_version: 2018-08-31

description: This template instantiates a basic VM.

parameters: user_key: type: string label: ssh_user_key description:
Public user ssh key to be injected in the cluster VMs constraints: \[
custom_constraint: nova.keypair \] vm_flavour: type: string label:
vm_flavour description: Flavour for the VM constraints: \[
custom_constraint: nova.flavor \] vm_image: type: string label: vm_image
description: Required VM image constraints: \[ custom_constraint:
glance.image \] user_network: type: string label: user_network
description: Add the required VM network constraints: \[
custom_constraint: neutron.network \]

resources: my_server: type: OS::Nova::Server properties: name: MyServer
metadata: server: master color: red security_groups: \[ default \]
networks: \[ network: get_param: user_network \] key_name: get_param:
user_key image: get_param: vm_image flavor: get_param: vm_flavour
:::

Our example contains four main sections:

`heat_template_version`

:   The [hot]{.smallcaps} specification has evolved since its initial
    release. The key `heat_template_version` indicates the version of
    the syntax used in this template. It's value can be a release date
    or (in recent version) the name of the version.

`description`

:   Providing a description is optional, but recommended.

`parameters`

:   Another optional section, `parameters` allow users to configure
    various properties when instantiating a new stack, without having to
    edit the template itself. A parameter value can be used elsewhere in
    the template using the function `get_param`. In this example, we use
    parameters to choose an SSH key, instance size ("flavor"), image,
    and a network.

`resources`

:   This section contains all the resources used by the Stack. In this
    case, there is just a single VM instance (OS::Nova::Server).

Optional additional sections are , , and .

## The Template Generator {#sec:template-generator}

The Heat dashboard provides a graphical interface where users can draw
templates by dragging resources onto a canvas, and connecting them.
Users can then download a template generated from this interface, or
immediately instantiate it as a stack.

Currently, there are a number of issues with the template generator,
which require manual edits to the generated templates. Therefore, the
template generator is currently not very useful. We will update this
section as soon as these problems are solved.

## Managing stacks {#sec:managing-stacks}

The button in the tab takes you to the overview page where you can
launch, suspend, resume and delete stacks.


![image](img/stacks_overview.png)


The overview page contains a list of all currently existing stacks
(either running or suspended), and buttons to perform the following
actions:

### Launch a stack {#launch-a-stack .unnumbered}

1.  Click to open the following wizard:


    ![image](img/launch_stack_template.png)


2.  Provide a template and --- optionally --- an environment for the
    stack.

    Template Source

    :   You can provide a template using one of the following options:

        File

        :   Provide a local file on your system.

        Direct Input

        :   Enter the template in a text field.

        URL

        :   Provide a [URL]{.smallcaps} to have OpenStack download the
            template from that location.

        In our example, we provide a [URL]{.smallcaps} from the
        repository
        [github.com/hpcugent/openstack-templates](https://github.com/hpcugent/openstack-templates),
        to instantiate the example from section
        [1.1](#sec:glsh-orch-templ){reference-type="ref"
        reference="sec:glsh-orch-templ"}. If you want to provide a
        template directly from GitHub, make sure to provide a "Raw"
        [URL]{.smallcaps}, `https://raw.githubusercontent.com/`....

    Environment Source

    :   Optionally, you can also provide an environment file. This is
        another [yaml]{.smallcaps} file, which contains customizations
        for your Heat templates, such as default values for parameters,
        or custom resource types you have created (see
        '[Environments](https://docs.openstack.org/heat/\osversion/template_guide/environment.html)'
        in the Heat template guide). You can provide a or choose .

3.  If you click , OpenStack will process the template. You can now
    enter a name for the stack, and provide values for all the template
    parameters:


    ![image](img/launch_stack_parameters.png)


4.  Click to instantiate the stack.

### Preview Stack {#preview-stack .unnumbered}

starts a wizard similar to the "Launch Stack" wizard, but completing the
wizard will only make the system perform a sanity check of your
template, without instantiating the stack. If the check passes, you can
inspect the parameters of the stack that would be created. The wizard
does not allow you to enter input parameter values, so any mandatory
input parameters should be provided in an environment.

### Delete Stacks {#delete-stacks .unnumbered}

deletes all selected stacks from the list .

Deleting a stack also deletes all of the resources (volumes, ports)
created by that stack, unless a different policy was set in the property
for those resources (see the '[Resources
section](https://docs.openstack.org/heat/\osversion/template_guide/hot_spec.html#resources-section)'
in the [hot]{.smallcaps} specification).

### More Actions {#more-actions .unnumbered}

The button hides the following additional actions:

::: description
verifies if the resources for selected stacks are still running.

suspends all resources of the selected stacks.

resumes the selected (suspended) stacks.
:::

You can quickly suspend, resume or delete a single stack using the
drop-down menu in the column of the overview. This menu also contains
the option , which allows you to update a Stack by providing a new
template.

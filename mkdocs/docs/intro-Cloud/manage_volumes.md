# Create and manage volumes

An OpenStack Volume is a block storage device which you
attach to instances to enable persistent storage. You can attach a
volume to a running instance or detach a volume and attach it to another
instance at any time. You can also create a snapshot from a volume, or
delete it.

#### Create a volume

1.  Open the Volumes tab and select the Volumes category.

2.  Click **Create Volume**.

    In the dialog box that opens, enter or select the following values.

    - **Volume Name**
    Specify a name for the volume.

    - **Description**
    Optionally, provide a brief description for the volume.

    - **Volume Source**
    Select one of the following options:

        -   No source, empty volume: Creates an empty volume. An empty
            volume does not contain a file system or a partition table.

        -   Snapshot: If you choose this option, a new field for Use
            snapshot as a source displays. You can select the snapshot
            from the list.

        -   Image: If you choose this option, a new field for Use image
            as a source displays. You can select the image from the
            list.

        -   Volume: If you choose this option, a new field for Use
            volume as a source displays. You can select the volume from
            the list. Options to use a snapshot or a volume as the
            source for a volume are displayed only if there are existing
            snapshots or volumes.

    - **Type**
    Select one of the following options:

        -   **tripleo**: This is the default option for the projects, it
            creates the volume in a regular hdd storage pool.

        -   **fastpool** (optional): It creates the volume in a high I/O
            throughput storage pool. Fastpool has its own storage quota
            and it is only accessible by project's request (contact if
            you need more information).

    - **Size (GB)**
    The size of the volume in gibibytes (GiB).

    - **Availability Zone**
    Select the Availability Zone from the list. By default, this
    value is set to the availability zone given by the cloud
    provider (for example, or ). For some cases, it could be .

3.  Click **Create Volume**.

The dashboard shows the volume on the Volumes tab.

#### Attach a volume to an instance

After you create one or more volumes, you can attach them to instances.
You can attach a volume to one instance at a time.

1.  Open the Volumes tab and click Volumes category.

2.  Select the volume to add to an instance and click **Manage Attahments**.

3.  In the Manage Volume Attachments dialog box, select an instance.

4.  Enter the name of the device from which the volume is accessible by
    the instance.

!!! Note

    The actual device name might differ from the volume name because of
    hypervisor settings.

5.  Click **Attach Volume**.

    The dashboard shows the instance to which the volume is now attached
    and the device name.

You can view the status of a volume in the Volumes tab of the dashboard.
The volume is either Available or In-Use.

Now you can mount, format, and use the volume from this instance.

#### Detach a volume from an instance

1.  Open the Volumes tab and select the Volumes category.

2.  Select the volume and click **Manage Attachments**.

3.  Click **Detach Volume** and confirm your changes.

A message indicates whether the action was successful.

#### Create a snapshot from a volume

1.  Open the Volumes tab and select the Volumes category.

2.  Select a volume from which to create a snapshot.

3.  In the Actions column, click **Create Snapshot**.

4.  In the dialog box that opens, enter a snapshot name and a brief
    description.

5.  Confirm your changes.

The dashboard shows the new volume snapshot in Volume Snapshots tab.

#### Edit a volume

1.  Open the Volumes tab and select the Volumes category.

2.  Select the volume that you want to edit.

3.  In the Actions column, click **Edit Volume**.

4.  In the Edit Volume dialog box, update the name and description of
    the volume.

5.  Click **Edit Volume**.

!!! Tip

    You can extend a volume by using the **Extend Volume** option available in
    the **More** dropdown list and entering the new value for volume size.

#### Delete a volume

When you delete an instance, the data in its attached volumes is not
deleted.

1.  Open the Volumes tab and select the Volumes category.

2.  Select the check boxes for the volumes that you want to delete.

3.  Click **Detele Volumes** and confirm your choice.

A message indicates whether the action was successful.


Analysis Reference
==================

ProLint carries out protein-lipid contact analysis and visualization. This
section outlines how to use ProLint for analyzing contact information.

ProLint uses MDTraj to read trajectories and both MDTraj.Trajectory and
MDTraj.Topology objects are used as inputs. ProLint has its own topology classes that
are used to define both Proteins and Lipids in the system. You typically start by loading
your simulation files::

    import mdtraj as md
    import prolint as pl

    t = md.load('system.xtc', top='system.gro')

MDTraj has many ways how you can manipulate the trajectory (e.g. use a stride, remove
periodicity, concatenate trajectories, etc.). ProLint assumes that loaded data contains only
proteins and lipids. As such, systems have to be preprocessed so that water, ions and ligand
are removed before they are read by ProLint. Here we assume that ``t`` is a Martini system
contains only proteins and lipids.

We start by defining the protein and lipid topologies. We define the lipid topology and
select only cholesterols for our analysis::

    lipids = pl.Lipids(t.topology, resolution="martini", lipid_names=['CHOL'])

Next, we define the protein topology::

    p = pl.Proteins(t.topology, resolution="martini")
    proteins = p.system_proteins()

GROMACS coordinate files do not contain protein names and count, so ProLint calculates this information
itself. In the first line, we define the protein topology and in the second line we use it to extract
information about the number and count of all proteins in the system.

Now we use the protein and lipid topologies to calculate contact information. We do this by first
calculating a ProLint.ComputeContacts object::

    contacts = pl.ComputeContacts(t, proteins, lipids)

That's it! Now, when we want to calculate interactions between proteins and lipids, all we have
to do is call the compute_neighbors method, like so::


    contacts.compute_neighbors(t, [60, 70, 80])
    contacts.compute_neighbors(t, range(15, 31), cutoff=0.64, atom_names=[ROH])

This will calculate contact information between proteins and lipids in the system.
For example::

    n = contacts.compute_neighbors(t, [100])
    print (n)
    # {'protein_name': {replicate: {residue: <contact class>}}}
    > {'Protein0': {0: {15: <prolint.LPContacts for residue 15>}}}

    print (n['Protein0'][0][100].contacts)
    # {'lipid': [duration_chol1, duration_chol2, duration_chol3, duration_chol4]}
    > {'CHOL': [62000.0, 156000.0, 212000.0, 18000.0]}

In the above commands, we calculate contacts between residue *100* and cholesterol *ROH* beads. The dictionary
output of ProLint, *n*, contains information for the requested residues for each replicate of each protein in the
system.

ProLint has several helper functions to manipulate contacts. Below are a few examples of how to use them.

A DataFrame of contacts
~~~~~~~~~~~~~~~~~~~~~~~

Creating a Pandas DataFrame is as easy as running the ProLint.contacts_dataframe() function::

    df = pl.contacts_dataframe(n, proteins, t)

ProLint will calculate several contact metrics (e.g. average contact duration, occupancy, etc.). The following
are the metrics supported by default:

.. list-table::
   :widths: 5 10 85
   :header-rows: 1

   * - Keyword
     - Name
     - Description
   * - ``mean``
     - Mean_Duration
     - The average duration of all contacts
   * - ``max``
     - Longest_Duration
     - The longest duration (averaged if more than 1 protein).
   * - ``sum``
     - Sum_of_all_Contacts
     - The total sum of all contacts.
   * - ``lnr``
     - Lipid_Number
     - The average number of lipids in contact (the total number of contacts
       normalized with respect to the number of frames).
   * - ``nlnr``
     - Normalized_Lipid_Number
     - Lipid_Number normalized with respect to the number of different lipids
       (e.g. number of different cholesterols).
   * - ``occ``
     - Occupancy
     - For each frame, we give a value of 0 if no lipid of interest is in
       contact with the residue and 1 otherwise. Occupancy is then: sum_of_all_1s / nr_of_frames.

You can easily define your own custom metrics.


Retrieving contact information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The contact dictionary output of ProLint is easy to understand and use. For convenience, however, there are
two helper functions you can use to get contact information for a particular residue::

    pl.retrieve_contacts(n, 20)
    pl.retrieve_contacts_flat(n, 20)


Now let's go over the plotting functionality supported by ProLint described in the :doc:`visualization`.
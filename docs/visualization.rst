Visualization Reference
=======================

ProLint carries out protein-lipid contact analysis and visualization. This
section outlines how to use ProLint for visualizing contact information.

In contrast to analysis, data visualization is more variable and different users will
have different preferences for how to best display results. ProLint does not attempt to
be a full-fledged visualization library. Instead, the main objective is to allow users to
quickly and without hassle obtain valuable insight on protein-lipid contact details in
their simulated systems. To do this, ProLint uses dedicated libraries that do that heavy
lifting in the background. All visualization tools supported by ProLint are interactive and
are intended to give users complete access to their data.

A scatter plot of data points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have a DataFrame of contact information (e.g. by running ProLint.contacts_dataframe()), you
can then visualize the data like so::

    pl.show_points(df)

Which, when run in a JupyterLab environment, will give an output like this:

.. image:: /images/points.png


Metric comparison
~~~~~~~~~~~~~~~~~

Because by default ProLint calculates several contact metrics and users may add custom definitions,
you may want to see how these parameters compare against each other. In particular, this becomes
important when you have two or more residues that interact strongly with a lipid, and you want to
compare their interactions against each other. You can do this using ProLint by typing::


    pl.show_radar(df)

This will normalize all contact metrics (there should be at least three present) and use a radar plot
for the visualization:

.. image:: /images/radar.png

Distance calculations
~~~~~~~~~~~~~~~~~~~~~

Another very important calculation that is very commonly done in lipid-protein interactions is measuring the
distance between a residue and a lipid as a function of simulation time. This gives you a clear idea if the
lipid is interacting specifically or not. To calculate the distance between a lipid and a residue in ProLint,
all you have to do is, first compute the distances and then visualize them::

    dist = contacts.contact_distances(t, proteins[0], [10, 11], 'CHOL', 'ROH')
    pl.show_distances(dist)

In the first command, we supply the MDTraj.Trajectory (t) and speciy the residues (10 & 11) of the protein (proteins[0])
along with the bead/atom ('ROH') of the lipid ('CHOL') that we want to measure distances. These are then visualized
using a dedicated application. You do not need any prior knowledge of the interactions for this calculation and
you don't need to compute neighbors at all.

You'll get an output like the following:

.. image:: /images/distance.png

3D Viewer
~~~~~~~~~

NGL Viewer based application to visualize contact metrics as contact heatmaps that are projected on the
surface of the protein. You visualize it in ProLint using::

    pl.show_contact_projection(t, df.Longest_Duration.to_list(), proteins[0])

In the first argument we give information about the topology of the system, in the second we provide
the contacts and in the third argument we tell ProLint which protein to use. We can also use the
ngl_repr argument to specify the structure representation. For example, if we use options like:
'surface', 'cartoon', or 'ball+stick' we get the following outputs:

.. image:: /images/projection.png

Please note that ProLint uses the nglview library. So this application is intendent to cover a majority
of use cases when it comes to visualizing contacts with lipids, but obviously it is not intendent to be
comprehensive or provide many options.

Graph Network
~~~~~~~~~~~~~

Lipids and proteins are represented as nodes and their interactions with each other as edges.
The width of the latter corresponds to the degree of the underlying interaction. To visualize
lipid-protein interactions as a graph network you execute the following commands::

    pl.network(lipids, df, df.columns[1], grouped=True, filename='network.json')
    pl.show_network('network.json')

In the first command, we store the interactions in a json file and then visualize them in the second
command. This will give an output like this:

.. image:: /images/network.png

The size of lipid nodes corresponds to the ratio of that particular lipid group in simulated systems.
The size of residue nodes corresponds to the relative content of each residue in the protein being shown.



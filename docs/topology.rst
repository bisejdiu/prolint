Topology Reference
====================

ProLint uses MDTraj to create two internal topologies. One for proteins and one for
the lipids in the system. These topologies are stored in the :class:`prolint.Proteins`
and :class:`prolint.Lipids` classes. Because systems can have multiple proteins and in
lipid-protein interaction studies they quite often do, :class:`prolint.Proteins` uses
:class:`prolint.Protein` to store information about individual proteins in the system.
Please be aware of this distinction when using ProLint.::

    p = pl.Proteins(t.topology, resolution="martini")
    proteins = p.system_proteins()

The first command creates an object that stores information about all proteins. In the second
command we retrieve information about individual proteins in the system.


Internal representation
-----------------------

.. currentmodule:: prolint
.. autosummary::
    :toctree: api/generated/

    Lipids
    Proteins
    ComputeContacts
    retrieve_contacts
    retrieve_contacts_flat
    contacts_dataframe

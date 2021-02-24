Graphics Reference
====================

Using the visualization module of ProLint usually requires a pandas DataFrame object. ::

    >>> n = contacts.compute_neighbors(t)
    >>> df = pl.contacts_dataframe(n, proteins, t)

ProLint provides several visualizaiton application that will display various facets of
lipid-protein contacts.

Internal representation
-----------------------

.. currentmodule:: prolint
.. autosummary::
    :toctree: generated/

    show_points
    show_radar
    show_distances
    show_contact_projection
    show_network

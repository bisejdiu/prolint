About
=====

``ProLint`` is a lightweight python library that has **four** core objectives:

* Powerful and customizable analysis of protein-lipid contacts
* Allow for quick and easy insight into simulation data
* Increase data sharing and accessibility
* Automation of protein-lipid contact generation

Analysis of protein-lipid contacts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Currently, the time it takes to analyze and interpret data usually exceeds the time
to set up and perform Molecular Dynamics (MD) Simulations. Add to this the
continuing trend of increased system sizes, simulated for longer time scales and
the need for a much bigger set of proteins, it becomes clear how analysis and
visualization of protein-lipid contacts can become a significant bottleneck. ProLint
bridges this gap between data generation and obtaining insight about relevant interactions.
To learn how ProLint analyses contacts, see :doc:`analysis`.

Quick and easy insight
~~~~~~~~~~~~~~~~~~~~~~
ProLint comes with a built-in visualization library that quickly and effortlessly displays
protein-lipid interactions. It uses modern visualization libraries like bokeh, d3.js,
nglviewer to do the heavy-lifting and allows the user to quickly see the presence (or absence) of
protein-lipid contacts in the simulated system.
To learn how to visualization interactions, see :doc:`visualization`.

Data sharing and accessibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Papers studying protein-lipid contacts are closed systems. They use widely different analyses
protocols and visualization tools that make it difficult to compare results across different
studies. Getting the original data that was used in published works is also a challenge.
ProLint allows for contact information to be extracted from simulated systems and stored
in small files that can be easily shared and made publicly available.

Automation
~~~~~~~~~~
It will become increasingly important to automate the generation of protein-lipid contacts for
any arbitrary protein. Such databases will be of immense importance to the scientific community.
ProLint is perfectly suited to be used as part of such automation pipelines.


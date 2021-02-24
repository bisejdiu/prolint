class SystemTopology(object):

    def __init__(self, topology, resolution="martini"):

        if resolution == "martini":
            lipid_indices = topology.select("all and not (name BB or (name =~ 'SC[1-9]'))")
            proteins_indices = topology.select("name BB or (name BB or (name =~ 'SC[1-9]'))")

        self.topology = topology
        self.dataframe = topology.to_dataframe()[0]
        self.l_indices = lipid_indices
        self.p_indices = proteins_indices
        self.pdf = self.dataframe.iloc[proteins_indices]
        self.ldf = self.dataframe.iloc[lipid_indices]


    def __str__(self):
        return "placeholder."

    def __repr__(self):
        return "placeholder."


class Lipids(SystemTopology):

    def __init__(self, topology, mdtraj_selection_string=''):

        super().__init__(topology)

        if mdtraj_selection_string != '':
            self.l_indices = topology.select(mdtraj_selection_string)

    def lipid_names(self):
        return self.dataframe.iloc[self.l_indices].resName.unique()


class Protein(object):

    def __init__(self, name):
        self.name = name
        self.counter = 1
        self.dataframe = []
        self.beads = 0
        self.n_residues = 0

    def get_indices(self, df=None):
        """
        Return indices from a given residue array.
        """
        if df is None:
            if len(self.dataframe) > 1:
                print ("Object has more than one dataframe. Using the first one.")
            else:
                print ("Using the available dataframe")
            df=self.dataframe[0]

        residues = df[df.name == "BB"].resSeq.to_list()
        indices = [df[df.resSeq == x].index.to_numpy() for x in residues]

        return indices

    def __str__(self):
        return "<prolint.Protein containing {} replicate(s) of {} and {} beads each>".format(self.counter, self.name, self.n_residues)

    def __repr__(self):
        return "<prolint.Protein containing {} replicate(s) of {} and {} beads each>".format(self.counter, self.name, self.n_residues)


class Proteins(SystemTopology):

    def __init__(self, topology):

        super().__init__(topology)

        # Get start and end indices of proteins in the system.
        # The assumption here is that proteins are ordered and the start residue of the next
        # protein is always smaller than the last residue of the previous protein.
        resseq = self.pdf.resSeq.to_list()
        p0 = resseq[0]
        # system_proteins contains the start and end indices of all proteins.
        fi_li = []
        fi = 0
        for li, p in enumerate(resseq):
            if p < p0:
                fi_li.append((fi, li-1))
                fi = li
            p0 = p
        fi_li.append((fi, li))

        self.fi_li = fi_li

    def system_proteins(self):

        c = 0
        proteins = []
        # Two proteins are the same if residue number and all beads are equal between them.
        for values in self.fi_li:

            # first and last index
            fi = values[0]
            li = values[1]

            # Get the data for the current protein.
            current_protein_df = self.pdf[(self.pdf.index >= fi) & (self.pdf.index <= li)]
            curr_len = len(current_protein_df)
            curr_names = current_protein_df.name.to_list()

            new_protein = True
            for pc in proteins:
                if curr_names == pc.beads:
                    pc.counter += 1
                    pc.dataframe.append(current_protein_df.copy())
                    new_protein = False

            if new_protein:
                protein = Protein(f'Protein{c}')
                protein.dataframe.append(current_protein_df.copy())
                protein.beads = curr_names
                protein.n_residues = curr_len
                proteins.append(protein)

            c += 1

        return proteins

    def __str__(self):
        return "class storing information on system proteins"

    def __repr__(self):
        return "class storing information on system proteins"
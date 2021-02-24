import numpy as np
import pandas as pd
import mdtraj as md
from collections import defaultdict, Counter
from prolint.utils.martinilipids import martini_lipids, lipid_species
# from prolint.core.systemtopology import Lipids

class ComputeContacts(object):

    def __init__(self, t, proteins, lipids, centrality="average"):

        # TODO:
        # assert that proteins is a list
        # Should support contact calculation between a specific residue and lipid (not just all residues only)

        self.frames = t.n_frames
        self.timestep = t.timestep
        self.t_unit = "unit"
        self.dt = None

        self.proteins = proteins
        self.lipids = lipids


    def compute_neighbors(self, t, cutoff=0.7, only_beads=[], grouped=True):


        if grouped:
            PLASMA_LIPIDS = martini_lipids(self.lipids.lipid_names())
        else:
            PLASMA_LIPIDS = {}
            for lip in self.lipids.lipid_names():
                PLASMA_LIPIDS[lip] = [lip]


        if len(only_beads) == 0:
            haystack_indices = self.lipids.l_indices
            lipid_names = self.lipids.lipid_names()
        else:
            df = self.lipids.ldf
            haystack_indices = list(df[df.name.isin(only_beads)].index)
            lipid_names = df[df.name.isin(only_beads)].resName.unique()

        if grouped:
            PLASMA_LIPIDS = martini_lipids(lipid_names)
        else:
            PLASMA_LIPIDS = {}
            for lip in lipid_names:
                PLASMA_LIPIDS[lip] = [lip]


        prolint_contacts = defaultdict(dict)
        for protein in self.proteins:
            for pc in np.arange(protein.counter):
                residue_indices = protein.get_indices(protein.dataframe[pc])
                per_residue_results = {}
                for residue, idx in enumerate(residue_indices):

                    print ("Working on: {}".format(residue))
                    md_out = md.compute_neighbors(t, cutoff, idx, haystack_indices=haystack_indices)
                    per_residue_results[residue+1] = LPContacts(t.topology, md_out, PLASMA_LIPIDS).contacts

                    # if residue >= 2:
                    #     break

                prolint_contacts[protein.name][pc] = per_residue_results

        return dict(prolint_contacts)


class LPContacts(object):
    # Requires import of martini_lipids & lipid_species

    def __init__(self, topology, mdtraj_contacts, PLASMA_LIPIDS):

        all_lipid_name_id = {}
        contacts = {}
        for index, values in enumerate(mdtraj_contacts):

            lipid_name_id = {}
            for value in values:

                bead = topology.atom(int(value))
                lipid_name_id[bead.residue.resSeq] = lipid_species(bead.residue.name, PLASMA_LIPIDS)

            for k, v in lipid_name_id.items():
                if all_lipid_name_id.get(v):
                    all_lipid_name_id[v].append(k)
                else:
                    all_lipid_name_id[v] = [k]

        for k in PLASMA_LIPIDS.keys():
            if all_lipid_name_id.get(k):
                contacts[k] = list((Counter(all_lipid_name_id[k]).values()))
            else:
                contacts[k] = [0]

        self.contacts = contacts

def standard_contact_metrics(cs, co=0):

    d = {}
    for c in cs:
        for k, v in c.items():
            v = np.array(v)
            if d.get(k):
                d[k].append(v)
            else:
                d[k] = [v]

    metric_results = {}
    contact_results = {}
    for lipid, contacts in d.items():

        metric_results[lipid] = {}

        means, maximums, sums = [], [], []

        for contact in contacts:
            contact = contact[contact>co]

            if len(contact) == 0:
                means.append(0)
                maximums.append(0)
                sums.append(0)

            else:
                means.append(contact.mean())
                maximums.append(contact.max())
                sums.append(contact.sum())

        metric_results[lipid]["mean"] = (np.mean(means), np.std(means))
        metric_results[lipid]["maximum"] = (np.mean(maximums), np.std(maximums))
        metric_results[lipid]["sum"] = (np.mean(sums), np.std(sums))

    return metric_results


def pandas_contact_metrics(c, p, co=0):

    pandas_input = defaultdict(dict)
    RESULTS = {
        "Mean":[],
        "Maximum":[],
        "Sum":[],
        "Protein":[],
        "Lipids":[],
        "Radius":[],
        "Sequence":[],
        "ResName":[]
    }

    proteins = list(c.keys())
    for protein in proteins:
        replicates = list(c[protein].keys())
        residues = list(c[protein][0].keys())

        df = [x.dataframe[0] for x in p if x.name == protein][0]

        for residue in residues:
            all_residue_contacts = [c[protein][x][residue] for x in replicates]
            metrics = standard_contact_metrics(all_residue_contacts)

            pandas_input[protein][residue] = metrics

            for lipid, values in metrics.items():
                RESULTS["Mean"].append(values["mean"][0])
                RESULTS["Maximum"].append(values["maximum"][0])
                RESULTS["Sum"].append(values["sum"][0])
                RESULTS["Protein"].append(protein)
                RESULTS["Lipids"].append(lipid)
                RESULTS["Radius"].append(0.7)
                RESULTS["Sequence"].append(residue)
                RESULTS["ResName"].append(df[df.resSeq == residue].resName.unique()[0])

    return pd.DataFrame(RESULTS)



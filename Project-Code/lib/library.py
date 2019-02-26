import os
from Bio import PDB
import numpy as np
import urllib
import matplotlib.pyplot as plt


def write_to_file(file_name, data, mode):
    with open(file_name, mode) as file:
        file.write(data + "\n")


def write_stream(filename, data_stream):
    with open(filename, "w+") as handle:
        handle.write(data_stream.read())
        data_stream.close()


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_ca_distnaces_from_pdb(path, length, chain_id=None):
    parser = PDB.PDBParser()
    chain = parser.get_structure(id='temp', file=path)[0]
    if chain_id is not None:
        chain = parser.get_structure(id='temp', file=path)[0][chain_id]
    distance_matrix = np.zeros((length, length))

    for r1, residue1 in enumerate(chain):
        for r2, residue2 in enumerate(chain):
            if residue1 != residue2:
                # compute distance between CA atoms
                try:
                    distance = residue1['CA'] - residue2['CA']
                    distance_matrix[r1][r2] = distance
                except KeyError:
                    continue

    return distance_matrix


def download_pdb(save_folder, hit_id, chain_id):
    file_name = "{}_{}.pdb".format(hit_id, chain_id)
    if not os.path.isfile(os.path.join(save_folder, file_name)):
        try:
            urllib.request.urlretrieve("http://files.rcsb.org/view/" + hit_id.lower() + ".pdb",
                                       os.path.join(save_folder, file_name))
        except:
            print("PDB {} not found.".format(hit_id))
            return False

    return True


def get_fasta_for_id(save_folder, hit_id, chain_id):
    file_name = "{}_{}.fasta".format(hit_id, chain_id)
    if not os.path.isfile(os.path.join(save_folder, file_name)):
        url = "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=fastachain&compression=NO&structureId={}&chainId={}"\
            .format(hit_id, chain_id)

        dest = os.path.join(save_folder, file_name)
        urllib.request.urlretrieve(url, dest)


def output_distance_matrix(save_folder, distance_matrix, prefix=None):
    map = plt.imshow(distance_matrix, cmap='gray')
    plt.colorbar(map)
    plt.savefig(os.path.join(save_folder, "{}distance_matrix.png".format((prefix + "_") if prefix else "")))
    plt.close()
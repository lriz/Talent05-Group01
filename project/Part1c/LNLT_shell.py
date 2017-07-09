import numpy as np
import json
import argparse
from single_particle_state_class import single_particle_state
from collections import OrderedDict

def shell_configurations():
    return [{'name': '0s1/2', 'N': 0},
            {'name': '0p3/2', 'N': 1},
            {'name': '0p1/2', 'N': 1},
            {'name': '0d5/2', 'N': 2},
            {'name': '1s1/2', 'N': 2},
            {'name': '0d3/2', 'N': 2},
            {'name': '0f7/2', 'N': 3},
            {'name': '1p3/2', 'N': 3},
            {'name': '0f5/2', 'N': 3},
            {'name': '1p1/2', 'N': 3},
            {'name': '0g9/2', 'N': 4}]

#TODO: add check shell configuration to see if we ordered the shell in the correct order. e.g. s-d-shell
#TODO: 0d5/2 should have P=1, 1s1/2 should have P=2, 0d3/2 should have P=3.

def choose_iter(elements, length):
    """
    Generate all possible elements from a list given a wanted length. e.g. number of states and number of particles.
    :param elements: the number of states.
    :param length: the number of particles.
    :return:
    """
    for i in xrange(len(elements)):
        if length == 1:
            yield (elements[i],)
        else:
            for next in choose_iter(elements[i+1:len(elements)], length-1):
                yield (elements[i],) + next
def choose(l, k):
    return list(choose_iter(l, k))

# Argparse: insert arguments to code using the command line.
parser = argparse.ArgumentParser(description='None')  # Generate a parser.
parser.add_argument('-f','--file',help='a json input file name for the program', type=str,required=True)  # Define a command line operation.
args = parser.parse_args()

folder_name = 'input_files/'  # Folder of input files.

with open("".join((folder_name,args.file))) as data_file:
        input_dict = json.load(data_file)  # A dictionary. Keys are the name of input, values are the value of input.

shell_configurations_list = shell_configurations()

# Ordering the dictionary according to P values.
input_dict["shell-configuration P-levels"] = OrderedDict(sorted(input_dict["shell-configuration P-levels"].iteritems(), key=lambda x: x[0]))
all_sps_list = []
sps_index = 1
for p_level_index in input_dict["shell-configuration P-levels"].keys():
    level_name = input_dict["shell-configuration P-levels"][p_level_index]["name"]
    N_number = [shell['N'] for shell in  shell_configurations_list  if shell['name'] == level_name][-1] #TODO: check that not empty.
    j_total = input_dict["shell-configuration P-levels"][p_level_index]["2J-total"]
    for m_j in range(-j_total, j_total+1, 2):
        all_sps_list.append(single_particle_state(p_level_index,
                                                     N_number,
                                                     input_dict["shell-configuration P-levels"][p_level_index]["angular momentum"],
                                                     j_total,
                                                     m_j,
                                                     sps_index))
        sps_index += 1

print all_sps_list
print
print "{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}".format("i", "p", "N", "L", "2J", "2M_J")
print "".join((" ","-"*34))
for sps in all_sps_list:
    print "{:>3} || {:>2} || {:>2} || {:>2} || {:>2} || {:>3}".format(sps.index, sps.p, sps.n, sps.l, sps.j, sps.m_j)

sps_list_m_broken = list([list(x) for x in choose_iter(all_sps_list, input_dict["number of particles"])])
print sps_list_m_broken


sps_list_m_scheme = []
for sps in sps_list_m_broken:
    sps_temp_dict = OrderedDict()
    for p in input_dict["shell-configuration P-levels"]:
        sps_p_list = []
        for i in sps:
            if i.get_p() == p:
                sps_p_list.append(i)
        sps_temp_dict[p] = sps_p_list
    sps_temp_dict = OrderedDict((k, v) for k, v in sps_temp_dict.iteritems() if v)
    m_bool = True
    for p, value in sps_temp_dict.iteritems():
        if sum([v.get_m_j() for v in value]) == input_dict["shell-configuration P-levels"][p]["M-total"]:
            continue
        else:
            m_bool = False
    if m_bool:
        sps_list_m_scheme.append(sps)

print
print sps_list_m_scheme



"""
sps_temp_list = []
for i in sps:
    sps_temp_list.append(i)
    for k in sps[sps.index(i)+1 :]:
        if k.get_p() == i.get_p():
            sps_temp_list.append(k)
"""







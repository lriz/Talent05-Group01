import argparse

isotopes_names = {8:'o', 9:'f'}

def main():
    parser = argparse.ArgumentParser(description='None')
    parser.add_argument('-pr','--protons_number',help='number of protons.', type=int,required=True)
    parser.add_argument('-A','--nucleons_number',help='number of nucleons.', type=int,required=True,nargs=3,metavar=("init","fin","leap"))
    parser.add_argument('-j','--j_values',help='desired j values.', type=str,required=True,nargs=3,metavar=("init","fin","leap"))
    parser.add_argument('-p','--parity',help='choice of parity.', type=str,required=True,default=1,choices=["0","1","2"])
    parser.add_argument('-s','--states',help='the number of states we want to use.', type=int,required=False,default=4)
    parser.add_argument('-in','--interaction_name',help='the name of the intraction used.', type=str,required=False)
    parser.add_argument('-dn','--directory_name',help='the name of the directory where the calculations are at.', type=str,required=False)
    args = parser.parse_args()

    directory_name = args.directory_name
    nucleons_number = args.nucleons_number
    #o_19b.lpt
    nucleons_number[1]+=1  # For 'range' function.
    for a in range(*nucleons_number):
        file_isotope = open( ''.join((directory_name, isotopes_names[args.protons_number], str(a), '_',
                                      args.interaction_name,'/',
                                      isotopes_names[args.protons_number], '_', str(a), args.interaction_name[-1], '.lpt')),'rb')

if __name__ == '__main__':
    main()

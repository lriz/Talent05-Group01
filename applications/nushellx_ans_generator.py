import argparse

def main():
    parser = argparse.ArgumentParser(description='None')
    parser.add_argument('-n','--isotope_name',help='insert the isotope name.', type=str,required=True)
    parser.add_argument('-c','--calculation_choice',help='which kind of calculation to perform.', type=str,default="lpe",required=True,choices=["lpe","den"])
    parser.add_argument('-ns','--number_of_states',help='number of states in lpe files.', default=0, type=str,required=False)
    parser.add_argument('-ms','--model_space',help='the wanted model space.', type=str,required=True)
    parser.add_argument('-r','--restrictions',help='restrictions for model space.', default="n", type=str,required=False)
    parser.add_argument('-i','--interaction',help='type of interaction.', type=str,required=True)
    parser.add_argument('-pr','--protons_number',help='number of protons.', type=str,required=True)
    parser.add_argument('-A','--nucleons_number',help='number of nucleons.', type=str,required=True)
    parser.add_argument('-j','--j_values',help='desired j values.', type=str,required=True,nargs=3)
    parser.add_argument('-p','--parity',help='choice of parity.', type=str,required=True,default=1,choices=["0","1","2"])
    parser.add_argument('-op','--option',help='endingoption.', type=str,required=False,default="st",choices=["st"])
    args = parser.parse_args()

    ans_file = open(''.join((args.isotope_name,args.interaction,'.ans')),'wb')
    lines_list = []
    lines_list.append("--------------------------------------------------")
    lines_list.append("{},   {:<3}           ! option (lpe or lan), neig (zero=10)".format(args.calculation_choice,args.number_of_states))
    lines_list.append("{}                   ! model space (*.sp) name (a8)".format(args.model_space))
    lines_list.append("n                    ! any restrictions (y/n)".format(args.restrictions))
    lines_list.append("{}                 ! interaction (*.int) name (a8)".format(args.interaction))
    lines_list.append("  8                  ! number of protons".format(args.protons_number))
    lines_list.append(" 19                  ! number of nucleons".format(args.nucleons_number))
    lines_list.append(" {:<3}, {:<3}, {:<3},      ! min J, max J, del J".format(*args.j_values))
    lines_list.append("  2                  ! parity (0 for +) (1 for -) (2 for both)".format(args.parity))
    lines_list.append("--------------------------------------------------")
    lines_list.append("st                   ! option".format(args.option))
    ans_file.write("\n".join(lines_list))
if __name__ == '__main__':
    main()
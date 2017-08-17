

def jnom(j):
    if j%2 == 0:
        return j/2
    else:
        return j

def jden(j):
    if j%2 == 0:
        return ""
    else:
        return "/2"

def shell_output(shell):
    l_nots=['s','p','d','f']+map(chr,xrange(ord('g'),ord('z')+1))
    return "{}{}_[{}{}]".format(shell.get_n(),
                                l_nots[shell.get_l()],
                                jnom(shell.get_j()),
                                jden(shell.get_j()))

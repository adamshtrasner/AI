import sys
from itertools import product


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"
    # Writing the propositions

    # d_i-ON-p_j (disk i on peg j)
    domain_file.write('Propositions:\n')
    for prod in product(disks, pegs):
        domain_file.write(f"{prod[0]}-ON-{prod[1]} ")

    # d_i-ON-d_j (disk i on top of disk j)
    for i in range(len(disks)):
        for j in range(i+1, len(disks)):
            domain_file.write(f"{disks[i]}-ON-{disks[j]} ")

    # d_i_top (disk i is the up-most disk on a certain peg)
    for disk in disks:
        domain_file.write(f"top_{disk} ")

    # avail_p_j (peg j is available - either empty or the top disk is not the smallest one)
    for peg in pegs:
        domain_file.write(f"avail_{peg} ")

    # Writing the actions
    domain_file.write('\nActions:\n')

    # MOVE_d_i_p_j-p_k (Move disk i from peg j to peg k)
    for prod in product(disks, pegs, pegs):
        if prod[1] != prod[2]:
            domain_file.write(f"Name: MOVE_{prod[0]}_{prod[1]}-{prod[2]}\n")
            domain_file.write(f"pre: top_{prod[0]} avail_{prod[2]} {prod[0]}-ON-{prod[1]}\n")
            domain_file.write(f"add: avail_{prod[1]} {prod[0]}-ON-{prod[2]}\n")
            domain_file.write(f"delete: avail_{prod[2]} {prod[0]}-ON-{prod[1]}\n")

    for prod in product(disks, disks, pegs):
        if prod[0] != prod[1]:
            # MOVE_d_i_d_j-p_k (Move disk i which is on top of disk j to peg k)
            domain_file.write(f"Name: MOVE_{prod[0]}_{prod[1]}-{prod[2]}\n")
            domain_file.write(f"pre: top_{prod[0]} avail_{prod[2]} {prod[0]}-ON-{prod[1]}\n")
            domain_file.write(f"add: top_{prod[1]} {prod[0]}-ON-{prod[2]}\n")
            domain_file.write(f"delete: avail_{prod[2]} {prod[0]}-ON-{prod[1]}\n")

            # MOVE_p_k_d_i-d_j (Move disk i from peg k to another peg where disk j is on top)
            domain_file.write(f"Name: MOVE_{prod[2]}_{prod[1]}-{prod[2]}\n")
            domain_file.write(f"pre: top_{prod[1]} top_{prod[2]} {prod[1]}-ON-{prod[0]}\n")
            domain_file.write(f"add: avail_{prod[0]} {prod[1]}-ON-{prod[2]}\n")
            domain_file.write(f"delete: top_{prod[2]} {prod[1]}-ON-{prod[0]}\n")

    # MOVE_d_i_d_j-d_k (Move disk i which is on top of disk j to a peg where disk k is on top of it)
    for prod in product(disks, disks, disks):
        if prod[1] != prod[2]:
            domain_file.write(f"Name: MOVE_{prod[0]}_{prod[1]}-{prod[2]}\n")
            domain_file.write(f"pre: top_{prod[0]} top_{prod[2]} {prod[0]}-ON-{prod[1]}\n")
            domain_file.write(f"add: top_{prod[1]} {prod[0]}-ON-{prod[2]}\n")
            domain_file.write(f"delete: top_{prod[2]} {prod[0]}-ON-{prod[1]}\n")

    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"
    # Initial state
    problem_file.write("Initial state: ")

    # Every disk is on peg 0
    for disk in disks:
        problem_file.write(f"{disk}-ON-p_0 ")

    # All disks are on top of each other in ascending order of sizes
    for i in range(n_-1):
        problem_file.write(f"d_{i}-ON-d{i+1} ")

    # disk 0 is the top disk
    problem_file.write(f"top_d_0 ")

    # All pegs except peg 0 are available
    for j in range(1, m_):
        problem_file.write(f"avail_p_{j} ")

    # Goal state
    problem_file.write("\nGoal state: ")

    # Every disk is in the last peg
    for i in range(n_):
        problem_file.write(f"d_{i}-ON-p{m_ - 1}")

    # All disks are on top of each other in ascending order of sizes
    for i in range(n_-1):
        problem_file.write(f"d_{i}-ON-d{i+1} ")

    # disk 0 is the top disk
    problem_file.write(f"top_d_0 ")

    # All pegs except last peg are available
    for j in range(m_ - 1):
        problem_file.write(f"avail_p_{j} ")

    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)

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
    for i in range(n_):
        for j in range(i+1, n_):
            domain_file.write(f"{disks[i]}-ON-{disks[j]} ")

    # d_i_top (disk i is the up-most disk on a certain peg)
    for disk in disks:
        domain_file.write(f"top_{disk} ")

    # avail_p_j (peg j is available - either empty or the top disk is not the smallest one)
    for peg in pegs:
        domain_file.write(f"avail_{peg} ")

    # Writing the actions
    domain_file.write('\nActions:\n')

    for i in range(n_):
        for j in range(i + 1, n_):
            for k in range(i + 1, n_):
                if j != k:
                    # MOVE_d_i_d_j-d_k (Move disk i which is on top of disk j to be on top of disk k in another peg)
                    domain_file.write(f"Name: MOVE_{disks[i]}_{disks[j]}-{disks[k]} \n")
                    domain_file.write(f"pre: top_{disks[i]} top_{disks[k]} {disks[i]}-ON-{disks[j]} \n")
                    domain_file.write(f"add: top_{disks[j]} {disks[i]}-ON-{disks[k]} \n")
                    domain_file.write(f"delete: top_{disks[k]} {disks[i]}-ON-{disks[j]} \n")

            for p_k in pegs:
                # MOVE_d_i_d_j-p_k (Move disk i which is on top of disk j to peg k)
                domain_file.write(f"Name: MOVE_{disks[i]}_{disks[j]}-{p_k} \n")
                domain_file.write(f"pre: top_{disks[i]} avail_{p_k} {disks[i]}-ON-{disks[j]} \n")
                domain_file.write(f"add: top_{disks[j]} {disks[i]}-ON-{p_k} \n")
                domain_file.write(f"delete: avail_{p_k} {disks[i]}-ON-{disks[j]} \n")

        for p_j in pegs:
            for k in range(i + 1, n_):
                # MOVE_d_i_p_j-d_k (Move disk i from peg k to be on top of disk j in another peg)
                domain_file.write(f"Name: MOVE_{disks[i]}_{p_j}-{disks[k]} \n")
                domain_file.write(f"pre: top_{disks[i]} top_{disks[k]} {disks[i]}-ON-{p_j} \n")
                domain_file.write(f"add: avail_{p_j} {disks[i]}-ON-{disks[k]} \n")
                domain_file.write(f"delete: top_{disks[k]} {disks[i]}-ON-{p_j} \n")

            for p_k in pegs:
                if p_j != p_k:
                    # MOVE_d_i_p_j-p_k (Move disk i from peg j to empty peg k)
                    domain_file.write(f"Name: MOVE_{disks[i]}_{p_j}-{p_k} \n")
                    domain_file.write(f"pre: top_{disks[i]} avail_{p_k} {disks[i]}-ON-{p_j} \n")
                    domain_file.write(f"add: avail_{p_j} {disks[i]}-ON-{p_k} \n")
                    domain_file.write(f"delete: avail_{p_k} {disks[i]}-ON-{p_j} \n")

    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"
    # Initial state
    problem_file.write("Initial state: ")

    # Largest disk on peg 0
    problem_file.write(f"{disks[n_-1]}-ON-p_0 ")

    # All disks are on top of each other in ascending order of sizes
    for i in range(n_-1):
        problem_file.write(f"{disks[i]}-ON-{disks[i+1]} ")

    # disk 0 is the top disk
    problem_file.write(f"top_d_0 ")

    # All pegs except peg 0 are available
    for j in range(1, m_):
        problem_file.write(f"avail_{pegs[j]} ")

    # Goal state
    problem_file.write("\nGoal state: ")

    # Largest disk on peg (m_-1)
    problem_file.write(f"{disks[n_ - 1]}-ON-p_{m_-1} ")

    # All disks are on top of each other in ascending order of sizes
    for i in range(n_-1):
        problem_file.write(f"{disks[i]}-ON-{disks[i+1]} ")

    # disk 0 is the top disk
    problem_file.write(f"top_d_0 ")

    # All pegs except last peg are available
    problem_file.write(f"{disks[n_-1]}-ON-{pegs[m_-1]} ")

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

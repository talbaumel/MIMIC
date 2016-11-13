import argparse

parser = argparse.ArgumentParser(description='Construct a file of the codes with their route.')
parser.add_argument('-codes', default='/home/datasets/MIMIC/MIMIC2/all_mimic2_codes', help='File location of icd codes.')
parser.add_argument('-icd9_parent2child', default='/home/datasets/MIMIC/ICD9/ICD9_parent_child_relations',
                    help='File location of the ICD9 parent child mapping.')
parser.add_argument('-output', default='/home/datasets/MIMIC/MIMIC2/all_mimic2_codes_with_route',help='output file name')
args = parser.parse_args()

def create_child2parent_tree(file):
    child2parent = dict()

    with open(file,'r') as in_fd:
        for line in in_fd:
            line_args = line.strip().split('\t')
            child2parent[line_args[1]] = line_args[0]
    return child2parent


def find_route(child2parent,code1):
    code = code1
    if code == '719.70':
        code = '719.7'
    route = [code]
    ancestor = code
    while ancestor!='@':
        if code not in child2parent.keys():
            return None
        ancestor = child2parent[ancestor]
        route.append(ancestor)
    route.reverse()
    return route


child2parent = create_child2parent_tree(args.icd9_parent2child)
with open(args.output,'w') as out_fd:
    with open(args.codes,'r') as in_fd:
        for line in in_fd:
            code = line.strip()
            route = find_route(child2parent,code)
            if route!=None:
                out_fd.write(code + '\t' + ','.join(route) + '\n')
            else:
                print(code)

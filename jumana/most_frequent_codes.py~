import argparse
from nltk import FreqDist


parser = argparse.ArgumentParser(description='Find the most frequent labels (exist in more than 10% of docs).')
parser.add_argument('-dataset', default='/home/datasets/MIMIC/MIMIC2/MIMIC_PREPROCESSED', help='File location of the dataset.')
parser.add_argument('-codes_route', default='/home/datasets/MIMIC/MIMIC2/all_mimic2_codes_with_route',
                    help='Location of the file containing all codes with their routes.')
parser.add_argument('-dataset_size', default='22815',
                    help='number of documents')
parser.add_argument('-codes', default='/home/datasets/MIMIC/MIMIC2/dataset_codes_with_path',
                    help='Path of file to save codes per document where the codes contain the path')
parser.add_argument('-output', default='/home/datasets/MIMIC/MIMIC2/most_frequent_codes',help='output file name')

args = parser.parse_args()

code_routes = {}
def read_code_routes():
    with open(args.codes_route,'r') as in_fd:
        for line in in_fd:
            line_args = line.strip().split('\t')
            code_routes[line_args[0]] = line_args[1].split(',')

# def calculate_code_freq():
#     code_freq = FreqDist()
#     with open(args.code_freq) as in_fd:
#         for line in in_fd:
#             line_args = line.strip().split()
#             code_freq[line_args[0]]+=int(line_args[1])
#             #go over all codes in route and add this codes frequency to them

def create_code_list_with_ancestors():
    with open(args.codes, 'w') as out_fd:
        with open(args.dataset,'r') as in_fd:
            for line in in_fd:
                line_args = line.strip().split('|')
                codes = set(line_args[0].split(','))

                for code in codes.copy():

                    codes.update(code_routes[code])
                out_fd.write(','.join(codes) + '\n')

def calculate_freq_for_codes():
    codes_fd = FreqDist()

    with open(args.codes,'r') as in_fd:
        for line in in_fd:
            for code in line.strip().split(','):
                codes_fd[code] += 1
    return codes_fd

def save_codes_above_threshold(codes_fd):
    threshold = 0.1*int(args.dataset_size)
    print(threshold)
    with open(args.output , 'w') as out_fd:
        print ('\n'.join([str(t) for t in codes_fd.most_common()]))
        for t in codes_fd.most_common():
            if t[1] < threshold:
                break
            out_fd.write(t[0] + '\n')

read_code_routes()
#create_code_list_with_ancestors()
codes_fd = calculate_freq_for_codes()
save_codes_above_threshold(codes_fd)
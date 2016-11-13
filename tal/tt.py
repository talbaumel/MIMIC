labels_count = defaultdict(int)
for doc_labels in all_codes_per_doc:
    for label in doc_labels:
        labels_count[label] += 1
count_to_label = map(lambda label: (labels_count[label], label), labels_count.keys())
count_to_label.sort(reverse=True)
print '50 top labals', map(lambda x: x[1], count_to_label[:50])
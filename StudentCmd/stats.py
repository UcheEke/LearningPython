import statistics

def stats(vector):
    mean = statistics.mean(vector)
    stdev = statistics.stdev(vector)
    return mean, stdev


def get_stats(records, type="student"):
    if type != "student":
            class_vector = []
            for v in records.values():
                class_vector.append(v)
            r = min([len(l) for l in class_vector])
            class_vector = [l[i] for i in range(r) for l in class_vector]
            results = stats(class_vector)
            print("\nClass Mean: {:.2f} (Std.Dev: {:.2f})".format(results[0], results[1]))
    else:
        for k, v in records.items():
            results = stats(v)
            print("{},{}: Mean Score {:.2f} (Std.Dev: {:.2f})".format(k[0].upper(), k[1], results[0], results[1]))

student_records = dict()
student_records[("Biggs", "Lisa")] = [75.0, 79.3, 82.4]
student_records[("Walton", "Travis")] = [73.8, 77.3, 74.3]

if __name__ == '__main__':
    get_stats(student_records, "student")
    get_stats(student_records, "class")

import pathes
from feature_calculations.configurations import header_size

header_size = header_size
num_of_features = 8657
num_of_participants = pathes.num_of_subjects
cluster_size = [2, 4, 6, 8]
k_list = [5, 7, 10, 15, 20, 25]

k_validation = 10

random_seed = 42
np_seed = 42

class_threshold = {'cv': 15, 'lto': 10}

participants_range = range(1, num_of_participants + 1)
fake_participants_range = range(200, 225)

restrictions = [10, 6, 6, 6, 6, 6, 6]

objective_tests = [
    {'name': 'all manipulation', 'filter': (1, [0, 1, 2, 3, 4]), 'labeler': (1, {0: 0, 1: 1, 2: 1, 3: 1, 4: 1}),
     'validation': 'cv', 'unconfound': False},
    {'name': '50ms manipulation', 'filter': (1, [0, 1]), 'labeler': (1, {0: 0, 1: 1}), 'validation': 'cv',
     'unconfound': False},
    {'name': '100ms manipulation', 'filter': (1, [0, 2]), 'labeler': (1, {0: 0, 2: 1}), 'validation': 'cv',
     'unconfound': False},
    {'name': '150ms manipulation', 'filter': (1, [0, 3]), 'labeler': (1, {0: 0, 3: 1}), 'validation': 'cv',
     'unconfound': False},
    {'name': '200ms manipulation', 'filter': (1, [0, 4]), 'labeler': (1, {0: 0, 4: 1}), 'validation': 'cv',
     'unconfound': False}]

subjective_tests = [
    {'name': 'all agency', 'filter': (1, [0, 1, 2, 3, 4]), 'labeler': (2, {0: 0, 1: 1}), 'validation': 'cv',
     'unconfound': False},
    {'name': '50ms agency', 'filter': (1, [0, 1]), 'labeler': (2, {0: 0, 1: 1}), 'validation': 'cv',
     'unconfound': False},
    {'name': '100ms agency', 'filter': (1, [0, 2]), 'labeler': (2, {0: 0, 1: 1}), 'validation': 'cv',
     'unconfound': False},
    {'name': '150ms agency', 'filter': (1, [0, 3]), 'labeler': (2, {0: 0, 1: 1}), 'validation': 'cv',
     'unconfound': False},
    {'name': '200ms manipulation', 'filter': (1, [0, 4]), 'labeler': (2, {0: 0, 1: 1}), 'validation': 'cv',
     'unconfound': False}]

objective_tests_names = [x['name'] for x in objective_tests]
subjective_tests_names = [x['name'] for x in subjective_tests]


def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_transpose(matrix):
    return list(map(list, zip(*matrix)))

class Allocater():

    _STDBASE = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    g_validity = [1, 3]

    def __init__(self, popluation) -> None:
        


        self._groups = []
        self._used = set()



        # print(self._pop_raw)

    @staticmethod
    def _assign_id(pops):
        id_list = []
        for index, value in enumerate(pops):
            attr, subj = value
            id_list.append((index, attr, subj))
        return id_list
    
    @staticmethod
    def _construct_vector_space(popluation: list) -> list:
        v_subject_all = [subjects for __id, _attr, subjects in popluation]
        return tuple(set(list(chain.from_iterable(v_subject_all))))

    @classmethod
    def _get_attrs(cls, type_id: int):
        return [
            cls._STDBASE[type_id // 16 // 4],
            cls._STDBASE[type_id // 16 % 4],
            cls._STDBASE[type_id % 16 // 4],
            cls._STDBASE[type_id % 16 % 4]
        ]
    
    def _get_subjects(self, subjects: list):
        return [1 if s in subjects else 0 for s in self._dimdef]

    '''
    def validate_group(self, g_index: tuple) -> tuple:
        # Produces the sum of matrices of their attributes
        g_pop = [value for index, value in enumerate(self._pop) if value[0] in g_index ]
        # print('G p',g_pop)

        g_prop_matrix = []
        for matrix in [self._get_attrs(__attr) for __id, __attr, __subj in g_pop]:
            g_prop_matrix = matrix_add(g_prop_matrix, matrix)
        
        # print('G m',g_prop_matrix)
        g_validy = [1, 3]
        # print('G',all([max(column) in g_validy for column in (g_prop_matrix)]),(g_prop_matrix))
        if not all([max(column) in g_validy for column in (g_prop_matrix)]):
            return False

        # Produces the sum of vectors of their subjects
        g_subject_matrix = matrix_tanspose([self._get_subjects(__subj) for __id, __attr, __subj in g_pop])
        # print(g_subject_matrix)
        g_subject_count = [sum(row) for row in g_subject_matrix]
        g_subject_common = sum(
            [1 if tot == 3 else 0 for tot in g_subject_count]
        )
        # print('G c1',g_subject_count)
        # print('G c2',g_subject_common)
        # print('validate_group',g_index, g_subject_common)
        return True if g_subject_common else False
    '''

    def validate_group(self, g_index: tuple) -> tuple:
        g_prop_matrix = [[0] * 4 for _ in range(4)]
        for __id in g_index:
            g_prop_matrix = matrix_add(g_prop_matrix, self._attr_matrices[self._pop_raw[__id][1]])

        if not all(max(column) in self.g_validity for column in g_prop_matrix):
            return False

            g_subject_matrix = [self._subject_vectors[idx] for idx in g_index]
            g_subject_common = sum(1 for row in matrix_transpose(g_subject_matrix) if sum(row) == 3)

            return g_subject_common > 0
    
    def iter_k(self, i, j):
        for k in range(j + 1, self._pop_size):
            if k in self._used:
                continue
            # print((i, j, k))
            if self.validate_group((i,j,k)):
                self._groups.append((i,j,k))
                self._used.add(i)
                self._used.add(j)
                self._used.add(k)
                return True
        return False

    def iter_j(self, i):
        for j in range(i + 1, self._pop_size):
            if j in self._used:
                continue
            if self.iter_k(i, j):
                return True
        return False
    
    def iter_i(self):
        for i, value in enumerate(self._pop):
            if i in self._used:
                continue
            if self.iter_j(i):
                continue
        return True

    def alloc(self):
        if self.iter_i():
            return self._groups
        return []
    
def alloc_study_groups(zbinis):
    robot =  Allocater(zbinis)
    # print(robot.form_study_group())
    return robot.alloc()

'''

stri = '{'
for i in range(0,256):
    stri = stri + str(i)+': '+ str(a._get_attrs(i))+','

stri = stri + '}'
print(stri)
'''
str2 = '{'

a = Allocater([])
_attr_matrices = {i: a._get_attrs(i) for i in range(0,256)}
def validate_group(g_index: tuple) -> tuple:
    g_prop_matrix = [[0] * 4 for _ in range(4)]
    for __id in g_index:
        g_prop_matrix = matrix_add(g_prop_matrix, _attr_matrices[__id])

    if not all(max(column) in [1, 3] for column in g_prop_matrix):
        return False
    return True
'''
i = 0
now = None
from itertools import combinations_with_replacement

with open('tbl2.txt','a') as f:
    f.write('{')
    for combo in combinations_with_replacement(range(0,256),3):
        if combo[0] != now:
            now = combo[0]
            print(now)
        f.write( str(combo) + ':' + str(validate_group(combo)) + ',')
        
    f.write('}')
'''

i = 0
now = None
from itertools import combinations_with_replacement

with open('tbl2.txt','a') as f:
    f.write('{')
    for i in range(0,256):
        f.write( str(i)+': '+ str(a._get_attrs(i))+',' )
        
    f.write('}')
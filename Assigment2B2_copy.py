from itertools import chain
import time

def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_transpose(matrix):
    return list(map(list, zip(*matrix)))

class Allocater():

    _STDBASE = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    g_validity = [1, 3]

    def __init__(self, popluation) -> None:
        self.t = time.time()
        self._pop = self._assign_id(popluation)
        self._pop_raw = self._pop.copy()
        self._pop.sort(key=lambda arg: (len(arg[2]),arg[0],arg[1]))
        self._pop_size = len(self._pop)

        self._dimdef = self._construct_vector_space(self._pop)

        self._groups = []
        self._used = set()

        # self._attr_matrices = {i: self._get_attrs(i) for i in range(0,256)}
        # self._id_map = {i: attr for i, attr, subj in self._pop_raw}
        self._subject_vectors = {i: self._get_subjects(subj) for i, attr, subj in self._pop_raw}

        # Precompute attribute bitmasks and subject bitmasks
        self._attr_bits = {i:[i>>6&0b11,i>>4&0b11,i>>2&0b11,i&0b11] for i in range(0,256)}

        # self._attr_bitmasks = {i: self._get_attr_bitmask(attr) for i, attr, subj in self._pop}
        # self._subject_bitmasks = {i: self._get_subject_bitmask(subj) for i, attr, subj in self._pop}

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


    def _get_subject_bitmask(self, subjects: list):
        bitmask = 0
        for s in subjects:
            if s in self._dimdef:
                bitmask |= 1 << self._dimdef.index(s)
        return bitmask
    

    def validate_group(self, g_indices: tuple) -> bool:
        # 00 01 10 11
        # 01 10 11 = 00
        # 00 10 11 = 01
        # 00 01 11 = 10
        # 00 01 10 = 11
        # print(self._pop_raw)
        g_attr_mtx = matrix_transpose([self._attr_bits[self._pop_raw[__index][1]] for __index in g_indices])
        if not all([(row[0]^row[1]^row[2] not in row) or (row[0] == row[1] == row[2]) for row in g_attr_mtx]):
            return False

        for row in matrix_transpose([self._subject_vectors[idx] for idx in g_indices]):
            if sum(row) == 3:
                return True
        return False
    
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
            if time.time() - self.t > 4.85:
                return True
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

# zbinis = [(198, ['FoC']), (138, ['FoC', 'Calc 1']), (14, ['FoC', 'Calc 1']), (66, ['Calc 1'])]
# robot = Allocater(zbinis)
# print(robot.alloc())




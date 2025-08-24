# from Assigment2Q1 import zbini_attrs
from itertools import chain
from itertools import combinations
from collections import UserList
from collections import defaultdict

def matrix_add(a,b):
    answer = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            row.append(a[i][j]+b[i][j])
        answer[i].append(row)
    return answer

def matrix_tanspose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

class Groups(UserList):
    _STDBASE = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]
    ]

    def __init__(self, *args):
        list.__init__(self, *args)
        self.append('FirstMen')
        self.name = 'Westeros'

        self.id = []
        self.attr = []
        self.subj = []

    @classmethod
    def _get_attrs(cls, type_id: int):
        return [
            cls._STDBASE[type_id // 16 // 4],
            cls._STDBASE[type_id // 16 % 4],
            cls._STDBASE[type_id % 16 // 4],
            cls._STDBASE[type_id % 16 % 4]
        ]
    
    def _add_attr(self, __attr):
        self.attr.append(self._get_attrs(__attr))

    def _add_subj(self, __iterable):
        self.subj = list(set(chain.from_iterable([self.subj, __iterable])))

    def append(self, __pop) -> None:
        self.id.append(__pop[0])
        self._add_attr(__pop[1])
        self._add_subj(__pop[2])
        return super().append(__pop)

    def add_to_group(self, __pop: any) -> bool:
        # (id, atri, subj)
        __id, __attr, __subj = __obj

        if self.__len__ > 4:
            return False
        
        g_prop_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for matrix in self.attr:
            g_prop_matrix = matrix_add(g_prop_matrix,matrix)
        g_prop_matrix = matrix_add(g_prop_matrix,self._get_attrs(__attr))
        g_vality = [1,len(self.data)]
        if not all([max(column) in g_vality for column in matrix_tanspose(g_prop_matrix)]):
            return False
        self.append(__pop)


class Allocater():
    '''
    Class to provide utility to allocate zbinis into groups.
    popluation: Zbinis that are waiting to be allocated.
    '''

    # Class constants
    # Note these only evalated once on class define
    _IDENITY = np.eye(4, dtype=int)
    _STDBASE = [_IDENITY[:, 0], _IDENITY[:, 1], _IDENITY[:, 2], _IDENITY[:, 3]]

    _ONE = 1
    _SCORE_SUBJ = 3
    _SCORE_SIZE_3 = 1

    _ALLOCATION_MIN = 0

    _GROUP_VALID_PORTRAIT = 1
    _GROUP_LEN_VALID = [3, 4]
    _GROUP_LEN_MIN = 3
    _GROUP_LEN_MAX = 4

    _INDEX_MIN = 0
    _INDEX_ALLOC_GROUP = 0
    _INDEX_ALLOC_SCORE = 1
    _INDEX_GROUP = 0
    _INDEX_VAILITY_BOOL = 0
    _INDEX_VAILITY_SUBJ = 1

    def __init__(self, popluation: list) -> None:
        '''
        Init varibles
        '''
        self._pop = self._assign_id(popluation)
        # [(0, 198, ['FoC']), (1, 138, ['FoC', 'Calc 1']), (2, 14, ['FoC', 'Calc 1']), (3, 66, ['Calc 1'])]

        self._pop.sort(key=lambda item: len(item[1])) # Sort in subject nums

        self._pop_size = len(self._pop)

        self._group_subj = defaultdict(list)
        self._dimdef = self._construct_vector_space(self._pop)
        for __pop in self._pop:
            __id, __attr, __subj = __pop
            for s in __subj:
                if s in self._dimdef:
                    self._group_subj[s].append(__pop)

        
    @staticmethod
    def _assign_id(pops):
        id_list = []
        for index, value in enumerate(pops):
            attr, subj = value
            id_list.append((index, attr, subj))
        return id_list

    @staticmethod
    def _construct_vector_space(popluation: list) -> list:
        v_subject_all = [subjects for ids, subjects in popluation]
        return tuple(set(list(chain.from_iterable(v_subject_all))))

    def _validate_input(self) -> bool:
        pass

    @staticmethod
    def _get_unique_len(literable: list) -> int:
        '''
        return -> int: number of unique elements in arugment
        '''
        concated_iter = list(chain.from_iterable(literable))
        return len(set(concated_iter))
    
    @staticmethod
    def _check_dupe(literable: list) -> bool:
        '''
        return -> weather all elements are unique
        '''
        concated_iter = list(chain.from_iterable(literable))
        len_raw = len(concated_iter)
        len_unique = len(set(concated_iter))
        return False if len_raw == len_unique else True


    
    @classmethod
    def _construct_list(cls, combo: list) -> tuple:
        l_group = []
        l_score = []
        for group in combo:
            l_group.append(group[cls._INDEX_ALLOC_GROUP])
            l_score.append(group[cls._INDEX_ALLOC_SCORE])
        return (l_group, l_score)

    @classmethod
    def _get_attrs(cls, type_id: int) -> np.array:
        '''
        Repesent the given zbini's attrbute in terms of a 4 by 4 matrix.
        This is modified version of qusition 1.
        were first element in list is replace as e1, nth item as en, etc.
        
        type_id: int
        return -> 
            np.array([4,4]) 4 by 4 numpy array
        '''

        # Order really dosen't mattter here, but kept same as Q1 for convence.
        return np.column_stack((
            cls._STDBASE[type_id // 16 // 4],
            cls._STDBASE[type_id // 16 % 4],
            cls._STDBASE[type_id % 16 // 4],
            cls._STDBASE[type_id % 16 % 4]
        ))
    
    def _get_subjects(self, subjects: list) -> np.array:
        '''
        Encodes the given zbini's subject as an standarlised vector.
        with each element in vector:
            1 == do the subject
            0 == dose not do the subject

        subjects: list of string of subjects
        return ->
            np.array([n,1]) a vector in R_n space defined above
        '''
        return np.array([1 if s in subjects else 0 for s in self._dimdef])

    def validate_group(self, g_index: tuple) -> tuple:
        '''
        Check a given group allocation is valid or not
        g_index: tuple of ids of members in the group
        return ->
            tuple[bool: valitivity, int: num of common subjects]
        '''
        
        g_size = len(g_index)
        if g_size not in self._GROUP_LEN_VALID:
            return (False, None)

        # Produces the sum of matrices of their attributes
        g_pop = [self._pop[i] for i in g_index]
        g_prop_matrix = sum([self._get_attrs(ids) for ids, s in g_pop])

        # Group is valid only if the sum on columns of matrix produced above
        # is equal to either 1 or the number of zbinis in the group.
        g_validy = [self._GROUP_VALID_PORTRAIT, g_size]
        if not all([max(column) in g_validy for column in g_prop_matrix.T]):
            return (False, None)

        # Produces the sum of vectors of their subjects
        g_subject_matrix = np.column_stack(
            [self._get_subjects(subject) for ids, subject in g_pop]
        )
        g_subject_count = [sum(row) for row in g_subject_matrix]

        # Count 1 if element in vector produced above
        # is equal to the number of zbinis in the group, else count 0
        # Group is valid only if non zero is counted.
        g_subject_common = sum(
            [1 if tot == g_size else 0 for tot in g_subject_count]
        )
        # print('validate_group',g_index, g_subject_common)
        return (True, g_subject_common) if g_subject_common else (False, None)
    
    def form_study_group(self) -> list:
        '''
        Find all possiable study groups from given popluation
        return ->
            list of tuple: [(group alloc, score)]
        '''
        allocated = []
        # Iterate threw size 4 then size 3
        for score_size, size in enumerate(self._GROUP_LEN_VALID, 
                                          self._SCORE_SIZE_3):
            # Iteratre for all possiable combination for given size
            for group in combinations(
                [i for i in range(self._INDEX_MIN, self._pop_size)], 
                size
            ):
                vality = self.validate_group(group)
                if not vality[self._INDEX_VAILITY_BOOL]:
                    continue
                allocated.append((
                    group, 
                    score_size + vality[
                        self._INDEX_VAILITY_SUBJ
                    ] * self._SCORE_SUBJ
                ))

        allocated.sort(
            key=lambda tuple: (
                -tuple[self._INDEX_ALLOC_SCORE], 
                tuple[self._INDEX_ALLOC_GROUP]
            )
        )
        # print('form_study_group', allocated)
        return allocated


    def alloc_group(self):
        while self._pop:
            group = []

            for key, val in enumerate(self._pop.copy()):
                pop = self._pop.pop(0)
    
def alloc_study_groups(zbinis):
    robot =  Allocater(zbinis)
    # print(robot.form_study_group())
    return robot.alloc_group()

zbinis = [(198, ['FoC']), (138, ['FoC', 'Calc 1']), (14, ['FoC', 'Calc 1']), (66, ['Calc 1'])]
Allocater(zbinis)
# print(possible_study_groups([(198, ['FoC']), (138, ['FoC', 'Calc 1']), (14, ['FoC', 'Calc 1']), (66, ['Calc 1'])]))
# [((0, 1, 2), 4), ((1, 2, 3), 4)]
# print(alloc_study_groups([(198, ['FoC']), (198, ['FoC']), (138, ['FoC']), (14, ['FoC'])]))
list.__weakrefoffset__
import numpy as np
from itertools import chain
from itertools import combinations

def pre_compute_attr():
    stdbase = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]
    
    return {i: np.column_stack([
            stdbase[i >> 6 & 0b11],
            stdbase[i >> 4 & 0b11],
            stdbase[i >> 2 & 0b11],
            stdbase[i & 0b11]])
            for i in range(0, 256)}

class Allocater():
    '''
    Class to provide utility to allocate zbinis into groups.
    popluation: Zbinis that are waiting to be allocated.
    '''

    # Class constants
    # Note these only evalated once on class define

    # Precompute get_attrs to avoide repeate computation on same attr
    _ATTR_RANGE = range(0, 256)
    _ATTRS = pre_compute_attr()
    

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
    _INDEX_POP_ATTR = 0
    _INDEX_POP_SUBJ = 1

    _INDEX_R_SOC = 0
    _INDEX_R_ACC = 1
    _INDEX_R_CLR = 2
    _INDEX_R_HIR = 3

    def __init__(self, popluation: list) -> None:
        '''
        Init varibles
        '''
        self._pop = popluation
        self._pop_size = len(self._pop)
        self._dimdef = self._construct_vector_space(self._pop)
        self._subject_vectors = {
            index: self._get_subjects(subj) 
            for index, (attr, subj) in enumerate(self._pop)
            }
        
    def _validate_input(self) -> bool:
        pass

    @staticmethod
    def bitwise_xor(input_list: list) -> int:
        '''
        return -> int: XOR resoult of all elements in list.
        '''
        result = 0
        for number in input_list:
            result = result ^ number
        return result

    @staticmethod
    def get_unique_len(literable: list) -> int:
        '''
        return -> int: number of unique elements in arugment
        '''
        concated_iter = list(chain.from_iterable(literable))
        return len(set(concated_iter))
    
    @staticmethod
    def check_dupe(literable: list) -> bool:
        '''
        return -> weather all elements are unique
        '''
        concated_iter = list(chain.from_iterable(literable))
        len_raw = len(concated_iter)
        len_unique = len(set(concated_iter))
        return False if len_raw == len_unique else True
    
    @staticmethod
    def check_uniqe(literable: list) -> bool:
        '''
        return: Weather given literable have only one unique
        '''
        return True if len(set(literable)) == 1 else False


    @classmethod
    def construct_list(cls, combo: list) -> tuple:
        '''
        Split up given list of tuples into two lists
        return ->
            tuple(list,list)
        '''
        l_group = []
        l_score = []
        for group in combo:
            l_group.append(group[cls._INDEX_ALLOC_GROUP])
            l_score.append(group[cls._INDEX_ALLOC_SCORE])
        return (l_group, l_score)

    @staticmethod
    def _construct_vector_space(popluation: list) -> list:
        '''
        Construct a vector space in R_n, 
        with n being the number of UNIQUE subjects zbinis have.
        Each dimension of vector will repsent
        weather zbini do the subject or not.

        popluation: list same as input into the class
        return -> list that states elements in vector is defined
        '''
        v_subject_all = [subjects for ids, subjects in popluation]
        return tuple(set(list(chain.from_iterable(v_subject_all))))



    @classmethod
    def _get_attrs(cls, type_id: int) -> np.array:
        '''
        Repesent the given zbini's attrbute in terms of Vector in R4.
        This is modified version of qusition 1.
        
        type_id: int
        return -> 
            np.array([4,4]) 4 by 4 numpy array
        '''
        if not isinstance(type_id, int):
            return None
        if type_id not in cls._ATTR_RANGE:
            return None
        # Return pre computed attrs.
        return cls._ATTRS[type_id]
    
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

        # Check weather group has valid inputs.
        g_size = len(g_index) 
        # Invalid size
        if g_size not in self._GROUP_LEN_VALID:
            return (False, None)
        
        for index in g_index:
            # Invalid index
            if index not in range(self._INDEX_MIN, self._pop_size):
                return (False, None)
            # Invalid attribute
            if self._pop[index][self._INDEX_POP_ATTR] not in self._ATTR_RANGE:
                return (False, None)
        
        # Consoldate all the vectoers as columns of matrix
        # Such that each row repesents the same attribute
        g_attr = [self._pop[index][self._INDEX_POP_ATTR] for index in g_index]
        g_attr_matrix = sum([self._ATTRS[attr] for attr in g_attr])

        g_validy = [self._GROUP_VALID_PORTRAIT, g_size]
        if not all([max(column) in g_validy for column in g_attr_matrix.T]):
            return (False, None)
        
        # Compute the number of subjects in subject
        # for people in the group
        g_subj_common = sum([1 if sum(row) == g_size else 0 
                             for row in np.column_stack(
                             [self._subject_vectors[idx] for idx in g_index])])
        return (True, g_subj_common) if g_subj_common else (False, None)
    
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

    def alloc(self):
        '''
        Alloc pops to study groups.
        return ->
            list of groups were allocated
        '''
        g_all = self.form_study_group()
        if not g_all:
            return []

        g_posiable = []

        # Theroticaly, the maxium number of groups exists
        # the the group sizes are the minium.
        g_max_therotical = self._pop_size // self._GROUP_LEN_MIN
        g_max_practical = len(g_all)
        g_max = min(g_max_therotical, g_max_practical)

        for size in range(g_max, self._ALLOCATION_MIN, -1):
            for allocation in combinations(g_all, size):
                groups, score = self.construct_list(allocation)
                if self.check_dupe(groups):
                    continue
                g_unalloc = self._pop_size - self.get_unique_len(groups)
                g_posiable.append((groups, g_unalloc, sum(score)))
        # print('alloc_group', g_posiable)
        # print(g_posiable)
        if not g_posiable:
            return []
        return min(
            g_posiable, 
            key=lambda tuple: (tuple[1], tuple[2], tuple[0])
        )[self._INDEX_GROUP]
    
def alloc_study_groups(zbinis):
    '''
    Function as required
    '''
    robot =  Allocater(zbinis)
    # print(robot.form_study_group())
    return robot.alloc()

# print(possible_study_groups([(198, ['FoC']), (138, ['FoC', 'Calc 1']), (14, ['FoC', 'Calc 1']), (66, ['Calc 1'])]))
# [((0, 1, 2), 4), ((1, 2, 3), 4)]
print(alloc_study_groups([(198, ['FoC']), (198, ['FoC']), (138, ['FoC']), (14, ['FoC'])]))
print(alloc_study_groups([(198, ['FoC']), (198, ['FoC']), (138, ['FoC']), (14, ['FoC'])]))
print(alloc_study_groups([(198, ['FoC']), (198, ['FoC']), (198, ['FoC']), (198, ['FoC'])]))
print(alloc_study_groups(None))
import numpy as np


class BlueList(list):
    def __init__(self, sequence=[], *args):
        if None in list(args) + sequence:
            print("ЛАЖААА. Среди элементов списка есть None. Список заменен на стандартный")
            super().__init__([2, 7, 1, 8, 2, 8])
        else:
            super().__init__(list(args) + sequence)

    def __str__(self):
        return '[' + ' --||-- '.join(map(str, self)) + ']' 
    
    def append(self, item):
        self.insert(len(self) // 2, item)
        self.insert(0, item)
        self.insert(len(self), item)
    
    def pop(self):
        ind = np.random.randint(0, len(self) - 1)
        val = self[ind]
        super().pop(ind)
        return val

    def remove(self, item):
        while item in self:
            super().remove(item)

    def randomize(self, num):
        for _ in range(num):
            self.pop()
        np.random.shuffle(self)


class BlueDict(dict):
    def __init__(self, sequence={}, **kwargs):
        super().__init__(sequence | {2 * key: val for key, val in kwargs.items()})

    def __str__(self):
        return 'Вы используете супер пупер словарь! \n' + '\n'.join(map(lambda m: str(m[0]) + ' - ' + str(m[1]), self.items()))
    
    def get(self, key):
        if key in self.keys():
            return super().get(key)
        else:
            raise Exception("ЛАЖААА. Нет такого ключа")
    
    def values(self):
        return list(super().keys())

    def keys(self):
        return ''.join(map(str, super().values()))

    def copy(self):
        return BlueDict({key: val for key, val in self.items() if not isinstance(key, str)})
        
    def true_form_of_dict(self, k):
        return BlueDict({key: val for j in [{key * i: val * i for key, val in self.items()} for i in range(2, k + 1)] for key, val in j.items()})
    


class BlueSet(set):
    def __init__(self, sequence):
        if isinstance(sequence, BlueList):
            super().__init__([val for ind, val in enumerate(sequence) if not
                ((isinstance(val_1:=sequence[ind-1], (int, float)) and sequence.count(val_1) > 1 and ind != 0) or 
                (isinstance(val_2:=sequence[(ind+1) % len(sequence)], (int, float)) and sequence.count(val_2) > 1 and ind != len(sequence) - 1))
                    ])
        else:
            raise Exception("ЛАЖААА. Нужно передавать данные только в виде BlueList")

        

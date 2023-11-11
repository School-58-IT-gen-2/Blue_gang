import numpy as np


class BlueList(list):
    def __init__(self, *args):
        if None in args:
            print("ЛАЖААА. Среди элементов списка есть None. Список замене на стандартный")
            super().__init__([2, 7, 1, 8, 2, 8])
        else:
            super().__init__(args)

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
    def __init__(self, **kwargs):
        super().__init__()
        
        for key, val in kwargs.items():
            self[2 * key] = val

    def __str__(self):
        return 'Вы используете супер пупер словарь! \n' + '\n'.join(map(lambda m: str(m[0]) + ' - ' + str(m[1]), d.items()))
    
    def get(self, key):
        if key in self.keys():
            return super().get(key)
        else:
            print('ЛАЖААА. Нет такого ключа')
    
    def values(self):
        return list(super().keys())

    def keys(self):
        return ''.join(map(str, super().values()))


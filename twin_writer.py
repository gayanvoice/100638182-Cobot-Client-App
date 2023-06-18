import sys
from rtde import serialize

sys.path.append("..")


class TwinWriter(object):
    def __init__(self, names, types):
        if len(names) != len(types):
            raise ValueError("List sizes are not identical.")
        self.__names = names
        self.__types = types

    def get_header_row(self):
        data = []
        columns = 0
        for i in range(len(self.__names)):
            size = serialize.get_item_size(self.__types[i])
            columns += size
            if size > 1:
                for j in range(size):
                    name = self.__names[i] + "_" + str(j)
                    data.append(name)
            else:
                name = self.__names[i]
                data.append(name)
        return data

    def get_data_row(self, data_object):
        data = []
        for i in range(len(self.__names)):
            size = serialize.get_item_size(self.__types[i])
            value = data_object.__dict__[self.__names[i]]
            if size > 1:
                data.extend(value)
            else:
                data.append(value)
        return data

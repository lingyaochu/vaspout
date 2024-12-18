import numpy as np

class Oszicar:
    
    def __init__(self, file):
        self.data = np.array(self.read_oszicar(file))
        self.ion_step_indexes = self.get_ionstep_index()
        self.energy,self.mag = self.get_data_all_ionstep()

    @staticmethod
    def read_oszicar(file):
        with open(file, 'r') as f:
            lines = f.readlines()
        return lines
    
    def get_ionstep_index(self):
        ionstep_index = []
        for i in range(len(self.data)):
            if self.data[i].split()[0].isdigit():
                ionstep_index.append(i)
        
        return np.array(ionstep_index)
    
    def get_data_from_ionstep(self, ionstep:int):
        """
        得到给定离子步的数据
        
        Args:
            ionstep: 具体的离子步，从0开始
        
        Returns:
            energy: 该离子步的能量
            magmom: 该离子步的自旋
        """
        assert len(self.ion_step_indexes) > 0, "the first ion step is not finished"
        assert ionstep + 1 <= len(self.ion_step_indexes), "the input ion step is out of range"
        index_of_data = self.ion_step_indexes[ionstep]
        ionstep_data_str = self.data[index_of_data].split()

        energy = float(ionstep_data_str[2])
        magmom = round(float(ionstep_data_str[-1]),4)
        return energy, magmom
    
    def get_data_all_ionstep(self):
        """
        得到所有离子步的数据

        Returns:
            energy_list: 所有离子步的能量列表
            magmom_list: 所有离子步的自旋列表
        """
        energy_list = []
        magmom_list = []
        for i in range(len(self.ion_step_indexes)):
            energy, magmom = self.get_data_from_ionstep(i)
            energy_list.append(energy)
            magmom_list.append(magmom)
        return np.array(energy_list), np.array(magmom_list)
        

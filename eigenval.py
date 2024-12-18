
import numpy as np
class Eigenval:
    def __init__(self, eigen_file):
        self.read_eigenval(eigen_file)

    def read_eigenval(self, eigen_file):
        """
        从EIGENVAL文件中读取数据,将输入写入到类变量中
        nelect: 体系总的电子数
        nkpt: 总k点数
        nbands: 每个k点上的总轨道数
        kpoints: 所有的k点的坐标
        kpt_weight: 所有k点的对应权重
        band_energy: [kpt, band, spin]对应的能量
        band_occ: [kpt, band, spin]对应的占据情况
        spin: 非自旋极化为2，自旋极化为1
        """
        with open(eigen_file,"r") as f:
            head = f.readline()
            self.spin = int(head.split()[3])
            for _ in range(4):
                f.readline()
            self.nelect, self.nkpt, self.nbands = [int(x) for x in f.readline().split()]

            self.kpoints = np.zeros((self.nkpt, 3))
            self.band_energy = np.zeros((self.nkpt, self.nbands, self.spin))
            self.band_occ = np.zeros((self.nkpt, self.nbands, self.spin))
            self.kpt_weight = np.zeros(self.nkpt)

            # 对kpt循环，再对bands循环
            for kpoint in range(self.nkpt):
                f.readline()
                kpt_and_weight = np.array([float(i) for i in f.readline().split()])
                self.kpoints[kpoint,:] = kpt_and_weight[:3]
                self.kpt_weight[kpoint] = kpt_and_weight[3]
                for band in range(self.nbands):
                    band_info = np.array([float(i) for i in f.readline().split()])
                    self.band_energy[kpoint, band, :] = band_info[1:1+self.spin]
                    self.band_occ[kpoint, band, :] = band_info[1+self.spin: 1+2*self.spin]
        return None
    
    def get_lumo(self, kpt, spin):
        """
        得到给定k点，给定自旋的最低未占据态的轨道编号（从0开始）以及能量
        """
        occ = self.band_occ[kpt,:,spin].copy()
        # 找出occ出现的第一个0的index
        band_index = np.where(occ == 0)[0][0]

        return band_index, self.band_energy[kpt, band_index, spin]
    
    def get_homo(self, kpt, spin):
        """
        得到给定k点，给定自旋的最高完全占据态的轨道编号（从0开始）以及能量
        """
        occ = self.band_occ[kpt,:,spin].copy()
        # 找出occ中最后出现的1的index
        band_index = np.where(occ == 1)[0][-1]

        return band_index, self.band_energy[kpt, band_index, spin]
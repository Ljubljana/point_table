import pandas as pd
import re
import sys
from PyQt5.Qt import *
from try_gui import Ui_Form


class Res(QWidget):
    hao = pd.DataFrame
    txtpath = ''
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    # 导入TXT
    def pb_daorutxt1(self):
        h2 = QFileDialog.getOpenFileName(self, '打开文件', '.', '点表文件(*.txt)')
        self.ui.xianshi1.setText(h2[0])
        self.txtpath = h2[0]
        h2 = pd.read_csv(h2[0], sep='\t', encoding='gbk')
        bzb = pd.read_excel('./标准表.xls')
        self.hao = h2
    # 0列，信号类型
    def pb_xinghaoleixing1(self):
        for i in self.hao.index:
            self.hao['信号类型'].at[i] = 1
        self.ui.xianshi2.insertPlainText('信号类型置1-完成:)\n')
        # 设置滚动条始终在最下面
        self.ui.xianshi2.verticalScrollBar().setValue(self.ui.xianshi2.verticalScrollBar().maximum())
        # print(11)

    # 2列，设备ID
    def pb_shebeiID1(self):
        ststionname = self.ui.lineEdit_zhanmingsuoxie.text()
        #Process finished with exit code -1073740791 (0xC0000409)是内存不足报错,加入如下代码即可。
        self.hao[['所属设备ID']] = self.hao[['所属设备ID']].astype(str)
        for i in self.hao.index:
            # self.hao['所属设备ID'].at[i] = 'nan'
            jgmc_p = r'开关'
            jgmc_q = r'主变'
            jgmc_s = str(self.hao['间隔名称'].at[i])
            jgmc_match1 = re.sub(jgmc_p, '', jgmc_s)  # 取到调号
            jgmc_match2 = re.sub(jgmc_q, '', jgmc_s)  # 取到调号
            # print(jgmc_match1)
            # print(jgmc_match2)
            if '开关' in str(self.hao['间隔名称'].at[i]):
                self.hao['所属设备ID'].at[i] = ststionname + 'CB' + jgmc_match1
            elif '主变' in str(self.hao['间隔名称'].at[i]):
                self.hao['所属设备ID'].at[i] = ststionname + 'XF' + jgmc_match2
            else:
                pass
        self.ui.xianshi2.insertPlainText('生成设备ID-完成:)\n')

    #4列，数据类型
    def pb_shujuleixing1(self):
        for i in self.hao.index:
            if pd.isnull(self.hao.iloc[i, 10]):  # 若装置名称为空，则数据类型赋值1
                self.hao['数据类型'].at[i] = 1
            else:
                self.hao['数据类型'].at[i] = 0
        self.ui.xianshi2.insertPlainText('生成软硬接点-完成:)\n')
    # 5列，告警级别
    def pb_gaojing1(self):
        bzb = pd.read_excel('./标准表.xls')
        for j in bzb.index:
            for i in self.hao.index:
                if str(bzb['46类信号'].at[j]) in self.hao['规范后名称'].at[i]:
                    self.hao['告警级别'].at[i] = '4,6'
        for j in bzb.index:
            for i in self.hao.index:
                if str(bzb['3类信号'].at[j]) in self.hao['规范后名称'].at[i]:
                    self.hao['告警级别'].at[i] = '3'
        for j in bzb.index:
            for i in self.hao.index:
                if str(bzb['2类信号'].at[j]) in self.hao['规范后名称'].at[i]:
                    self.hao['告警级别'].at[i] = '2'
        for j in bzb.index:
            for i in self.hao.index:
                if str(bzb['1类信号'].at[j]) in self.hao['规范后名称'].at[i]:
                    self.hao['告警级别'].at[i] = '1'
        self.ui.xianshi2.insertPlainText('生成告警级别-完成:)\n')
    #6列，控制位
    def pb_kongzhiwei1(self):
        for i in self.hao.index:
            self.hao['控制位'].at[i] = 0
        self.ui.xianshi2.insertPlainText('控制位置0-完成:)\n')
    #15列，光字牌
    def pb_guangzipai1(self):
        for i in self.hao.index:
            self.hao['是否上光字牌'].at[i] = 1
        self.ui.xianshi2.insertPlainText('是否上光字牌置1-完成:)\n')
    #16列，取反
    def pb_qufan1(self):
        for i in self.hao.index:
            self.hao['是否取反'].at[i] = 0
        self.ui.xianshi2.insertPlainText('取反置0-完成:)\n')
    #初始化最后一大块
    def pb_dianhao1(self):
        for i in self.hao.index:
            self.hao.iloc[i, [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]] = -1
        self.ui.xianshi2.insertPlainText('最后一大块的初始化-完成:)\n')
    #输出TXT
    def pb_shuchutxt1(self):
        # print(22)
        # print(self.txtpath)
        url2 = self.txtpath
        pattern2 = r'[.]'  # 分割字符串做输出路径
        burl = re.split(pattern2, url2)
        self.hao.to_csv(burl[0] + 'out.txt', sep='\t', index=False)
        self.ui.xianshi2.insertPlainText('输出点表-完成:)\n')


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = Res()
    window.show()

    sys.exit(app.exec_())

import re
import time
import mmap
import linecache
import contextlib
import threading
from multiprocessing import Pool


def method1(path):
      file = open(path,'r')
      lines = file.readlines()
      lss = []
      for line in lines:
            ls = re.split(r',',line)
            lss.append(ls)
def method2(path):
      file = open(path, 'r')
      lines = file.readlines()
      lss = []
      for line in lines:
            ls = line.split(",")
            lss.append(ls)
      file.close()
def method3(path):
      lines = linecache.getlines(path)
      lss = []
      for line in lines:
            ls = line.split(",")
            lss.append(ls)
      # 清除缓存
      linecache.clearcache()
def method5(path):
      read_lines_count = 0
      lss = []
      f = open(path,'r')
      with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            m.seek(0, 0)
            m.readline()
            while True:
                  line = m.readline().strip()
                  temps = line.split(b',')
                  lss.append(temps)
                  read_lines_count += 1
                  if read_lines_count == 20000:
                        break
      f.close()

# def method5(path):
#       f = open(path, 'r')
#       lss = []
#       for i  in f:
#             ls = i.split(",")
#             lss.append(ls)

def method6(path):
      f = open(path,'r')
      str = f.read()
      ls = str.split('\n')
      lss = []
      for i in ls:
            lss.append(i.split(","))


class mThread:
      def __init__(self,trainFile):
            self.file = open(trainFile,'r')
            self.lss = []
            self.count = 0
      def run(self):
            with lock:
                  while self.count <20000:
                        line = self.file.readline()
                        self.lss.append(line.split(","))
                        self.count += 1
      def print(self):
            print(len(self.lss))


class mThread_1:
      def __init__(self,trainFile):
            self.lines = linecache.getlines(trainFile)
            self.lss = []
            self.count = 0
      def run(self):
            with lock:
                  while self.count <20000:
                        line = self.lines[self.count]
                        self.lss.append(line.split(","))
                        self.count += 1
      def print(self):
            print(len(self.lss))

class mThread_2:
      def __init__(self,trainFile):
            self.f = open(trainFile,'r')
            self.m = mmap.mmap(self.f.fileno(), 0, access=mmap.ACCESS_READ)
            self.m.seek(0,0)
            self.m.readline()
            self.lss = []
            self.count = 0
      def run(self):
            with lock:
                  while self.count <20000:
                        line = self.m.readline().strip()
                        temps = line.split(b',')
                        self.lss.append(temps)
                        self.count += 1
      def print(self):
            self.f.close()
            self.m.close()
            print(len(self.lss))

def method7(path):
      f = open(path,'r')
      lss = []
      line = f.readline()
      while line:
            lss.append(line.split(","))
            line = f.readline()
      f.close()

def method8(path):
      f = open(path,'r')
      lss = []
      for i in f:
            lss.append(i.split(","))
      f.close()

def method9(n_pro,each,path):
      start = n_pro*each
      end = (n_pro + 1)*each
      file = open(path,'r')
      lines = file.readlines()
      ls = []
      for i in range(start,end):
            ls.append(lines[i])
      file.close()
      return ls

def method10(n_pro,each,path):
      start = n_pro * each
      end = (n_pro + 1) * each
      file = open(path, 'r')
      lines = linecache.getlines(path)
      ls = []
      for i in range(start, end):
            ls.append(lines[i])
      file.close()
      return ls

def method11(n_pro,each,path):
      read_lines_count = 0
      f = open(path, 'r')
      ls = []
      with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            m.seek(6000 * n_pro * each, 0)
            while True:
                  line = m.readline().strip()
                  ls.append(line.split(','))
                  read_lines_count += 1
                  if read_lines_count == read_test_lines_set:
                        break
      f.close()
      return ls

if __name__ == "__main__":
      a = int(round(time.time() * 1000))
      train_file = "../测试集(20000).txt"

      pro_num = 4
      tef = open(train_file)
      tef.seek(0, 2)
      read_test_lines_set = int(tef.tell() / 6000 / pro_num)
      tef.close()

      pool = Pool(processes=pro_num)
      lss = []
      for i in range(pro_num):
            res = pool.apply_async(method11, (i,read_test_lines_set,train_file))
            lss.append(res)
      pool.close()
      pool.join()

      b = int(round(time.time() * 1000))
      print("time:", b - a, 'ms')
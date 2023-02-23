from collections import deque# may not need this
from pathlib import Path
import json

#TODO implement feature to sort primers based on gc content
def sort_primers(primers:list , ascending : bool = True):
    """ sort primers"""
    #if ascending:
    #    for i in primers:
    pass

def try_sort():
    """this is just a place holder func"""
    primers_=[]
    ordered_primers =deque()
    ordered_primers.append(primers_[0])
    for index , i in enumerate(primers_):
        if index > 0:
            gc_content_current = list(i.values())[0][0]['GC_content']
            gc_content_previous = list(ordered_primers[-1].values())[0][0]['GC_content']
            if gc_content_current <= gc_content_previous:
                pre = ordered_primers.pop()
                #print(len(ordered_primers))
                #print(f'appending current -->{i}')
                ordered_primers.append(i)
                #print(f'appending pre -->{pre}')
                ordered_primers.append(pre)
            else:
                ordered_primers.append(i)
        #print(len(ordered_primers), f'at position{index}')

    print('done loop')
    for i in ordered_primers:
        print(i)
    pass



class Primer_Search():
    """
    search primers of desired height  from a sequence
    primers returned:
        -contain atleast 40% gc_content
        -starting 2 and last 2 bases are either g or c
    """
    def __init__(self, primer_length:int, data:Path):
        self.length = primer_length
        self.file_path = data
        self.seq = self._read_clean(data=data)

    def _read_clean(self, data:Path):
        with open(filepath, 'r') as file:
            data = file.read()
        seq = ""
        bases = 'acgt'
        for i in data:
            if i.lower() in bases:
                seq += i
        return seq

    def _check_GC(self, primer:str) -> int:
        count_gc = 0
        for i in primer:
            if i.lower() in 'gc':
                count_gc += 1
        gc_content = count_gc/len(primer)
        return gc_content

    def _start_strong(self, primer:str) ->str:
        """checks if a primer first and last 2 bases are g or c"""
        if primer[:2] in 'ggcc' and primer[-2:] in 'ggcc':
            return True
        else:
            return False

    def __call__(self, fp_write:Path):
        primers_=[]
        with open(fp_write, 'w') as file:
            count_primers = 0
            for i in range(0, len(self.seq)-self.length):
                primer = self.seq[i:i+self.length]
                if self._start_strong(primer) and self._check_GC(primer) >= 0.4:
                    count_primers += 1
                    primer_info={primer:[{'GC_content':self._check_GC(primer), 'pos_in_seq':i}]}
                    primers_.append(primer_info)
                    file.write(json.dumps(primer_info))
                    file.write('\n')

if __name__ == "__main__":
    filepath = 'data/pEM40_seq.txt'
    fp_write = 'results/primers.txt' # file to write to
    ps = Primer_Search(20, filepath)
    ps(fp_write=fp_write)

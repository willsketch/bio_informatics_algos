import json
from pathlib import Path

#TODO implement feature to sort primers based on gc content

class Primer_Search():
    """
    input:
    txt file with sequence

    searches primers of desired height  from a sequence
    primers returned:
        -contain atleast 40% gc_content
        -starting 2 and last 2 bases are either g or c

    output:
    writes (ordered) primers to a txt file
    """
    def __init__(self, primer_length:int, data:Path, ordered:bool = True):
        self.length = primer_length
        self.file_path = data
        self.ordered = ordered
        self.count_primers = 0
        self.seq = self._read_clean(data=data)


    def _read_clean(self, data:Path) -> str:
        """cleans the file provided and returns sequence"""
        with open(filepath, 'r') as file:
            data = file.read()
        seq = ""
        bases = 'acgt'
        # checks if every character in file is a dna base
        for i in data:
            if i.lower() in bases:
                seq += i
        return seq

    def _check_GC(self, primer:str) -> int:
        """ calculates gc content of each primer"""
        count_gc = 0
        #count the number of gc bases
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

    def _create_primers(self) -> list:
        """ function to create primers"""
        primers_=[]
        for i in range(0, len(self.seq)-self.length):
            primer = self.seq[i:i+self.length]
        #check whether its a strong primer and contains atleast 40% gc content
            if self._start_strong(primer) and self._check_GC(primer) >= 0.4:
                self.count_primers += 1
                primer_info={primer:[{'GC_content':self._check_GC(primer), 'pos_in_seq':i}]}
                primers_.append(primer_info)

        return primers_

    def _sort_primers(self, primers:list) -> list:
        """ sort primers in descending order of gc_content"""

        primers_copy = primers.copy()# create copy of primers
        #create list of only gc_content as a proxy for primers
        gc_content = [list(i.values())[0][0]['GC_content'] for i in primers_copy]
        min_gc = min(gc_content)
        ordered_primers =[]
        while min_gc < 1:
            indices = [i for i, e in enumerate(gc_content) if e == min_gc]
            for i in indices:
                ordered_primers.append(primers_copy[i])
            gc_content =[1 if i == min_gc else i for i in gc_content]
            min_gc = min(gc_content)
        ordered_primers.reverse()
        return ordered_primers

    def __call__(self, fp_write:Path):
        """ writes primer info to desired file"""
        primers= self._create_primers()
        if self.ordered:
            primers = self._sort_primers(primers)
        with open(fp_write, 'w') as file:
            for primer_info in primers:
                file.write(json.dumps(primer_info))
                file.write('\n')

if __name__ == "__main__":
    filepath = 'data/pEM40_seq.txt'
    fp_write = 'results/primers_ordered.txt' # file to write to
    ps = Primer_Search(20, filepath)
    ps(fp_write=fp_write)

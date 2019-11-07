import os
import re
import gzip
import csv
from pathlib import Path 
from constant import *
from typing import List, Iterator, Optional


class ParseLog:
    filepath: Optional[str] = None
    
    def __init__(self,filepath:str , dirname:str) -> None:
        self.filepath = filepath
        self.dirname = dirname

    def find_file(self) -> str:
        assert self.filepath is not None
        yield from Path(self.dirname).rglob(self.filepath)

    def open_file(self) -> Iterator[List[str]]:
        names = self.find_file()
        for name in names:
            if name.suffix == '.gz':
                yield gzip.open(name, 'rt')
            else:
                open(name,'rt')      
    
    def concat_file(self) -> Iterator[List[str]]:
        logfiles = self.open_file()
        for f in logfiles:
            yield from f
    
    def parse_log_files(self) -> Iterator[List[str]]:        
        loglines = self.concat_file()
        groups = (LOG_PATTERN.match(line) for line in loglines)
        tuples = (g.groups() for g in groups if g)

        colnames = COLNAMES

        log = (dict(zip(colnames, t)) for t in tuples)

        return log

    def save_to_csv(self) -> List[str]:
        dict_data = self.parse_log_files()
        with open(SAVE_TO_CSV, 'w', newline='') as csvfile:
            header = [next(dict_data) for x in range(1)]
            writer = csv.DictWriter(csvfile, fieldnames=COLNAMES)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)

if __name__=='__main__':
    p = ParseLog('2008*', 'data\iislogs_gz')
    log = p.save_to_csv()
    for l in log:
        print(l) 

import openpyxl
import math
from pathlib import Path

META_TABLE = Path(__file__).parent / 'meta' / \
    'FINA_Points_Table_Base_Times.xlsx'


class BaseTime:
    def __init__(self, table: str = META_TABLE):
        self.table = table
        self.max_age = math.inf
        self.global_data = {}
        self.data = {}
        self._parse()

    def _parse(self):
        workbook = openpyxl.load_workbook(self.table)
        sheet = workbook.active
        data = {}
        for row in sheet.iter_rows(min_row=4):
            values = tuple(r.value for r in row)
            if values[3] != 1:
                continue
            data.setdefault(values[0], {})
            data[values[0]][(values[2], values[4], values[5])] = values[8]
        self.data = data[values[0]].copy()
        self.global_data = data

    def get_point(
        self,
        gender: str,
        distance: int,
        stroke: str,
        result: float | int
    ) -> int:
        if result <= 0:
            return 0
        B = self.data[(gender, distance, stroke)]
        return 1000 * (B / result) ** 3


if __name__ == '__main__':
    # table = 'FINA_Points_Table_Base_Times.xlsx'
    bt = BaseTime()
    print(bt.get_point('M', 800, 'FREE', 567.65))

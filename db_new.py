from typing import List, Dict

from db_def import DBInterface
from util import parse_time


# ----------------- 数据定义 -----------------

class TestDB(DBInterface):
    def __init__(self):
        super().__init__()
        self.int_val = 1
        self.bool_val = True


class FirstRunDB(DBInterface):
    def __init__(self):
        super().__init__()

    def get_update_at(self):
        return parse_time(self.update_at)


class WelfareDB(DBInterface):
    def __init__(self):
        super().__init__()

        self.share_code_list = [] # type: List[str]
        self.exchanged_dict = {} # type: Dict[str, bool]


if __name__ == '__main__':
    print(DBInterface())
    print(TestDB())
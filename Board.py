import random
from enum import Enum

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 16
SIZE = 20  # 块大小
MINE_COUNT = 99


# 单元格状态
class CellStatus(Enum):
    normal = 1,   # 未点击
    clicked = 2,  # 已点击
    mine = 3      # 地雷
    flag = 4      # 标记为地雷
    ask = 5       # 标记为问号
    bomb = 6      # 踩中地雷
    hint = 7      # 被双击的周围
    double = 8    # 正被双击


# Mine Class
class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._around_mine_count = -1
        self._status = CellStatus.normal
        self.set_value(value)

    def __repr__(self):
        return str(self._value)

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    x = property(fget=get_x, fset=set_x)

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    y = property(fget=get_y, fset=set_y)

    def get_value(self):
        return self._value

    def set_value(self, value: int) -> None:
        if value:
            self._value = 1
        else:
            self._value = 0

    value = property(fget=get_value, fset=set_value, doc='0:not a mine 1:mine')

    def get_around_mine_count(self):
        return self._around_mine_count

    def set_around_mine_count(self, count):
        self._around_mine_count = count

    around_mine_count = property(fget=get_around_mine_count,
                                 fset=set_around_mine_count,
                                 doc='num of mines around')

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    status = property(fget=get_status, fset=set_status, doc='Cell status')


# Mine Cell class
class MineCell:
    def __init__(self):
        self._cell = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]

        # 埋雷
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._cell[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1

    def get_cell(self):
        return self._cell

    cell = property(fget=get_cell)

    def get_mine(self, x, y):
        return self._cell[y][x]

    def open_mine(self, x, y):
        # 踩到雷了
        if self._cell[y][x].value:
            self._cell[y][x].status = CellStatus.bomb
            return False

        # 先把状态改为 clicked
        self._cell[y][x].status = CellStatus.clicked

        around = _get_around(x, y)

        _sum = 0
        for i, j in around:
            if self._cell[j][i].value:
                _sum += 1
        self._cell[y][x].around_mine_count = _sum

        # 如果周围没有雷，那么将周围8个未中未点开的递归算一遍
        if _sum == 0:
            for i, j in around:
                if self._cell[j][i].around_mine_count == -1:
                    self.open_mine(i, j)

        return True

    def double_mouse_button_down(self, x, y):
        if self._cell[y][x].around_mine_count == 0:
            return True

        self._cell[y][x].status = CellStatus.double

        around = _get_around(x, y)

        sumflag = 0  # 周围被标记的雷数量
        for i, j in _get_around(x, y):
            if self._cell[j][i].status == CellStatus.flag:
                sumflag += 1
        # 周边的雷已经全部被标记
        result = True
        if sumflag == self._cell[y][x].around_mine_count:
            for i, j in around:
                if self._cell[j][i].status == CellStatus.normal:
                    if not self.open_mine(i, j):
                        result = False
        else:
            for i, j in around:
                if self._cell[j][i].status == CellStatus.normal:
                    self._cell[j][i].status = CellStatus.hint
        return result

    def double_mouse_button_up(self, x, y):
        self._cell[y][x].status = CellStatus.clicked
        for i, j in _get_around(x, y):
            if self._cell[j][i].status == CellStatus.hint:
                self._cell[j][i].status = CellStatus.normal

def _get_around(x, y):
    """返回(x, y)周围的点的坐标"""
    return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]

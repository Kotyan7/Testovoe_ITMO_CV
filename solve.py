import numpy as np
from heapq import heappop, heappush
from collections import defaultdict

def find_edges(g):
    G = np.matrix(g)
    N = len(G)
    edges = []
    for i in range(N):
        for j in range(N):
            if G[(i, j)] != 0:
                edges.append((i, j, G[(i, j)]))
    sorted_edges = sorted(edges, key=lambda x: (x[0], x[2]))
    return sorted_edges


def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))
    q, seen, mins = [(0, f, ())], set(), {f: 0}
    while q:
        cost, v1, path = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = path + tuple([v1])
            if v1 == t:
                return (cost, path)
            for c, v2 in g.get(v1, ()):
                if v2 in seen:
                    continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))
    return float("inf")


def solve(start, state, target_vertices, all_length, limit, first=True):
    '''
    Функция решения состоит из 2 этапов:
    1 Этап находим путь жадно.
    2 Этап находим путь перебором, но в процессе поиска
    отслеживаем, чтобы длина перебираемых путей не 
    оказалась больше длины жадного пути
    start - индекс вершины старта
    state - словарь с наименьшими путями от одной вершины к другой
    target_vertices - индексы не посещённых вершин
    all_length - начальная пройденная длина
    limit - ограничение поиска решений
    first - запускаеть функцию в жадном режиме - True - жадный режим/False - режим перебора
    '''
    if first:
        # ищем среди всех путей минимальный, получаем длину пути и путь (список вершин)
        leng, arr = min([state[f'{start}_{i}'] for i in target_vertices if i != start])
        # обновляем индексы не посещённых вершин
        target_vertices1 = set(target_vertices) - set(arr)
        # выбираем новую отправную точку
        start = arr[-1]
        # обновляем длинну пройденого пути
        all_length += leng
        if not target_vertices1: # если не посещенных вершин не осталось - идём в 0 вершину
            leng, arr = state[f'{start}_{0}']
            all_length += leng
            return all_length
        # применяем функцию дальше
        return solve(start, state, target_vertices1, all_length, limit, first=True)
    temp = 0
    # перебираем все пути
    for leng, arr in sorted([state[f'{start}_{i}'] for i in target_vertices if i != start]):
        target_vertices1 = set(target_vertices) - set(arr)
        start = arr[-1]
        temp = all_length + leng
        # если длина пути оказалась больше базового (найденого жадно)
        # то дальше путь не будет рассчитываться
        if temp > limit: 
            continue
        if not target_vertices1: # если не посещенных вершин не осталось - идём в 0 вершину
            leng, arr = state[f'{start}_{0}']
            temp = temp + leng
            # если найден более оптимальный путь
            # то обновляем нашу оценку
            if temp < limit:
                limit = temp
        new_limit = solve(start, state, target_vertices1, temp, limit, first=False)
        limit = new_limit if new_limit < limit else limit
    return limit


M = []
# считываем данные

n = int(input())
for i in range(n):
    M.append([int(st) for st in input().split()])

M = np.array(M)
# находим вершины
edges = find_edges(M)
state = dict()

# находим минимальное расстояние от одной вершины к другой
# и сохраняем в словарь
for i in range(n):
    for j in range(n):
        if i!=j:
            state[str(i)+'_'+str(j)]= dijkstra(edges, i, j)

# задаём целевые вершины для посещения
target_vertices = set(range(1, n))
start = 0
all_length = 0

# ищем базовое решение
limit = solve(start, state, target_vertices, all_length, 0, first=True)

target_vertices = set(range(1, n))
start = 0
all_length = 0
# ищем основное решение
print(solve(start, state, target_vertices, all_length, limit, first=False))


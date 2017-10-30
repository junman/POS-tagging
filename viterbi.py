# -*- coding:utf-8 -*-
def viterbi(obs, states, start_p, trans_p, emit_p):
    """
    :param obs: 可见序列
    :param states: 隐状态
    :param start_p: 开始概率
    :param trans_p: 转换概率
    :param emit_p: 发射概率
    :return: 序列+概率
    """
    path = {}
    V = [{}]  # 记录第几次的概率
    for state in states:
        V[0][state] = start_p[state] * emit_p[state].get(obs[0], 0)
        path[state] = [state]
    for n in range(1, len(obs)):
        V.append({})
        newpath = {}
        for k in states:
            pp,pat=max([(V[n - 1][j] * trans_p[j].get(k,0) * emit_p[k].get(obs[n], 0) ,j )for j in states])
            V[n][k] = pp
            newpath[k] = path[pat] + [k]
            # path[k] = path[pat] + [k]#不能提起变，，后面迭代好会用到！
        path=newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return prob, path[state]
# A*算法寻找初始状态到目标状态的路径
def h(init, goal):
    # 边缘队列初始已有源状态节点
    queue = [Node(init, 0, Start, None)]  #已经生成但没考察的表
    visit = {}  # 访问过的表
    # 队列没有元素则查找失败
    while queue:
        index = GetMinIndex(queue)    # 获取拥有最小估计距离的节点索引
        node = queue[index]
        visit[toInt(node.state)] = True
        if node.state == goal:
            return node
        del queue[index]
        for act in GetActions(node.state):
            near = Node(act(node.state), node.step + 1, act, node)  #不同动作会获得的状态下的节点
            if toInt(near.state) not in visit:
                queue.append(near)     # 获取此操作下到达的状态节点并将其加入边缘队列中
    return None

#用于计算当前状态到目标状态，计算h（n）
goal_dic = {
    1:(0,0), 2:(0,1), 3:(0,2),
    4:(1,0), 5:(1,1), 6:(1,2),
    7:(2,0), 8:(2,1), 0:(2,2)
}
# 输出状态
def PrintState(state):
    for i in state:
        print(i)
# 复制状态
def Copy(state):
    s = []
    for i in state: s.append(i[:])
    return s
# 获取空格的位置
def GetSpace(state):
    for y in range(len(state)):
        for x in range(len(state[y])):
            if state[y][x] == 0: return y, x
# 获取空格上移后的状态，不改变原状态
def Up(state):
    s = Copy(state)
    y, x = GetSpace(s)
    s[y][x], s[y - 1][x] = s[y - 1][x], s[y][x]   #将位置交换一下
    return s
# 获取空格下移后的状态，不改变原状态
def Down(state):
    s = Copy(state)
    y, x = GetSpace(s)
    s[y][x], s[y + 1][x] = s[y + 1][x], s[y][x]
    return s
# 获取空格左移后的状态，不改变原状态
def Left(state):
    s = Copy(state)
    y, x = GetSpace(s)
    s[y][x], s[y][x - 1] = s[y][x - 1], s[y][x]
    return s
# 获取空格右移后的状态，不改变原状态
def Right(state):
    s = Copy(state)
    y, x = GetSpace(s)
    s[y][x], s[y][x + 1] = s[y][x + 1], s[y][x]
    return s
#计算h（n），是表中每一个节点的和
def GetDistance(src):
    dic, d = goal_dic, 0
    for i in range(len(src)):
        for j in range(len(src[i])):
            pos = dic[src[i][j]]
            y, x= pos[0], pos[1]
            d += abs(y - i) + abs(x - j)
    return d
# 在该状态下，空格能够执行的操作
def GetActions(state):
    acts = []
    y, x = GetSpace(state)
    if x > 0:acts.append(Left)
    if y > 0:acts.append(Up)
    if x < len(state[0]) - 1:acts.append(Right)
    if y < len(state[0]) - 1: acts.append(Down)
    return acts
# 用于统一操作序列的函数
def Start(state):
    return
# 边缘队列中的节点类
class Node:
    state = None   # 八数码的状态，列表形式
    value = -1     # f（n），也就是启发值
    step = 0       # 初始状态到当前状态的距离，也就是执行了几步了
    action = Start  #到这个节点的状态，空格的操作
    parent = None,  # 父节点
    # 用状态和步数构造节点对象
    def __init__(self, state, step, action, parent):
        self.state = state
        self.step = step
        self.action = action
        self.parent = parent
        # 计算估计距离
        self.value = GetDistance(state) + step  #f=h+g
# 获取拥有最小启发值的元素索引，在已经扩展过的节点的列表里找
def GetMinIndex(queue):
    index = 0
    for i in range(len(queue)):    #队列的长度，队列是已经扩展的节点放的是
        node = queue[i]
        if node.value < queue[index].value:
            index = i
    return index
# 将状态转换为整数
def toInt(state):
    value = 0
    for i in state:
        for j in i:
            value = value * 10 + j
    return value


# 将链表倒序，返回链头和链尾
def reverse(node):
    if node.parent == None:
        return node, node
    head, rear = reverse(node.parent)
    rear.parent, node.parent = node, None
    return head, node

#初始状态
init_state = [
    [2, 4, 3],
    [1, 5, 6],
    [7, 8, 0]
]
# 目标状态
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
node= h(init_state, goal_state)
if node == None:
    print("无法从初始状态到达目标状态！")
else:
    node, rear = reverse(node)
    step=1
    all=0
    while node:
        # 启发值包括从起点到此节点的距离
        print("第",step, "步：", node.action.__name__,)
        PrintState(node.state)
        all=all+node.value
        node = node.parent
        step=step+1
print("总启发值为:",all)

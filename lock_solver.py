from collections import deque


def apply_move(config, module_idx, direction, rules):
    """
    应用一次移动操作，返回新的配置，越界则返回None
    :param config: 当前模块状态列表（1-7）
    :param module_idx: 要移动的主模块编号（1-5）
    :param direction: 移动方向，+1左移，-1右移
    :param rules: 游戏联动规则字典
    :return: 新的配置列表，或None（越界时）
    """
    new_config = config.copy()
    # 先计算所有模块的目标位置
    changes = {}
    # 主模块的移动
    changes[module_idx] = direction
    # 处理联动规则
    for target_mod, coeff in rules.get(module_idx, []):
        changes[target_mod] = changes.get(target_mod, 0) + direction * coeff

    # 应用所有变化并检查越界
    for mod, delta in changes.items():
        new_pos = new_config[mod - 1] + delta
        if not (1 <= new_pos <= 7):
            return None
        new_config[mod - 1] = new_pos
    return new_config


def solve_lock(initial_config, game_rules, target_pos=4):
    """
    BFS求解开锁步骤
    :param initial_config: 初始模块状态
    :param game_rules: 联动规则
    :param target_pos: 目标位置（默认中间位置4）
    :return: 步骤列表（模块编号、方向）和最终状态
    """
    target_config = [target_pos] * len(initial_config)
    visited = set()
    # 队列元素：(当前状态, 步骤列表)
    queue = deque([(tuple(initial_config), [])])
    visited.add(tuple(initial_config))

    while queue:
        current_config, steps = queue.popleft()
        # 检查是否已开锁
        if list(current_config) == target_config:
            return steps, list(current_config)
        # 尝试所有模块的左右移动
        for module in range(1, len(initial_config) + 1):
            for direction in [1, -1]:  # 1左移，-1右移
                new_config = apply_move(
                    list(current_config), module, direction, game_rules
                )
                if new_config is not None and tuple(new_config) not in visited:
                    visited.add(tuple(new_config))
                    new_steps = steps.copy()
                    # 记录移动方向：+表示左移，-表示右移
                    move_str = f"{module}{'+' if direction == 1 else '-'}"
                    new_steps.append(move_str)
                    queue.append((tuple(new_config), new_steps))
    return None, None


def render_lock_steps(steps):
    """
    将开锁步骤列表渲染为易读格式，每个步骤一行，带箭头符号表示移动方向与次数
    :param steps: 形如 ["2+", "3+", "1-", "1-", ...] 的步骤列表
    :return: 多行字符串，每行为一步的描述
    """
    if not steps:
        return "无有效步骤"

    # 先按模块+方向分组，统计次数
    grouped = []
    current = steps[0]
    count = 1
    for step in steps[1:]:
        if step == current:
            count += 1
        else:
            grouped.append((current, count))
            current = step
            count = 1
    grouped.append((current, count))

    lines = []
    for move, cnt in grouped:
        mod = int(move[0])
        direction = move[1]
        if direction == "+":
            dir_text = "左移"
            arrow = "←" * cnt
        else:  # "-"
            dir_text = "右移"
            arrow = "→" * cnt

        line = f"模块{mod} {dir_text}{cnt}次 {arrow}"
        lines.append(line)

    return "\n".join(lines)


# 让我们以旧营地惠斯勒旁边的小屋箱子为例
initial_config = [7,7,7,5]
game_rules = {
    1: [(2, -1),(3,-1),(4,1)],  # 移动模块1：仅模块1移动
    2: [(3, -1)],  # 移动模块2：模块3同向，模块5同向
    3: [],  # 移动模块3：模块5同向，模块1反向
    4: [(2, -1)],  # 移动模块4：模块3反向
}

# 运行求解
steps, final_state = solve_lock(initial_config, game_rules)

if steps:
    print("找到开锁步骤（格式：模块号+方向，+左移，-右移）：")
    print(render_lock_steps(steps))
    print("初始状态:", initial_config)
    print("最终状态:", final_state)
else:
    print("无法找到开锁步骤（可能无解或规则错误）")

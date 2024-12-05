from data import precedence_matrix, ind_symbols, rules


def crumple(stack, items, symbols):
    flag = True
    while flag:
        len_stack = len(stack) - 1
        while len_stack >= 1:
            for row in items:
                if " ".join(stack[-len_stack:]) == row:
                    stack[-len_stack:] = []
                    stack.append('char')
                    break
            len_stack -= 1

        return stack, items, symbols


def shift_reduce_parser(precedence_matrix, symbols, items):
    stack = ['@']  # Начальный символ в стеке
    stack.append(symbols[0])
    symbols.pop(0)
    symbols.append('$')
    while symbols:
        top_stack = stack[-1]
        next_input = symbols[0]

        if next_input == '$':
            for _ in range(10):
                stack, items, symbols = crumple(stack, items, symbols)
                if stack == ['@', 'char'] and symbols == ['$']:
                    return 'все ок'


        # Получаем индексы символов
        i = ind_symbols.index(top_stack)
        j = ind_symbols.index(next_input)

        # Получаем приоритет из матрицы предшествования
        precedence = precedence_matrix[i][j]

        if precedence <= 0:  # Сдвиг
            stack.append(next_input)
            symbols.pop(0)
        elif precedence > 0:  # Свертка
            stack, items, symbols = crumple(stack, items, symbols)
            print('свернули')
            if stack == ['@', 'char'] and symbols == ['$']:
                return 'все ок'

            elif stack == ['$']:
                for _ in range(50):
                    stack, items, symbols = crumple(stack, items, symbols)
                return 'все ок'

            stack.append(symbols[0])
            symbols.pop(0)

    return 'ошибка'


def do_it_now_beach(code: str):
    symbols = " ".join(i.strip() for i in code.split('\n'))
    print(symbols)
    f_row = []

    for item in symbols.split():
        if item in ind_symbols:
            f_row.append(item)
        elif item.isdigit():
            f_row.append('char')
        else:
            f_row.append('char')
    print(f_row)
    format_rules = []
    for i in rules:
        row = ''
        for j in i.split():
            if j in ind_symbols:
                row += j + ' '
            else:
                row += 'char '
        format_rules.append(row.rstrip())

    # Запускаем анализ
    result = shift_reduce_parser(precedence_matrix, f_row, format_rules)
    print(result)
    return result

class Solver(object):
    def __init__(self, sim_specs=None, dimension_elements=None, name_space=None):
        
        self.sim_specs = sim_specs
        self.dimension_elements = dimension_elements
        self.name_space = name_space
        
        ### Functions ###

        def logic_and(a, b):
            return (a and b)
        
        def logic_or(a, b):
            return (a or b)
        
        def logic_not(a):
            return (not a)
        
        def greater_than(a, b):
            if a > b:
                return True
            elif a <= b:
                return False
            else:
                raise Exception()

        def less_than(a, b):
            if a < b:
                return True
            elif a >= b:
                return False
            else:
                raise Exception()

        def no_greater_than(a, b):
            if a <= b:
                return True
            elif a > b:
                return False
            else:
                raise Exception()

        def no_less_than(a, b):
            if a >= b:
                return True
            elif a < b:
                return False
            else:
                raise Exception()

        def equals(a, b):
            if a == b:
                return True
            elif a != b:
                return False
            else:
                raise Exception

        def plus(a, b):
            # print(self.HEAD, 'plus', a,type(a), b, type(b))
            try:
                return a + b
            except TypeError as e:
                if type(a) is dict and type(b) is dict:
                    o = dict()
                    for k in a:
                        o[k] = a[k] + b[k]
                    return o
                else:
                    raise e

        def minus(a, b):
            # print(self.HEAD, 'minus', a,type(a), b, type(b))
            try:
                return a - b
            except TypeError as e:
                if type(a) is dict and type(b) is dict:
                    o = dict()
                    for k in a:
                        o[k] = a[k] - b[k]
                    return o
                elif type(a) is dict and type(b) in [int, float]:
                    o = dict()
                    for k in a:
                        o[k] = a[k] - b
                    return o
                elif type(a) in [int, float] and type(b) is dict:
                    o = dict()
                    for k in b:
                        o[k] = a - b[k]
                    return o
                else:
                    raise e

        def times(a, b):
            try:
                return a * b
            except TypeError as e:
                if type(a) is dict and type(b) is dict:
                    o = dict()
                    for k in a:
                        o[k] = a[k] * b[k]
                    return o
                elif type(a) is dict and type(b) in [int, float]:
                    o = dict()
                    for k in a:
                        o[k] = a[k] * b
                    return o
                elif type(a) in [int, float] and type(b) is dict:
                    o = dict()
                    for k in b:
                        o[k] = a * b[k]
                    return o
                else:
                    raise e

        def divide(a, b):
            try:
                return a / b
            except TypeError as e:
                if type(a) is dict and type(b) is dict:
                    # print(self.HEAD, 'a/b', a, b)
                    o = dict()
                    for k in a:
                        o[k] = a[k] / b[k]
                    return o
                elif type(a) is dict and type(b) in [int, float]:
                    o = dict()
                    for k in a:
                        o[k] = a[k] / b
                    return o
                elif type(a) in [int, float] and type(b) is dict:
                    o = dict()
                    for k in b:
                        o[k] = a / b[k]
                    return o
                else:
                    raise e

        def con(a, b, c):
            if a:
                return b
            else:
                return c

        def step(stp, time):
            # print('step:', stp, time)
            if sim_specs['current_time'] >= time:
                # print('step out:', stp)
                return stp
            else:
                # print('step out:', 0)
                return 0
        
        ### Function mapping ###

        self.built_in_functions = {
            'AND':      logic_and,
            'OR':       logic_or,
            'NOT':      logic_not,
            'GT':       greater_than,
            'LT':       less_than,
            'NGT':      no_greater_than,
            'NLT':      no_less_than,
            'EQS':      equals,
            'PLUS':     plus,
            'MINUS':    minus,
            'TIMES':    times,
            'DIVIDE':   divide,
            'MIN':      min,
            'MAX':      max,
            'CON':      con,
            'STEP':     step,
        }

        self.time_related_functions = [
            'INIT',
            'DELAY',
            'HISTORY',
        ]

        self.custom_functions = {}
        self.time_expr_register = {}
        
        self.id_level = 1

        self.HEAD = "SOLVER"

    def calculate_node(self, parsed_equation, node_id='root', subscript=None):
        self.id_level += 1

        # print(self.HEAD, 'processing node {} on subscript {}:'.format(node_id, subscript))
        # if type(parsed_equation) is dict:
        #     for k, p in parsed_equation.items():
        #         print(self.HEAD, k, p.nodes(data=True))
        # else:
        #     print(self.HEAD, parsed_equation.nodes(data=True))
        
        if type(parsed_equation) is dict:
            # print(self.HEAD, 'type of parsed_equation: dict')
            value = dict()
            for sub, sub_equaton in parsed_equation.items():
                # print(self.HEAD, 'sub', sub)
                value[sub] = self.calculate_node(parsed_equation=sub_equaton, node_id='root', subscript=sub)
            # print(self.HEAD, 'v1', value)
        else:
            # print(self.HEAD, 'type of parsed_equation: graph')
            if node_id == 'root':
                node_id = list(parsed_equation.successors('root'))[0]
            node = parsed_equation.nodes[node_id]
            # print(self.HEAD, 'node:', node_id, node)
            operator = node['operator']
            operands = node['operands']
            if operator[0] == 'IS':
                # print(self.HEAD, 'oprt1')
                # print(self.HEAD, 'o1')
                value = operands[0][1]
                # print(self.HEAD, 'v2', value)
            elif operator[0] == 'EQUALS':
                # print(self.HEAD*self.id_level, 'operator v3', operator)
                # print(self.HEAD*self.id_level, 'operands v3', operands)
                if operands[0][0] == 'NAME':
                    if subscript:
                        try:
                            value = self.name_space[operands[0][1]][subscript]
                            # print(self.HEAD*self.id_level, 'v3.1.1', value)
                        except TypeError:
                            value = self.name_space[operands[0][1]]
                            # print(self.HEAD*self.id_level, 'v3.1.2', value)
                    else:
                        # print(self.HEAD*self.id_level, 'v3.1.3.0', self.name_space)
                        value = self.name_space[operands[0][1]]
                        # print(self.HEAD*self.id_level, 'v3.1.3', value, operands)
                    # print(self.HEAD*self.id_level, 'v3.1', value)
                elif operands[0][0] == 'FUNC':
                    # print(self.HEAD, 'o3')
                    value = self.calculate_node(parsed_equation, node_id, subscript)
                    # print(self.HEAD*self.id_level, 'v3.2', value)
                else:
                    # print(self.HEAD, 'o4')
                    raise Exception()
                # print(self.HEAD*self.id_level, 'v3', value)
            
            elif operator[0] == 'SPAREN': # TODO this part is too dynamic, therefore can be slow. Need to resolve this when compiling.
                var_name = operands[0][1]
                # print('a1', var_name, subscript)
                if len(operands) == 1: # only var_name; no subscript is specified
                    # print('a1.1')
                    # this could be 
                    # (1) this variable (var_name) is not subscripted therefore the only value of it should be used;
                    # (2) this variable (var_name) is subscripted in the same way as the variable using it (a contextual info is needed and provided in the arg subscript)
                    if subscript:
                        # print('a1.1.1')
                        value = self.name_space[var_name][subscript] 
                    else:
                        # print('a1.1.2')
                        value = self.name_space[var_name]
                    # print(self.HEAD, 'v4', value)
                else: # there are explicitly specified subscripts in oprands
                    # print('a1.2')
                    if subscript: # subscript is explicitly specified; like a[Element_1] or a[Dimension_1]
                        # print('a1.2.0', subscript, self.dimension_elements)
                        subscript_from_operands = list()
                        operands_containing_subscript = operands[1:]
                        for i in range(len(operands_containing_subscript)):
                            if operands_containing_subscript[i][1] in self.dimension_elements.keys(): # it's sth like Dimension_1
                                # print('a1.2.0.1')
                                subscript_from_operands.append(subscript[i]) # take the element from arg subscript in the same position to replace Dimension_1
                            else: # it's sth like Element_1
                                # print('a1.2.0.2')
                                subscript_from_operands.append(operands_containing_subscript[i][1]) # add to list directly
                        subscript_from_operands = tuple(subscript_from_operands)
                        # print('a1.2.1', subscript_from_operands)
                        value = self.name_space[var_name][subscript_from_operands] # try if subscript is Element_1

                    else: # subscript is not explicitly specified
                        # print('a1.2.2')
                        # like a[Dimension1] -> Which element of Dimension1 to use, 
                        # depends on the other variable.

                        subscript = tuple(operand[1] for operand in operands[1:]) # use tuple to make it hashable
                        # print(self.HEAD, 'subscripts', subscripts, 'subscript of interest', subscript)
                        value = self.name_space[var_name][subscript]
                    # print(self.HEAD, 'v5', value)
            
            elif operator[0] == 'PAREN':
                value = self.calculate_node(parsed_equation, operands[0][2])
                # print(self.HEAD, 'v6', value)

            elif operator[0] in self.built_in_functions.keys(): # plus, minus, con, etc.
                # print(self.HEAD*self.id_level, 'operator v7', operator, operands)
                func_name = operator[0]
                function = self.built_in_functions[func_name]
                oprds = []
                for operand in operands:
                    # print(self.HEAD, 'oprd', operand)
                    v = self.calculate_node(parsed_equation, operand[2])
                    # print(self.HEAD, 'value', v)
                    oprds.append(v)
                # print(self.HEAD, 'oprds', oprds)
                value = function(*oprds)
                # print(self.HEAD*self.id_level, 'v7', value)
            
            elif operator[0] in self.custom_functions.keys(): # graph functions
                # print(self.HEAD, 'custom func operator', operator)
                func_name = operator[0]
                function = self.custom_functions[func_name]
                oprds = []
                for operand in operands:
                    # print(self.HEAD, 'oprd', operand)
                    v = self.calculate_node(parsed_equation, operand[2])
                    # print(self.HEAD, 'value', v)
                    oprds.append(v)
                # print(self.HEAD, 'oprds', oprds)
                value = function(*oprds)
                # print(self.HEAD, 'v8', value)

            elif operator[0] in self.time_related_functions: # init, delay, etc
                # print(self.HEAD, 'time-related func. operator:', operator, 'operands:', operands)
                func_name = operator[0]
                if func_name == 'INIT':
                    if tuple(operands[0]) in self.time_expr_register.keys():
                        value = self.time_expr_register[tuple(operands[0])]
                    else:
                        value = self.calculate_node(parsed_equation, operands[0][2])
                        self.time_expr_register[tuple(operands[0])] = value
                elif func_name == 'DELAY':
                    # expr value
                    expr_value = self.calculate_node(parsed_equation, operands[0][2])
                    if tuple(operands[0]) in self.time_expr_register.keys():
                        self.time_expr_register[tuple(operands[0])].append(expr_value)
                    else:
                        self.time_expr_register[tuple(operands[0])] = [expr_value]
                    
                    # init value
                    if len(operands) == 2: # there's no initial value specified -> use the delyed expr's initial value
                        init_value = self.time_expr_register[tuple(operands[0])][0]
                    elif len(operands) == 3: # there's an initial value specified
                        init_value = self.calculate_node(parsed_equation, operands[2][2])
                    else:
                        raise Exception("Invalid initial value for DELAY in operands {}".format(operands))

                    # delay time
                    delay_time = self.calculate_node(parsed_equation, operands[1][2])
                    if delay_time > (self.sim_specs['current_time'] - self.sim_specs['initial_time']): # (- initial_time) because simulation might not start from time 0
                        value = init_value
                    else:
                        delay_steps = delay_time / self.sim_specs['dt']
                        value = self.time_expr_register[tuple(operands[0])][-int(delay_steps+1)]
                elif func_name == 'HISTORY':
                    # expr value
                    expr_value = self.calculate_node(parsed_equation, operands[0][2])
                    if tuple(operands[0]) in self.time_expr_register.keys():
                        self.time_expr_register[tuple(operands[0])].append(expr_value)
                    else:
                        self.time_expr_register[tuple(operands[0])] = [expr_value]
                    
                    # historical time
                    historical_time = self.calculate_node(parsed_equation, operands[1][2])
                    if historical_time > self.sim_specs['current_time']:
                        value = 0
                    else:
                        historical_steps = (historical_time - self.sim_specs['initial_time']) / self.sim_specs['dt']
                        value = self.time_expr_register[tuple(operands[0])][int(historical_steps)]
                else:
                    raise Exception('Unknown time-related operator {}'.format(operator[0]))
                # print(self.HEAD, 'v9', value)
            else:
                raise Exception('Unknown operator {}'.format(operator[0]))
        
        # print(self.HEAD, 'value for {} {}'.format(node_id, subscript), value)
        self.id_level -= 1
        try:
            return value[subscript]
        except KeyError as e: # due to dict[None]
            return value
        except TypeError as e: # due to float[sub]
            return value


if __name__ == '__main__':
    from Parser import Parser

    name_space= {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': {('ele1',):8},
        'aa': True,
        'ba': False,
        'bb': 0,
        'bc': 1,
        'ac': 2,
        'cc': 3,
        'i' : {('ele1',):9}
    }

    tests = [
        (1, 'a', 1),
        (2, 'a+b-c', 0),
        (3, 'a+b-2', 1),
        (4, 'a*b', 2),
        (5, 'a/2', 0.5),
        (6, 'INIT(a)', None),
        (7, 'DELAY(a, 1)', None),
        (8, 'a*((b+c)-d)', 1),
        (9, 'a > b', False),
        (10, 'a < 2', True),
        (11, 'IF aa THEN bb ELSE cc', 0),
        (12, 'IF aa THEN IF ba THEN bb ELSE bc ELSE ac', 1),
        (13, 'h[ele1]', 8),
        (14, 'IF (a + h[ele1]) > (c * 10) THEN INIT(d / e) ELSE f - g', None),
        (15, 'h+i-i', {('ele1',): 8}),
        (16, '10-4-3-2-1', 0)
    ]

    # for test in tests[12:13]:
    for test in tests:
        if test[2] is not None:
            n = test[0]
            formula = test[1]
            result = test[2]
            parser = Parser()
            graph = parser.parse(formula)
            
            # print('graph_nodes', graph.nodes(data=True))
            # print('graph_edges', graph.edges())
            
            # fig, ax = plt.subplots()
            # labels = {}
            # labels_operators = nx.get_node_attributes(graph, 'operator')
            # labels_operands = nx.get_node_attributes(graph, 'operands')
            # for id, label_operator in labels_operators.items():
            #     labels[id] = str(id) + '\n' + 'operator:' + str(label_operator) + '\n' + 'operands:' + str(labels_operands[id])
            # labels['root'] = 'root'
            # nx.draw_shell(graph, with_labels=True, labels=labels, node_color='C1')
            # plt.show()
            
            print('{:2} formula: {:30}'.format(n, formula))
            solver = Solver(name_space=name_space)
            outcome = solver.calculate_node(graph)
            # if outcome != result:
            print('   outcome: {:<20} type: {:20} {:2} {:5}'.format(str(outcome), str(type(outcome)), str(n), str(outcome==result)))
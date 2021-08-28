import copy
import time


class BlockWorldAgent:

    def __init__(self):
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        # Add your code here! Your solve method should receive
        # as input two arrangements of blocks. The arrangements
        # will be given as lists of lists. The first item in each
        # list will be the bottom block on a stack, proceeding
        # upward. For example, this arrangement:
        # [["A", "B", "C"], ["D", "E"]]
        # represents two stacks of blocks: one with B on top
        # of A and C on top of B, and one with E on top of D.
        #
        # Your goal is to return a list of moves that will convert
        # the initial arrangement into the goal arrangement.
        # Moves should be represented as 2-tuples where the first
        # item in the 2-tuple is what block to move, and the
        # second item is where to put it: either on top of another
        # block or on the table (represented by the string "Table").
        #
        # For example, these moves would represent moving block B
        # from the first stack to the second stack in the example
        # above:[("C", "Table"), ("B", "E"), ("C", "A")]

        start = time.time()

        class State:
            def __init__(self, first_stack, second_stack, total_num, moves=None):
                if moves is None:
                    moves = []
                self.first_stack = first_stack
                self.second_stack = second_stack
                self.total_num = total_num
                self.moves = moves

            def __eq__(self, other):
                return (self.first_stack == other.first_stack and self.second_stack == other.second_stack
                        and self.total_num == other.total_num and self.moves == other.moves)

            def goal_state_move(self):
                while self.difference() != 0:
                    self = self.select_move()
                return self.moves

            def select_move(self):  # will select and return the best move
                # first try moving the top block to a stack, if the diff is not reduced, then move it to the temp_table
                for index, stack in enumerate(self.first_stack):
                    for index2, stack2 in enumerate(self.first_stack):
                        if index != index2:  # don't move to itself stack
                            curr_table, move = self.valid_state_move(self.first_stack, index, index2)
                            new_state = State(curr_table, self.second_stack, self.total_num, copy.copy(self.moves))
                            new_state.moves.append(move)
                            if new_state.difference() < self.difference():
                                return new_state

                # move the top block to the temp_table, skip if it is already on the table (itself alone on a table)
                for index, stack in enumerate(self.first_stack):
                    if len(stack) > 1:  # not it self alone
                        curr_table, move = self.valid_state_move(self.first_stack, index, -1)  # -1 means table
                        new_state = State(curr_table, self.second_stack, self.total_num, copy.copy(self.moves))
                        new_state.moves.append(move)
                        if new_state.difference() <= self.difference():
                            return new_state

            def valid_state_move(self, table, start_index, end_index):
                temp_table = copy.deepcopy(table)
                left = temp_table[start_index]
                top_block = left.pop()
                right = []

                if end_index < 0:  # move to table (-1)
                    temp_table.append(right)
                    move = (top_block, 'Table')
                else:  # move to stack
                    right = temp_table[end_index]
                    move = (top_block, right[-1])
                right.append(top_block)

                if len(left) == 0:
                    temp_table.remove(left)
                return temp_table, move

            def difference(self):
                same_num = 0
                # compare each stack on two stacks
                for left in self.first_stack:
                    for right in self.second_stack:
                        index = 0
                        while index < len(left) and index < len(right):
                            if left[index] == right[index]:
                                same_num += 1
                                index += 1
                            else:
                                break
                diff = self.total_num - same_num
                return diff

        total_num = 0
        for ls in initial_arrangement:
            for e in ls:
                total_num += 1
        state = State(initial_arrangement, goal_arrangement, total_num)
        solution = state.goal_state_move()

        end = time.time()
        run_time = str((end - start) * 1000)
        print("Running time:" + run_time + "ms")
        return solution

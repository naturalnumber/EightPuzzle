from typing import Generic, TypeVar

from framework import N, CostNode, StateNode, Action

# This is the generic type hint for whatever node type is ultimately used. It should descend from CostNode
D = TypeVar('D')


# This is the class that models the various search algorithms
class Searcher(Generic[D]):
    # Consider implementing: Uniform Cost Search
    methods = ("BFS", "DFS", "DLS", "IDS")  # , "BDS"
    method_names = ("Breadth First Search", "Depth First Search", "Depth-limited Search",
                    "Iterative Deepening Search")  # , "Bidirectional Search"

    def __init__(self, method, start: D, is_graph: bool = False, uniform: bool = True, limit: N = None,
                 increment: N = None, override: bool = False):
        """
        This class will perform the requested search starting from the given initial node.

        :param method: The short form name of the search method, found in Searcher.methods
        :param start: The initial node
        :param is_graph: Whether or not the search should be graph or tree search
        :param uniform: Whether or not the costs are uniform
        :param limit: The depth/cost limit to use (if DLS or IDS)
        :param increment: The depth increment to use (if IDS)
        :param override: Whether to use the above limits and increments regardless of search type
        """
        # Stored parameters
        self.method: str = method
        self.start: CostNode = start
        self.uniform: bool = uniform
        self.is_graph: bool = is_graph
        self.limit = limit
        self.increment = increment

        # Internal values
        self._limit = None
        self._increment = None

        # Advanced option flags/variables
        self.track_complexity = False

        self.debug = False

        self.trace = False
        self.show_states = False
        self.track_expansion = False
        self.trace_functions = False

        self.step_through = False

        self.nodes_seen = 0

        # Method initializations
        if method == "BFS":
            from collections import deque

            # Data structure setup
            self.frontier: deque = deque()
            self.explored: set = set()

            # Method assignments
            self._add_to_frontier = self.frontier.append
            self._get_frontier_size = self.frontier.__len__
            self._get_from_frontier = self.frontier.popleft
            self._empty_explored = self.explored.clear
            self._add_to_explored = self.explored.add
        elif method in ["DFS", "DLS", "IDS"]:
            # Data structure setup
            self.frontier: list = []
            self.explored: set = set()

            # Method assignments
            self._add_to_frontier = self.frontier.append
            self._get_frontier_size = self.frontier.__len__
            self._get_from_frontier = self.frontier.pop
            self._empty_explored = self.explored.clear
            self._add_to_explored = self.explored.add
        elif method == "BDS":
            raise NotImplementedError("Bidirectional Search")

        # Depth limit parameter configuration
        if method in ["DLS", "IDS"] or (override and limit): self._limit = limit
        if method in ["IDS"] or (override and increment): self._increment = increment

    def search(self) -> D:
        """
        This method initiates the requested search.
        :return: The goal found or None
        """
        # Debug output
        if self.debug: print(f"Searcher.search() @ " + self.start.describe())

        # Optional output
        if self.trace_functions:
            print(f"\tself._add_to_frontier = {self._add_to_frontier}")
            print(f"\tself._get_frontier_size = {self._get_frontier_size}")
            print(f"\tself._get_from_frontier = {self._get_from_frontier}")
            print(f"\tself._empty_explored = {self._empty_explored}")
            print(f"\tself._add_to_explored = {self._add_to_explored}")

        # Data structure initialization
        self._add_to_frontier(self.start)
        if self.is_graph: self._empty_explored()

        # Search loop
        while self._get_frontier_size() > 0:
            # Advanced option pause
            if self.step_through: input()

            # Choose node from frontier
            current: StateNode = self._get_from_frontier()

            # Advanced statistic
            if self.track_complexity: self.nodes_seen += 1

            # Optional output
            if self.trace_functions:
                print(f"\tself._add_to_frontier = {self._add_to_frontier}")
                print(f"\tself._get_frontier_size = {self._get_frontier_size}")
                print(f"\tself._get_from_frontier = {self._get_from_frontier}")
                print(f"\tself._empty_explored = {self._empty_explored}")
                print(f"\tself._add_to_explored = {self._add_to_explored}")

            if self.trace: print(f"\n\tFrontier gives: " + current.describe())

            if self.show_states:
                # print(str(current.state))
                for line in str(current.state).split('\n'): print("\t\t" + line)

            # Goal checking
            if current.is_goal():
                if self.trace: print(f"\tGoal found!\n")
                return current

            # Graph search node tracking
            if self.is_graph: self._add_to_explored(current.state)

            # Limit checking and expansion
            if (self._limit and current.cost < self._limit) or not self._limit:
                if self.is_graph:
                    expansion = current.expand(self.explored)  # Filters based on set of seen states
                else:
                    expansion = current.expand()

                # sorts expanded nodes in non-uniform case
                if not self.uniform: expansion.sort()

                # Optional output
                if self.trace:
                    print(f"\tExpansion gives {len(expansion)} new configurations, via:")
                    a: Action
                    e: 'StateNode'
                    action: Action
                    actions = {e.action for e in expansion if e.action}
                    if len(actions) == 0:
                        actions = {a for a in current.actions() if (a.result and (a.result in expansion))}
                    for action in actions:
                        print("\t\t" + str(action))

                if self.track_expansion:
                    n = 1
                    l = 0
                    lines = []
                    # print(f"\n")
                    for node in expansion:
                        l = 0
                        for line in str(node.state).split('\n'):
                            # print(line)
                            if n == 1:
                                lines.append("\t\t")
                            elif len(expansion) * len(line) < 30:
                                lines[l] += "\t\t"
                            else:
                                lines[l] += "\t"
                            lines[l] += line
                            # print(lines)
                            l += 1
                        n += 1
                        # May need to pad for uneven states here
                    for line in lines: print(line)
                    # print('\n')

                # Add expansion to frontier
                for e in expansion:
                    self._add_to_frontier(e)

            # Optional output
            elif self.trace and self._limit:
                print(f"\tLimit ({self._limit}) reached!")

        # Limit incrementation
        if self._limit and self._increment:
            self._limit += self._increment

            # Optional output
            if self.trace:
                print(f"\tLimit increased to {self._limit}")
                print("\n")
            return self.search()

        if self.trace: print("\n")
        return None  # Failed search

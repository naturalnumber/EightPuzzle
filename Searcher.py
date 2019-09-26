from Framework import ANode


class Searcher:
    def __init__(self, method, start: ANode):
        self.method = method
        self.start = start

        self.frontier = []
        self.explored = set()

        self._add_to_frontier = self.frontier.append
        self._get_frontier_size = self.frontier.__sizeof__
        self._get_from_frontier = self.frontier.pop()
        self._empty_explored = self.explored.clear
        self._add_to_explored = self.explored.add

    def _tree_search_(self) -> ANode:
        self._add_to_frontier(self.start)

        while self._get_frontier_size() > 0:
            current = self._get_from_frontier()
            if current.is_goal():
                return current
            else:
                self._add_to_frontier(current.expand())
        return False

    def _graph_search_(self) -> ANode:
        self._add_to_frontier(self.start)
        self._empty_explored()

        while self._get_frontier_size() > 0:
            current = self._get_from_frontier()
            if current.is_goal():
                return current
            else:
                self._add_to_explored(current)
                self._add_to_frontier(current.expand(self.explored))
        return False

import abc


class Search():
    @abc.abstractmethod
    def search(self, initial_state, goal_state):
        pass
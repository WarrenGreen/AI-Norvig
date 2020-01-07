from abc import abstractmethod


class Problem:
    @abstractmethod
    def generate_successors(self, state):
        """
        Args:
            state (List): representation of current state

        Returns:
            (Generator[List, None, None]) - representation of state

        """
        raise NotImplementedError()

    @abstractmethod
    def get_value(self, state):
        """
        Args:
            state: representation of current state

        Returns:
            (int) - value of current state

        """
        raise NotImplementedError()

    @abstractmethod
    def is_terminal(self, state):
        """

        Args:
            state: representation of current state

        Returns:
            (bool) - whether provided state is a terminal state

        """
        raise NotImplementedError()

    @abstractmethod
    def create_start(self):
        """

        Returns:
            (List) - valid starting state

        """

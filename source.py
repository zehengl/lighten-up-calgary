from abc import abstractmethod, ABC


class LightenUpCalgary(ABC):

    base_url = "https://lightenupcalgary.ca/"

    @classmethod
    @abstractmethod
    def get_addresses(self):
        pass

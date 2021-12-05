class Book:
    def __init__(self, isbn="", name="", description="", is_loaned=None, author_id=""):
        self._id = -1
        self.isbn = isbn
        self.name = name
        self.description = description
        self.is_loaned = is_loaned
        self.author_id = author_id


class Client:
    def __init__(self, first_name="", second_name=""):
        self._id = -1
        self.first_name = first_name
        self.second_name = second_name
        self._full_name = first_name + " " + second_name

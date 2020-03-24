import json

# create model classes here
class User:
    # constructor
    def __init__(self, name, email, id_number):
        self.name = name
        self.email = email
        self.id_number = id_number

    def serialize(self):
        return {"name": self.name, "email": self.email, "id": self.id_number}


class Mentor(User):
    pass


class Client(User):
    # constructor
    def __init__(self, name, email, id_number, notes, attachments):
        super().__init__(name, email, id_number)
        self.notes = notes
        self.attachments = attachments
    
    def serialize(self):
        new_dict = super().serialize()
        new_dict.update({"notes": self.notes, "attachments": self.attachments})
        return new_dict


class Volunteer(User):
    #constructor
    def __init__(self, name, email, id_number, notes, attachments):
        super().__init__(name, email, id_number)
        self.notes = notes
        self.attachments = attachments

    def serialize(self):
        new_dict = super().serialize()
        new_dict.update({"notes": self.notes, "attachments": self.attachments})
        return new_dict


class Donor(User):
    def __init__(self, name, email, id_number, notes, total_donated):
        super().__init__(name, email, id_number)
        self.notes = notes
        self.total_donated = total_donated

    def serialize(self):
        new_dict = super().serialize()
        new_dict.update({"notes": self.notes, "total_donated": self.total_donated})
        return new_dict

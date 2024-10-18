from models.Subject import Subject


class SubjectService:
    def __init__(self, db) -> None:
        self.db =db

    def get_subjects(self):
        """
        Get all subjects
        :return:
            list[Subject]: a list of all subjects in the database
        """
        result = self.db.query(Subject).all()
        return result

    def get_subject(self, id):
        """
        Get subject by id
        :param id: The id of the resource
        :return: The subject fund
        """
        result = self.db.query(Subject).filter(Subject.id == id).first()
        return result

    def create(self, subject: Subject):
        """
        Create a new subject
        :param self: the current object
        :param subject: the model to be created
        :return:
        """
        # define new model
        new_subject = Subject(**subject.dict())
        # store in database
        self.db.add(new_subject)
        # commit changes
        self.db.commit()
        return

    def update(self, id: int, data: Subject):
        """
        Update a subject
        :param id: the id of the model
        :param data: the data to be updated on model
        :return:
        """
        # load model from database
        subject = self.db.query(Subject).filter(Subject.id == id).first()
        # set model data
        subject.name = data.name
        subject.description = data.description
        # commit changes
        self.db.commit()
        return

    def delete(self, subject: Subject):
        """
        Delete a subject
        :param subject: the model to be deleted
        :return:
        """
        self.db.delete(subject)
        self.db.commit()
        return
from django.db import models

class PinchartManager(models.Manager):
    pass

class WordManager(models.Manager):
    pass

class BitDescriptionManager(models.Manager):
    pass

class SequenceManager(models.Manager):
    
    def copy(self, new_name="None"):
        """
         copies entire sequence to another 
        """

        # if there was no new name supplied,
        # just call it with the original name
        # and copy.
        if new_name is None:
            new_name = self.name + " COPY"

        # create the new sequence()
        new_sequence = self.create(name=new_name)
        new_sequence.save()

        # get the steps
        steps = self.steps.all().order_by('number')

        # copy all of the steps
        for i in steps:

            # make a copy of the existing step
            new_step = i

            # change the sequence that the step is 
            # attached to, to the squence being copied
            new_step.sequence = new_sequence

            # save the new step in the new seqence
            new_step.save()

        return new_sequence

class StepManager(models.Manager):

    def insert(self, sequence_id, step_number):
        """
            Inserts a new step into a sequence at the
            given step number
        """
        # gets the steps that we need to move
        steps = self.filter(sequence=sequence_id, number__gte=step_number).order_by('number')

        # increment all of the step numbers
        # to make room for the new step
        for i in steps:
            i.number = i.number + 1
            i.save()

        # create the new step in at the correct number
        new_step = self.create(sequence=sequence_id, number=step_number)

        return new_step

    def remove(self, sequence_id, step_number):
        """
            Removes a step at the current step number
            and moves the steps beyond the step number
            up in the order
        """
        # get the step to delete
        delete_step = self.filter(sequence=sequence_id, number=step_number).order_by('number')

        # delete the step
        delete_step.delete()

        # get the steps to decrement
        steps = self.filter(number__gt=step_number)

        # decrement the step numbers
        for i in steps:
            i.number = i.number - 1
            i.save()

class StepDataManager(models.Manager):
    pass
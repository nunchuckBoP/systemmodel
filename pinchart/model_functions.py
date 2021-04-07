from pinchart.models import Sequence, Step

def copy_sequence(sequence_id, new_name):

    # get the seqence to be copied
    sequence = Sequence.objects.filter(pk=sequence_id)

    # get the steps that need to be copied
    sequence_steps = Step.objects(sequence=sequence)

    # new sequence insance
    new_sequence = Sequence(name=new_name)

    # save the new sequence
    saved_sequence = new_sequence.save()

    # loop through the steps and create new ones
    # for the new sequence
    for a_step in sequence_steps:

        new_step = Step(
            sequence=saved_sequence,
            word=a_step.word,
            number = a_step.number,
            description = a_step.description,
            value_dint = a_step.value_dint,
            value_real = a_step.value_real,
            value_string = a_step.value_string,
            value_int = a_step.value_int
        )

        new_step.save()

def insert_sequence_step(sequence_id, step_number):

    steps = Sequence.objects.filter(pk=sequence_id, number__gte=step_number).order_by('number')

    # increment the step numbers
    for a_step in steps:
        a_step.number = a_step.number + 1
        a_step.save()

    # create a new step, save it, and return it
    new_step = Step(number=step_number)
    new_step.save()
    return new_step

def remove_sequence_step(sequence_id, step_number):

    delete_step = Sequence.objects.filter(pk=sequence_id, number=step_number)
    steps = Sequence.objects.filter(pk=sequence_id, number__gt=step_number).order_by('number')

    # delete the step
    delete_step.delete()

    for a_step in steps:
        a_step.number = a_step.number - 1
        a_step.save()

    
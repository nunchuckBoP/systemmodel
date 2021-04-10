from pinchart import models

def copy_pinchart(pinchart_object, new_name):
    """
        COPIES A PINCHART FROM ONE TO ANOTHER
    """
    
    # copy and save the new pinchart
    new_pinchart = pinchart_object
    new_pinchart.pk = None
    new_pinchart.name = new_name
    new_pinchart.save()

    # get the words
    words = models.Word.filter(pinchart=pinchart_object)

    # copy the words to the new pinchart
    for a_word in words:
        new_word = a_word
        new_word.pk = None
        new_word.pinchart = new_pinchart
        new_word.save()

    # get the sequences
    sequences = pinchart_object.sequences.all()

    for a_sequence in sequences:

        # copy the sequence from the source pinchart to the new one
        copy_sequence(a_sequence, new_pinchart)

def copy_sequence(sequence_object, dest_pinchart, new_name=None):
    """
        COPIES A SEQUENCE FROM ONE PINCHART TO ANOTHER
    """
    
    # copy the new sequence
    new_sequence = sequence_object
    new_sequence.pk = None
    new_sequence.pinchart = dest_pinchart
    if new_name is not None:
        new_sequence.name = new_name
    new_sequence.save()

    # get the steps for the sequence
    steps = sequence_object.steps

    # loop through the steps and copy each one
    for a_step in steps:

        # copy the step
        copy_step(a_step, new_sequence)


def copy_step(step_object, dest_sequence, step_number=None):
    """
        COPIES A STEP FROM ONE SEQUENCE TO ANOTHER
    """
    # copy the step object
    new_step = step_object
    new_step.pk = None
    if step_number is not None:
        new_step.number = step_number
    new_step.sequence = dest_sequence
    new_step.save()

    # gets the step data words
    step_data_words = step_object.step_data

    for a_step_data_word in step_data_words:

        # copies the step data word 
        copy_step_data(a_step_data_word, new_step)


def copy_step_in_sequence(step_object, step_number_int):
    """
        COPIES ONE STEP IN A SEQUENCE TO A NEW STEP 
        IN THE SEQUENCE
    """
    new_step = step_object
    new_step.pk = None
    new_step.number = step_number_int
    new_step.save()

    # get the step data words
    step_data_words = step_object.step_data
    
    for a_step_data_word in step_data_words:

        copy_step_data(a_step_data_word, new_step)

def copy_step_data(step_data_word, dest_step):
    """
        COPIES STEP DATA FROM ONE STEP TO ANOTHER
    """
    new_step_data_word = step_data_word
    new_step_data_word.pk = None
    new_step_data_word.step = dest_step
    new_step_data_word.save()
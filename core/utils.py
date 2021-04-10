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

def copy_sequence(sequence_object, new_pinchart_object, new_name=None):
    """
        COPIES A SEQUENCE FROM ONE PINCHART TO ANOTHER
    """


def copy_step(step_object, dest_sequence):
    """
        COPIES A STEP FROM ONE SEQUENCE TO ANOTHER
    """
    pass

def copy_step_data():
    """
        COPIES STEP DATA FROM ONE STEP TO ANOTHER
    """
    pass
ANNOTATION_UNIT_PADDING = 75

def annotation_log_label():
    """
    Provides a label for logging in the annotation section to make it easier to search on.
    Changing this label will be uniform throughout the annotation section.
    """
    return 'Annotation:'


def format_annotation_logging(annotation_unit, dataset=""):
    """
    Provides a formatted string for logging that is consistent with
    annotation unit's genomic_unit and corresponding dataset to the console
    The string is padded to make the logs uniform and easier to read.
    """
    if dataset != "":
        annotation_unit_string = f"{annotation_unit.get_genomic_unit()} for {dataset}"
    else:
        annotation_unit_string = annotation_unit.to_name_string()
    return f"{annotation_log_label()} {annotation_unit_string}".ljust(ANNOTATION_UNIT_PADDING)
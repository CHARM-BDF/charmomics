""" Enumerations for the CHARMomics project. """

import logging

from enum import Enum

logger = logging.getLogger(__name__)


class GenomicUnitType(str, Enum):
    """Enumeration of the different types of genomic units that can be analyzed"""

    GENE = "gene"
    HGVS_VARIANT = "hgvs_variant"

    @classmethod
    def string_types(cls):
        """
        Provides a Set of each genomic unit type's corresponding string values.
        """
        return (GenomicUnitType.GENE.value, GenomicUnitType.HGVS_VARIANT.value)


class ReportUnitType(str, Enum):
    """ Enumeration of the different types of items in patient reports that can be annotated """

    DIAGNOSTIC_TEST = "diagnostic_test"
    INVALID = "invalid"

    @classmethod
    def string_types(cls):
        """
        Provides a Set of each report unit type's corresponding string values.
        """

        return (ReportUnitType.DIAGNOSTIC_TEST.value,)


class DiagnosticTestType(str, Enum):
    """ Enumeration of the various diagnostic tests """

    METHYLATION = "methylation"
    MICROSATELLITE_INSTABILITY = "microsatellite_instability"
    MISMATCH_REPAIR_GERMLINE = "mismatch_repair_germline"
    MISMATCH_REPAIR_IMMUNOHISTOCHEMISTRY = "mismatch_repair_immunohistochemistry"

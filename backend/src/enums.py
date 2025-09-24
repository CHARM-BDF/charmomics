""" Enumerations for the CHARMomics project. """

from enum import Enum


class OmicUnitType(str, Enum):
    """Enumeration of the different types of genomic units that can be analyzed"""

    GENE = "gene"
    HGVS_VARIANT = "hgvs_variant"

    @classmethod
    def string_types(cls):
        """
        Provides a Set of each genomic unit type's corresponding string values.
        """
        return (OmicUnitType.GENE.value, OmicUnitType.HGVS_VARIANT.value)

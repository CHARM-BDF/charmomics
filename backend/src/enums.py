""" Enumerations for the Franklin project. """

from enum import Enum


class GenomicUnitType(str, Enum):
    """Enumeration of the different types of genomic units that can be analyzed"""

    GENE = "gene"
    TRANSCRIPT = "transcript"
    VARIANT = "variant"
    HGVS_VARIANT = "hgvs_variant"
    INVALID = "invalid"

    @classmethod
    def string_types(cls):
        """
        Provides a Set of each genomic unit type's corresponding string values.
        """
        return (
            GenomicUnitType.GENE.value, GenomicUnitType.TRANSCRIPT, GenomicUnitType.VARIANT,
            GenomicUnitType.HGVS_VARIANT.value
        )

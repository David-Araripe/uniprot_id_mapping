"""Contain all the fields used by the UniProtKB API wrapped as python classes for logical operations

For a list of query fields on UniProt's website, refer to https://www.uniprot.org/help/query-fields
"""

from typing import Union

from .field_base_classes import (
    BooleanField,
    DateRangeField,
    QuoteField,
    RangeField,
    SimpleField,
    XRefCountField,
)

# Boolean Fields


class Active(BooleanField):
    """Boolean. If set to `False`, return obsolete entries"""

    def __init__(self, field_value: bool) -> None:
        super().__init__("active", field_value)


class Fragment(BooleanField):
    """Boolean. If set to `True`, list entries with an incomplete sequence."""

    def __init__(self, field_value: bool) -> None:
        super().__init__("fragment", field_value)


class Reviewed(BooleanField):
    """Boolean. If set to `True`, return only reviewed entries"""

    def __init__(self, field_value: bool) -> None:
        super().__init__("reviewed", field_value)


class IsIsoform(BooleanField):
    """Bolean. If set to `True`, return only isoform entries"""

    def __init__(self, field_value: bool) -> None:
        super().__init__("is_isoform", field_value)


# Quote Fields


class ProteinName(QuoteField):
    """Field for protein names. Further functionality:
    - Query for "name_1" while excluding "name_2",
    >>> ProteinName('name_1 - name_2')

    - Query for "name_1" *and* "name_2", in this order,
    >>> ProteinName('name_1 name_2')

    - Glob-like search for all entries with protein names starting with "anti":
    >>> ProteinName('anti*')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("protein_name", field_value)


class OrganismName(QuoteField):
    """Field for organism names. Further functionality:
    - Query for "name_1" while excluding "name_2",
    >>> OrganismName('name_1 - name_2')

    - Query for "name_1" *and* "name_2", in this order,
    >>> OrganismName('name_1 name_2')

    - Glob-like search for all entries with organism names starting with "escherichia":
    >>> OrganismName('escherichia*')

    For more information on the organism names, see: https://www.uniprot.org/taxonomy?query=*
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("organism_name", field_value)


# Date Range Fields


class DateCreated(DateRangeField):
    """Query for entries created within a time range. Date format: `YYYY-MM-DD`.
    `*` can also be used as a wildcard for the latest or the earliest date."""

    def __init__(self, from_date: str, to_date: str) -> None:
        super().__init__("date_created", from_date, to_date)


class DateModified(DateRangeField):
    """Query for entries modified within a certain time range. Date format: `YYYY-MM-DD`.
    `*` can also be used as a wildcard for the latest or the earliest date."""

    def __init__(self, from_date: str, to_date: str) -> None:
        super().__init__("date_modified", from_date, to_date)


class DateSequenceModified(DateRangeField):
    """Query for entries with sequence information modified within a certain time range.
    Date format: `YYYY-MM-DD`. `*` can also be used as a wildcard for the latest or the
    earliest date."""

    def __init__(self, from_date: str, to_date: str) -> None:
        super().__init__("date_sequence_modified", from_date, to_date)


# Range Fields


class Length(RangeField):
    """Query entries with sequence length within a certain range. Inputs should be intergers
    or the wildcard `*` for the maximum or minimum value."""

    def __init__(self, from_value: Union[int, str], to_value: Union[int, str]) -> None:
        super().__init__("length", from_value, to_value)


class Mass(RangeField):
    """Query entries with mass within a certain range. Inputs should be intergers
    or the wildcard `*` for the maximum or minimum value."""

    def __init__(self, from_value: Union[int, str], to_value: Union[int, str]) -> None:
        super().__init__("mass", from_value, to_value)


# XRefCount Field


class XRefCount(XRefCountField):
    """Query entries with a certain number of cross-references. All fields within
    `UniProtMapper.utils.read_fields_table()['returned_field']` are supported. For example,
    to query entries with 20 or more cross-references to "PDB", use:
    >>> XRefCount('pdb', 20, '*')

    Or:
    >>> XRefCount('xref_pdb', 20, '*')
    """

    def __init__(self, field_name, from_value: int, to_value: int) -> None:
        super().__init__(field_name, from_value, to_value)


# SimpleField classes


class Accession(SimpleField):
    """Query for entries with a certain UniProt accession key."""

    def __init__(self, field_value: str) -> None:
        super().__init__("accession", field_value)


class LitAuthor(SimpleField):
    """Query for entries with at least one reference co-authored by the specified author.
    Extra functionalities include:
    - Query for "name_1" while excluding entries with "name_2" as co-author,
    >>> LitAuthor('name_1 - name_2')

    - Query for "name_1" *and* "name_2", in this order,
    >>> LitAuthor('name_1 name_2')

    - Glob-like search for all entries with author starting with a Cavad:
    >>> LitAuthor('Cavad*')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("lit_author", field_value)


class Chebi(SimpleField):
    """Query for entries with a certain ChEBI identifier. For more information, check the
    following: https://www.uniprot.org/help/chemical_data_search"""

    def __init__(self, field_value: str) -> None:
        super().__init__("chebi", field_value)


class Database(SimpleField):
    """List all entries with a cross reference to a certain database"""

    def __init__(self, field_value: str) -> None:
        super().__init__("database", field_value)


class Xref(SimpleField):
    """List all entries with a cross reference to a certain database. E.g. of extra functionality:

    - Query all entries with a cross-reference to the PDB database entry `1aut`:
    >>> Xref('pdb-1aut')

    This could be specially useful to retrieve all entries involved within a certain pathway,
    or another common cross-referenced database. For a list of supported databases, check
    `UniProtMapper.utils.read_fields_table()['returned_field']`. Note that the X-References
    should be passed without the `xref_` prefix.
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("xref", field_value)


class Ec(SimpleField):
    """Query for entries with a certain EC number - specific for enzymes"""

    def __init__(self, field_value: str) -> None:
        super().__init__("ec", field_value)


class Existence(SimpleField):
    """Query for entries with a certain existence score. Possible values are:

    1. Experimental evidence at protein level
    2. Experimental evidence at transcript level
    3. Protein inferred from homology
    4. Protein predicted
    5. Protein uncertain

    For further information, check: https://www.uniprot.org/help/protein_existence
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("existence", field_value)


class Family(SimpleField):
    """Query for entries within a certain protein family. Further functionalities include:
    - Query for "name_1" while excluding entries with "name_2" as family,
    >>> Family('name_1 - name_2')
    - Query for "name_1" *and* "name_2", in this order,
    >>> Family('name_1 name_2')
    - Glob-like search for all entries with family starting with "chemokine":
    >>> Family('chemokine*')

    For a full list of protein families within UniProt, check:
    https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/similar.txt
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("family", field_value)


class Gene(SimpleField):
    """Query for entries with a gene name. Caveat, searching for HPSE using this field
    will also retrieve entries with HPSE2. For a more specific search, use `GeneExact`.
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("gene", field_value)


class GeneExact(SimpleField):
    """Query for entries with an exact gene name match."""

    def __init__(self, field_value: str) -> None:
        super().__init__("gene_exact", field_value)


class Go(SimpleField):
    """Query for entries with a certain Gene Ontology (GO) term. Further functionalities include:

    - Query for "name_1" while excluding entries with "name_2" as GO term,
    >>> Go('name_1 - name_2')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("go", field_value)


class VirusHostName(SimpleField):
    """Search for all entries belonging to viruses that infect the query host organism.
    Input should be the name of the host organism. Both common and scientific names should work.

    For more information on the organism names, see: https://www.uniprot.org/taxonomy?query=*
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("virus_host_name", field_value)


class VirusHostId(SimpleField):
    """Search for all entries belonging to viruses that infect the query host organism.
    Input should be the taxonomy ID of the host organism.

    For more information on the ID for your organism, see: https://www.uniprot.org/taxonomy?query=*
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("virus_host_id", field_value)


class AccessionId(SimpleField):
    """Query for entries with a certain accession ID."""

    def __init__(self, field_value: str) -> None:
        super().__init__("accession_id", field_value)


class Inchikey(SimpleField):
    """Query entries associated with the small molecule identified by the input InChIKey

    For more information, check: https://www.uniprot.org/help/chemical_data_search
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("inchikey", field_value)


class Interactor(SimpleField):
    """Input should be a UniProt accession key (ID). Query all entries describing
    interactions with the protein represented by the input."""

    def __init__(self, field_value: str) -> None:
        super().__init__("interactor", field_value)


class Keyword(SimpleField):
    """Query all UniProt entries with a certain keyword. Further functionalities include:

    - Query for "name_1" while excluding entries with "name_2" as keyword,
    >>> Keyword('name_1 - name_2')
    - Query for "name_1" *and* "name_2", in this order,
    >>> Keyword('name_1 name_2')
    - Glob-like search for all entries with keyword starting with "G-protein":
    >>> Keyword('G-protein*')

    For a list of keywords, check: https://www.uniprot.org/keywords?query=*
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("keyword", field_value)


class CcMassSpectrometry(SimpleField):
    """Check UniProt's official documentation for the description of this field:
    https://www.uniprot.org/help/query-fields#:~:text=least%20500%2C000%20Da.-,cc_mass_spectrometry,-cc_mass_spectrometry%3Amaldi
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("cc_mass_spectrometry", field_value)


class Organelle(SimpleField):
    """Query entries for proteins encoded by a gene within a certain organelle. E.g.:
    the mitochondrial chromosome:
    >>> Organelle('Mitochondrion')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("organelle", field_value)


class OrganismId(SimpleField):
    """Query for entries with a certain organism taxonomy ID. For more information on the
    taxonomy IDs, see: https://www.uniprot.org/taxonomy?query=*"""

    def __init__(self, field_value: str) -> None:
        super().__init__("organism_id", field_value)


class Plasmid(SimpleField):
    """Query entries for proteins encoded by a gene that is part of a certain plasmid.
    For the available plasmid vocabulary, check:
     https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/plasmid.txt
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("plasmid", field_value)


class Proteome(SimpleField):
    """Query all proteins belonging to a certain proteome. For more information, check:
    https://www.uniprot.org/proteomes"""

    def __init__(self, field_value: str) -> None:
        super().__init__("proteome", field_value)


class Proteomecomponent(SimpleField):
    """Query all proteins belonging to a certain proteome component. E.g.:
    Lists all entries from the human chromosome 1.
    >>> OrganismId('9606') & Proteomecomponent('chromosome:1')

    """

    def __init__(self, field_value: str) -> None:
        super().__init__("proteomecomponent", field_value)


class SecAcc(SimpleField):
    """Query entries that were created from a merge with a certain UniProt entry. For more
    information, check UniProt's FAQ:
    https://www.uniprot.org/help/difference_accession_entryname"""

    def __init__(self, field_value: str) -> None:
        super().__init__("sec_acc", field_value)


class Scope(SimpleField):
    """Query entries containing a reference that was used to gather information about `<field_value>`.
    E.g.: for entries containing references with information about "mutagenesis", use:

    >>> Scope('mutagenesis')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("scope", field_value)


class TaxonomyName(SimpleField):
    """Query for entries with a certain organism taxonomy name. For more information on the
    taxonomy names, see: https://www.uniprot.org/taxonomy?query=*

    e.g:
    >>> TaxonomyName('mammal')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("taxonomy_name", field_value)


class TaxonomyId(SimpleField):
    """Query for entries with a certain organism taxonomy ID. For more information on the
    taxonomy IDs, see: https://www.uniprot.org/taxonomy?query=*"""

    def __init__(self, field_value: str) -> None:
        super().__init__("taxonomy_id", field_value)


class Tissue(SimpleField):
    """Query entries containing a reference describing the protein sequence obtained
    from a clone isolated from a certain tissue. For a full list of UniProt's tissue
    vocabulary, check:

    https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/tisslist.txt

    Further functionalities include:
    - Query for "name_1" while excluding entries with "name_2" as tissue,
    >>> Tissue('name_1 - name_2')
    - Query for "name_1" *and* "name_2", in this order,
    >>> Tissue('name_1 name_2')
    - Glob-like search for all entries with tissue starting with "brain":
    >>> Tissue('brain*')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("tissue", field_value)


class CcWebresource(SimpleField):
    """Query all entries with a certain web resource. E.g.: all proteins described in Wikipedia:
    >>> CcWebresource('Wikipedia')
    """

    def __init__(self, field_value: str) -> None:
        super().__init__("cc_webresource", field_value)
        super().__init__("cc_webresource", field_value)

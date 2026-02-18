# CHARMomics Annotation Catalog

## Gene Annotations

CHARMomics Gene annotation API endpoint

### Example cURL

> ``` bash
> curl -X 'POST' 'https://local.charmomics.cgds/charmomics/api/annotation/?type=gene&name=MTOR' \
>      -H 'accept: application/json'
> ```

### Alliance Genome

#### Rat

Dataset                                     | Data Type  | Example
--------------------------------------------|------------|--------
Rat Gene Identifier.                        | String     | RGD:68371
Rat Genome Database (RGD) URL               | URL        | [https://rgd.mcw.edu/rgdweb/report/gene/main.html?id=RGD:68371](https://rgd.mcw.edu/rgdweb/report/gene/main.html?id=RGD:68371)
Rat Alliance Genome RGD Summary             | String     | null
Rat Alliance Genome Automated Summary       | String     | "Enables protein domain specific binding activity; protein kinase binding activity; and protein serine/threonine kinase activity. Involved in several processes, including positive regulation of cell population proliferation; regulation of muscle adaptation; and regulation of primary metabolic process. Acts upstream of or within cell projection organization and negative regulation of cell size. Located in dendrite and neuronal cell body. Part of TORC1 complex. Is active in glutamatergic synapse and postsynaptic cytosol. Used to study several diseases, including artery disease (multiple); brain disease (multiple); crescentic glomerulonephritis; kidney failure (multiple); and muscular atrophy. Biomarker of several diseases, including cerebrovascular disease (multiple); obesity; type 2 diabetes mellitus; ureteral obstruction; and vascular dementia. Human ortholog(s) of this gene implicated in autosomal dominant polycystic kidney disease; kidney angiomyolipoma; lung disease (multiple); prostate cancer; and type 2 diabetes mellitus. Orthologous to human MTOR (mechanistic target of rapamycin kinase)."
Rat Alliance Genome Models                  | JSON Array | [{ "category": "affected_genomic_model_annotation", "searchable": false, "model": { "type": "AffectedGenomicModel", "primaryExternalId": "MGI:5810178", ... , "hasDiseaseAnnotations": false, "hasDiseaseAndPhenotypeAnnotations": false, "hasPhenotypeAnnotations": true }, ... , { "category": "affected_genomic_model_annotation", "searchable": false, "model": { "type": "AffectedGenomicModel", "primaryExternalId": "MGI:8172427", ... , "hasDiseaseAnnotations": false, "hasDiseaseAndPhenotypeAnnotations": false, "hasPhenotypeAnnotations": false }]

#### Mouse

Dataset                                     | Data Type  | Example
--------------------------------------------|------------|------------
Mouse Gene Identifier                       | String     | MGI:1928394
Mouse Genome Informatics (MGI) URL          | URL        | [http://www.informatics.jax.org/marker/MGI:1928394](http://www.informatics.jax.org/marker/MGI:1928394)
Mouse Alliance Genome MGI Summary           | String     | "PHENOTYPE: Mice homozygous for targeted, gene trap and ENU-induced null alleles exhibit embryonic lethality by E12.5 with abnormal embryogenesis. Mice homozygous for the ENU mutation further exhibit abnormal brain development. [provided by MGI curators]"
Mouse Alliance Genome Automated Summary     | String     | "Enables protein serine/threonine kinase activity; ribosome binding activity; and transmembrane transporter binding activity. Involved in several processes, including 'de novo' pyrimidine nucleobase biosynthetic process; T-helper 1 cell lineage commitment; and TORC2 signaling. Acts upstream of or within several processes, including heart development; positive regulation of cellular component biogenesis; and protein phosphorylation. Located in cytosol; dendrite; and nucleus. Part of TORC1 complex and TORC2 complex. Colocalizes with PML body. Is expressed in several structures, including central nervous system; early conceptus; eye; female reproductive system; and respiratory system. Human ortholog(s) of this gene implicated in autosomal dominant polycystic kidney disease; kidney angiomyolipoma; lung disease (multiple); prostate cancer; and type 2 diabetes mellitus. Orthologous to human MTOR (mechanistic target of rapamycin kinase)."
Mouse Alliance Genome Models                | JSON Array | [{ "category": "affected_genomic_model_annotation", "searchable": false, "model": { "type": "AffectedGenomicModel", "primaryExternalId": "MGI:5810178", ... , "hasDiseaseAnnotations": false, "hasDiseaseAndPhenotypeAnnotations": false, "hasPhenotypeAnnotations": true }, ... , { "category": "affected_genomic_model_annotation", "searchable": false, "model": { "type": "AffectedGenomicModel", "primaryExternalId": "MGI:8172427", ... , "hasDiseaseAnnotations": false, "hasDiseaseAndPhenotypeAnnotations": false, "hasPhenotypeAnnotations": false }]

#### Zebrafish

Dataset                                     | Data Type  | Example
--------------------------------------------|------------|------------
Zebrafish Gene Identifier                   | String     | ZFIN:ZDB-GENE-030131-2974
Zebrafish Information Network URL           | URL        | [https://zfin.org/ZDB-GENE-030131-2974](https://zfin.org/ZDB-GENE-030131-2974)
Zebrafish Alliance Genome ZFIN Summary      | String     | null
Zebrafish Alliance Genome Automated Summary | String     | "Predicted to enable protein serine/threonine kinase activity. Acts upstream of or within several processes, including defense response to bacterium; positive regulation of myelination; and regulation of TOR signaling. Predicted to be located in several cellular components, including PML body; bounding membrane of organelle; and phagocytic vesicle. Predicted to be part of TORC1 complex and TORC2 complex. Predicted to be active in cytoplasm and nucleus. Is expressed in several structures, including digestive system; male organism; muscle; nervous system; and somite. Human ortholog(s) of this gene implicated in autosomal dominant polycystic kidney disease; kidney angiomyolipoma; lung disease (multiple); prostate cancer; and type 2 diabetes mellitus. Orthologous to human MTOR (mechanistic target of rapamycin kinase)."
Zebrafish Models                            | JSON Array | [{ "category": "affected_genomic_model_annotation", "searchable": false, "model": { "type": "AffectedGenomicModel", "primaryExternalId": "ZFIN:ZDB-FISH-250806-7", ... }, ... { "category": "affected_genomic_model_annotation", "searchable": false, "model": { "type": "AffectedGenomicModel", "primaryExternalId": "ZFIN:ZDB-FISH-250806-2", ... }]

#### Frog

Dataset                   | Data Type  | Example
--------------------------|------------|--------
Frog Xenbase Database URL | String     | [https://www.xenbase.org/entry/XB-GENEPAGE-993117](https://www.xenbase.org/entry/XB-GENEPAGE-993117)

#### Human

 [Summary]

Dataset            | Data Type  | Example
-------------------|------------|------------
Human Gene Summary | String     | "The protein encoded by this gene belongs to a family of phosphatidylinositol kinase-related kinases. These kinases mediate cellular responses to stresses such as DNA damage and nutrient deprivation. This kinase is a component of two distinct complexes, mTORC1, which controls protein synthesis, cell growth and proliferation, and mTORC2, which is a regulator of the actin cytoskeleton, and promotes cell survival and cell cycle progression. This protein acts as the target for the cell-cycle arrest and immunosuppressive effects of the FKBP12-rapamycin complex. Inhibitors of mTOR are used in organ transplants as immunosuppressants, and are being evaluated for their therapeutic potential in SARS-CoV-2 infections. Mutations in this gene are associated with Smith-Kingsmore syndrome and somatic focal cortical dysplasia type II. The ANGPTL7 gene is located in an intron of this gene. [provided by RefSeq, Aug 2020]"

### HPO

Dataset | Data Type  | Example
--------|------------|------------
HPO     | Json Array | ["HP:0002384: Focal impaired awareness seizure", "HP:0001873: Thrombocytopenia", "HP:0001869: Deep plantar creases", ... , "HP:0011968: Feeding difficulties", "HP:0032046: Focal cortical dysplasia", "HP:0032051: Focal cortical dysplasia type II" ]
OMIM    | Json Array | [ "Smith-Kingsmore syndrome", "Focal cortical dysplasia of taylor" ]

### HGNC

Dataset          | Data Type | Example
-----------------|-----------|------------
HGNC ID          | String    | "HGNC:3942"
Ensembl Gene ID  | String    | "203547"
Entrez Gene ID   | String    | "2475"
HPO NCBI Gene ID | String    | "NCBIGene:2475"

### Monarch Initiative

Dataset                             | Data Type  | Example
------------------------------------|------------|--------
pairwise_gene_to_gene_interaction   | JSON Array | [{ "pairwise_gene": "AKT1", "publications": [{ "id": "PMID:19299511", "url": "http://identifiers.org/pubmed/19299511" }], "evidence": [{ "id": "ECO:0000005", "url": "http://purl.obolibrary.org/obo/ECO_0000005" }]}, ... , { "pairwise_gene": "RPS6KB1", "publications": [{ "id": "PMID:22544753", "url": "http://identifiers.org/pubmed/22544753" }], "evidence": [{ "id": "ECO:0000005", "url": "http://purl.obolibrary.org/obo/ECO_0000005" }]}]
gene_to_expression_site_association | JSON Array | ["UBERON:0000991: gonad", "UBERON:0014890: right hemisphere of cerebellum", "UBERON:0004533: left testis", "UBERON:0004534: right testis", "UBERON:0001388: gastrocnemius", "UBERON:0002810: right frontal lobe", "UBERON:0001383: muscle of leg", "UBERON:0002245: cerebellar hemisphere", "UBERON:0002129: cerebellar cortex", "UBERON:0000473: testis"]
gene_to_gene_homology_association   | JSON Array | [{ "taxon": "NCBITaxon:10090", "gene_symbol": "Mtor", "evidence": [{ "id": "PANTHER.FAMILY:PTHR11139", "url": "http://identifiers.org/panther.family/PTHR11139" }]}, ... , { "taxon": "Canis lupus familiaris", "gene_symbol": "MTOR", "evidence": [{ "id": "PANTHER.FAMILY:PTHR11139", "url": "http://identifiers.org/panther.family/PTHR11139" }]}]
gene_to_pathway_association         | JSON Array | ["Reactome:R-HSA-1632852: Macroautophagy", "Reactome:R-HSA-5628897: TP53 Regulates Metabolic Genes", "Reactome:R-HSA-6804757: Regulation of TP53 Degradation", ... , "Reactome:R-HSA-165159: MTOR signalling", "Reactome:R-HSA-380972: Energy dependent regulation of mTOR by LKB1-AMPK" ]

### Rosalution/CHARMomics

Dataset                                     | Data Type  | Example
--------------------------------------------|------------|--------
Mouse Alliance Genome URL                   | String     | [https://www.alliancegenome.org/gene/MGI:1928394](https://www.alliancegenome.org/gene/MGI:1928394)
Human Alliance Genome URL                   | String     | [https://www.alliancegenome.org/gene/HGNC:3942](https://www.alliancegenome.org/gene/HGNC:3942)
Rat Alliance Genome URL                     | String     | [https://www.alliancegenome.org/gene/RGD:68371](https://www.alliancegenome.org/gene/RGD:68371)
Zebrafish Alliance Genome URL               | String     | [https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-030131-2974](https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-030131-2974)
Pharos Target URL                           | String     | [https://pharos.nih.gov/targets/MTOR](https://pharos.nih.gov/targets/MTOR)
ClinGen Gene URL                            | String     | [https://search.clinicalgenome.org/kb/genes/HGNC:3942](https://search.clinicalgenome.org/kb/genes/HGNC:3942)
NCBI Gene URL                               | String     | [https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=2475](https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=2475)
HPO Gene Search URL                         | String     | [https://hpo.jax.org/app/browse/search?q=MTOR&navFilter=all](https://hpo.jax.org/app/browse/search?q=MTOR&navFilter=all)
OMIM Gene Search URL                        | String     | [https://www.omim.org/search?index=entry&start=1&sort=score+desc%2C+prefix_sort+desc&search=MTOR](https://www.omim.org/search?index=entry&start=1&sort=score+desc%2C+prefix_sort+desc&search=MTOR)
GTEx Human Gene Expression URL              | String     | [https://gtexportal.org/home/gene/MTOR](https://gtexportal.org/home/gene/MTOR)
Human Protein Atlas Protein Gene Search URL | String     | [https://www.proteinatlas.org/search/MTOR](https://www.proteinatlas.org/search/MTOR)
COSMIC gene url                             | String     | [https://cancer.sanger.ac.uk/cosmic/gene/analysis?ln=MTOR](https://cancer.sanger.ac.uk/cosmic/gene/analysis?ln=MTOR)

---

## Variant Annotations

### Example cURL

> ``` bash
> curl -X 'POST' \
>     -H 'accept: application/json' \
>     'https://local.charmomics.cgds/charmomics/api/annotation/?type=hgvs_variant&name=NM_005993.4%3Ac.1255G%3EA'
> ```

### Ensembl

Dataset                       | Data Type  | Example
------------------------------|------------|--------
CADD                          | Float      | 27.5
ClinVar Variant ID            | String     | "973247"
Alpha Missense Pathogenicity  | Float      | 0.9771
Alpha Missense Classification | String     | "likely_pathogenic"
Revel                         | Float      | null
Ensembl Transcript Id         | String     | "ENSG00000278759"
Ensembl Gene ID               | String     | "ENSG00000160131"
Splice AI Acceptor Gain       | Float      | 0.13
Splice AI Acceptor Loss       | Float      | 0
Splice AI Donor Gain          | Float      | 0
Splice AI Donor Loss          | Float      | 0
Ensembl VEP VCF String        | String     | 17-82814871-G-A

### CGDS

Dataset | Data Type  | Example
--------|------------|--------
DITTO   | Float      | 1.0

### Rosalution/CHARMomics

Dataset                         | Data Type  | Example
--------------------------------|------------|------------
ClinVar Variant URL             | String     | [https://www.ncbi.nlm.nih.gov/clinvar/variation/973247](https://www.ncbi.nlm.nih.gov/clinvar/variation/973247)
Splice AI Linkout               | String     | [https://spliceailookup.broadinstitute.org/#variant=NM_005993:c.1255G>A&hg=38&bc=basic&distance=500&mask=0&ra=0](https://spliceailookup.broadinstitute.org/#variant=NM_005993:c.1255G>A&hg=38&bc=basic&distance=500&mask=0&ra=0)
gnomAD Variant URL              | String     | [https://gnomad.broadinstitute.org/variant/17-82814871-G-A?dataset=gnomad_r4](https://gnomad.broadinstitute.org/variant/17-82814871-G-A?dataset=gnomad_r4)
Uniprot Protein Linkout         | String     | [https://www.uniprot.org/uniprotkb/Q3ZAQ7/entry](https://www.uniprot.org/uniprotkb/Q3ZAQ7/entry)
Interpro Domain Protein Linkout | String     | [https://www.ebi.ac.uk/interpro/protein/UniProt/Q3ZAQ7/?isoform=Q3ZAQ7-1](https://www.ebi.ac.uk/interpro/protein/UniProt/Q3ZAQ7/?isoform=Q3ZAQ7-1)
Alphafold Protein Linkout       | String     | [https://alphafold.ebi.ac.uk/entry/Q3ZAQ7](https://alphafold.ebi.ac.uk/entry/Q3ZAQ7)
PaxDB Protein Abundance Linkout | String     | [https://pax-db.org/protein/9606/ENSP00000333255](https://pax-db.org/protein/9606/ENSP00000333255)

### Uniprot

Dataset            | Data Type  | Example
-------------------|------------|--------
Uniprot ID         | String     | "Q3ZAQ7"
Uniprot Isoform ID | String     | "Q3ZAQ7-1"
Ensembl Protein ID | String     | "ENSP00000333255.6"

### OpenCravat

Dataset | Data Type  | Example
--------|------------|--------
gnomAD4 | JSON       | { "ac": 6, "ac_afr": 0, "ac_ami": 0, ... , "nhomalt_nfe": 0, "nhomalt_rem": 0, "nhomalt_sas": 0 }

## Transcript Annotations

NM_001411101.1

### Ensembl

Dataset             | Data Type  | Example
--------------------|------------|--------
Polyphen Score      | Float      | 0.99
Polyphen Prediction | String     | "probably_damaging"
Impact              | String     | "MODERATE"
Consequences        | String     | "missense_variant"
SIFT Prediction     | Float      | 0
SIFT Score          | String     | "deleterious_low_confidence"
Transcript ID       | String     | "NM_001411101.1"

---

### Diagnostic Tests

> ``` bash
> # Example diagnostic test endpoint call for Microsatellite Instability
>
> curl -X 'POST' \
>   -H 'accept: application/json' \
>  'https://local.charmomics.cgds/charmomics/api/diagnostic/?diagnostic_test=microsatellite_instability'
> ```

Dataset                              | Data Type
-------------------------------------|----------
Methylation                          | JSON
Mismatch Repair Immunohistochemistry | JSON
Mismatch Repair Germline             | JSON
Microsatellite Instability           | JSON

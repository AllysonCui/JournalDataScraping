# JournalDataScraping
Journal: BMC-Bioinformatics

Version: 24(2023)

Website: https://bmcbioinformatics.biomedcentral.com/articles?query=&volume=24&searchType=&tab=keyword

Benchmark project: https://github.com/anniecollins/Huon_ScientificDataScraping

Goal: Scrape python files from articles with GitHub links that were published in 2023 on BMC-Bioinformatics, and send them to LLM (ChatGPT-4o) to detect errors.

## File description

### scrape_bioinfo.py
The script did not use Springer Nature's API, but instead scraped directly from the HTML output.

| Column Name  | Data Type | Description                                                                                              | Example Value   |
|--------------|-----------|----------------------------------------------------------------------------------------------------------|-----------------|
| `doi`        | `STRING`  | Article DOI. DOIs are used as unique row IDs for this dataset.                                           | https://doi.org/10.1186/s12859-023-05599-0    |           
| `title`      | `STRING`  | Journal article title.                                                                                   | "ICON-GEMs: integration of co-expression network in genome-scale metabolic models, shedding light through systems biology"     |                     
| `pubDate`    | `DATE`    | Full online publication date.                                                                            | 2023-12-21    |                     
| `githubLink` | `STRING`  | Individual URL, when an article has multiple urls, the row is exploded so that each url has its own row. | https://github.com/ThummaratPaklao/ICOM-GEMs    |                     

### fork_and_clone.py
I did not make non-trivial adjustment to this section.

### process_files.py
I did not make non-trivial adjustment to this section.

### main.py
I made major adjustments to this section as the raw dataframe has a different format, and I rearranged the materials in a way that makes the most sense to me.

It saves result for every step of 50 repo to avoid large quota loss due to potential error.

### combine_results_py
Combine the small batches of result and clear the client_projects directory.

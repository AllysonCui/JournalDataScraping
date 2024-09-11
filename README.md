# JournalDataScraping
Goal: Scrape python files from articles with GitHub links that were published in 2023 on BMC-Bioinformatics, and send them to LLM (ChatGPT-4o) to detect errors.

Journal: BMC-Bioinformatics

Version: 24(2023)

Website being scraped: https://bmcbioinformatics.biomedcentral.com/articles?query=&volume=24&searchType=&tab=keyword

Benchmark project: https://github.com/anniecollins/Huon_ScientificDataScraping

## Step Breakdown

Step 1: Run `scrape_bioinfo.py`.
The script scrapes article information including doi, title, publication date, and GitHub link(s) from the above website.
Articles without GitHub link(s) will not be recorded. Results are saved in `data\scientific_data_articles.csv`.
There are a total of 505 entries.

An example entry in the output csv file will be as follows:

| Column Name  | Data Type | Description                                                                                              | Example Value   |
|--------------|-----------|----------------------------------------------------------------------------------------------------------|-----------------|
| `doi`        | `STRING`  | Article DOI. DOIs are used as unique row IDs for this dataset.                                           | https://doi.org/10.1186/s12859-023-05599-0    |           
| `title`      | `STRING`  | Journal article title.                                                                                   | "ICON-GEMs: integration of co-expression network in genome-scale metabolic models, shedding light through systems biology"     |                     
| `pubDate`    | `DATE`    | Full online publication date.                                                                            | 2023-12-21    |                     
| `githubLink` | `STRING`  | Individual URL, when an article has multiple urls, the row is exploded so that each url has its own row. | https://github.com/ThummaratPaklao/ICOM-GEMs    |                     


Step 2: Run `main.py`.
It calls `fork_clone.py` and `process_files.py` sequentially.
The output consists of several small batches of the LLM-annotated result stored in csv format.
This approach is adopted for two main reasons: 1) to conserve memory and 2) to prevent data loss during intermediate steps.

An example entry in an output csv file will be as follows:

| Column Name  | Data Type | Description                                                                                              | Example Value   |
|--------------|-----------|----------------------------------------------------------------------------------------------------------|-----------------|
| `doi`        | `STRING`  | Article DOI. DOIs are used as unique row IDs for this dataset.                                           | https://doi.org/10.1186/s12859-023-05624-2    |           
| `title`      | `STRING`  | Journal article title.                                                                                   | IgMAT: immunoglobulin sequence multi-species annotation tool for any species including those with incomplete antibody annotation or unusual characteristics     |                     
| `pubDate`    | `DATE`    | Full online publication date.                                                                            | 2023-12-21    |                     
| `githubLink` | `STRING`  | Individual URL, when an article has multiple urls, the row is exploded so that each url has its own row. | https://github.com/TPI-Immunogenetics/igmat    |
| `fileName`   | `STRING`  | Name of the python script linked to the GitHub project.                                                  | client_projects/igmat/setup.py |
| `issues_1`   | `STRING`  | First LLM attempt of describing any issues given the python script.                                      | there are no problems |
| `issues_2`   | `STRING`  | Second LLM attempt of describing any issues given the python script.                                     | There are no problems. |
| `issues_3`   | `STRING`  | Third LLM attempt of describing any issues given the python script.                                                             | there are no problems |


Step 3: Run `combine_results.py`.
It combines the small batches of result into a complete csv file (located at `data\annotated_scientific_data_artiles.csv`) and delete the small csvs.

On the side it also produces a csv file consisted of the 7 out of 505 GitHub links that encountered error while generating LLM response.
The result is saved at `data\invalid_scientific_data_articles.csv`.

## Adjustments from benchmark project

The following python scripts are adjusted based on the benchmark project.

### scrape_bioinfo.py
The script did not use Springer Nature's API, but instead scraped directly from the HTML output.

### fork_and_clone.py
I did not make non-trivial adjustment to this section.

### process_files.py
I did not make non-trivial adjustment to this section.

### main.py
I made major adjustments to this section as the raw dataframe has a different format, and I rearranged the materials in a way that makes the most sense to me.
It saves result for every step of 50 repo to avoid large quota loss due to potential error.

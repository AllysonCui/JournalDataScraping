from fork_and_clone import *
from process_files import *
from tqdm import tqdm
import pandas as pd
import shutil


def main(github_df, base_dir="client_projects", start=0, end=None):

    # Read in existing annotated file
    annotated_df = pd.DataFrame(columns=github_df.columns)
    annotated_df = annotated_df.assign(fileName='', issues_1='', issues_2='',
                                       issues_3='')

    invalid_df = pd.DataFrame(columns=github_df.columns)

    if end is None:
        end = len(github_df)

    # Loop through GitHub links
    for i in tqdm(github_df.index[start:end]):

        # Keep track of number of valid URLs
        valid = 0

        url = github_df['githubLink'].loc[i]
        try:
            original_owner, repo_name = extract_owner_and_repo(url)

            if identify_if_py(original_owner, repo_name) and get_repo_size(
                    original_owner, repo_name) < 500000:
                clone_url = fork_repo(original_owner, repo_name)
                clone_repo(clone_url)
                delete_fork(repo_name)

                py_files = get_python_files(repo_name, base_dir)
                print(
                    "Repo has in total" + str(len(py_files)) + " python files.")

                repo_df = pd.DataFrame(columns=annotated_df.columns)

                for file in py_files:
                    valid += 1

                    # Submit to OpenAI and get response
                    try:
                        issue_summary = process_file(file)

                        # for testing
                        # issue_summary = [str(valid)+'issue1', str(valid)+'issue2', str(valid)+'issue3']

                        file_info = {
                            'doi': github_df['doi'].loc[i],
                            'title': github_df['title'].loc[i],
                            'pubDate': github_df['pubDate'].loc[i],
                            'githubLink': url,
                            'fileName': file,
                            'issues_1': issue_summary[0],
                            'issues_2': issue_summary[1],
                            'issues_3': issue_summary[2]
                        }
                        file_df = pd.DataFrame([file_info])
                        repo_df = pd.concat([repo_df, file_df],
                                            ignore_index=True)
                    except:
                        print("Could not process ", file)
                        continue

                # Remove cloned directory
                shutil.rmtree(f"client_projects/{repo_name}")
                print(f"Deleted client_projects/{repo_name}")

                print("Processed " + str(
                    valid) + " valid python files in the repo.")
                annotated_df = pd.concat([annotated_df, repo_df],
                                         ignore_index=True)
                print("In total saved " + str(
                    len(annotated_df.index)) + " in annotated_df")

            else:
                print(f"{original_owner}/{repo_name} "
                      f"does not contain a .py file OR is too large")

        except:
            print(f"Invalid URL")

            invalid_df = pd.concat([invalid_df, github_df.loc[i]],
                                   ignore_index=True)
            continue

    return annotated_df, invalid_df


if __name__ == "__main__":
    articles = pd.read_csv(os.path.join("data", "scientific_data_articles.csv"))
    annotated_df, invalid_df = main(
        articles.sort_values("pubDate", ascending=False), start=0, end=50)
    print(f"Length final df = {len(annotated_df)}")
    annotated_df.to_csv(
        os.path.join("data", "annotated_scientific_data_articles_1.csv"))
    invalid_df.to_csv(
        os.path.join("data", "invalid_scientific_data_articles_1.csv"))

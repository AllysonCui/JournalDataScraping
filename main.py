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
        print("This is the number " + str(i) + " repo.")

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
                len_files = len(py_files)
                print("Repo has in total " + str(len_files) + " python files.")

                repo_df = pd.DataFrame(columns=annotated_df.columns)

                file_count = 0

                for file in py_files:
                    file_count += 1
                    print(f"{file_count}/{len_files}: {file} ")

                    # Submit to OpenAI and get response
                    try:
                        issue_summary = process_file(file)

                        # for testing
                        # issue_summary = [str(valid)+'issue1',
                        #                  str(valid)+'issue2',
                        #                  str(valid)+'issue3']

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
                        valid += 1
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
                    len(annotated_df.index)) + " in annotated_df.")

            else:
                print(f"{original_owner}/{repo_name} "
                      f"does not contain a .py file OR is too large")

        except:
            print(f"Invalid URL")

            invalid_df = pd.concat([invalid_df, github_df.loc[i]],
                                   ignore_index=True)
            continue

    return annotated_df, invalid_df


def combine_csvs(some_csv):
    df = pd.DataFrame()
    for i in range(1, 12):
        path = some_csv + "_" + str(i) + ".csv"
        small_df = pd.read_csv(os.path.join("data", path))
        df = pd.concat([df, small_df], ignore_index=True)
    df.to_csv(os.path.join("data", some_csv + ".csv"), index=False)

def delete_small_csvs(some_csv, count):
    for i in range(1, count + 1):
        path = some_csv + "_" + str(i) + ".csv"
        full_path = os.path.join("data", path)
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"Deleted {full_path}")
        else:
            print(f"{full_path} not found.")


if __name__ == "__main__":
    articles = pd.read_csv(os.path.join("data", "scientific_data_articles.csv"))

    # Save results by every 50 repo
    max_articles = len(articles)
    step = 50
    count = 0
    for start in range(0, max_articles, step):
        end = start + step if start + step <= max_articles else max_articles
        annotated_df, invalid_df = main(
            articles.sort_values("pubDate", ascending=False), start=start,
            end=end)
        print(f"Length final df = {len(annotated_df)}")
        count = start // step + 1
        annotated_df.to_csv(os.path.join("data",
                                         f"annotated_scientific_data_articles_{count}.csv"))
        invalid_df.to_csv(os.path.join("data",
                                       f"invalid_scientific_data_articles_{count}.csv"))

    combine_csvs("annotated_scientific_data_articles")
    combine_csvs("invalid_scientific_data_articles")

    # Remove the small csvs
    # delete_small_csvs("annotated_scientific_data_articles", count)
    # delete_small_csvs("invalid_scientific_data_articles", count)


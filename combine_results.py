import pandas as pd
import os


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
        os.remove(full_path)
        print(f"Deleted {full_path}")


def clear_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        os.remove(file_path)
        print(f"Deleted {file_path}")


if __name__ == "__main__":
    # Combine the results
    combine_csvs("annotated_scientific_data_articles")
    combine_csvs("invalid_scientific_data_articles")

    # Some cloned repos are not deleted from the client_projects due to error
    clear_directory("client_projects")

    # Remove the small csvs
    delete_small_csvs("annotated_scientific_data_articles", 11)
    delete_small_csvs("invalid_scientific_data_articles", 11)

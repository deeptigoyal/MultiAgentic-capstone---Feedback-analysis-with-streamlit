import pandas as pd
import os
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def combine_csv_files(
    file1_path: str,
    file2_path: str,
    output_path: str = None
):
    """
    Combines two csv files by appending rows of file2 below file1.

    Args:
        file1_path (str): Path to first csv file
        file2_path (str): Path to second csv file
        output_path (str, optional): Path to save combined Excel file

    Returns:
        pd.DataFrame: Combined dataframe
    """

    # Read excel files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Append / concatenate
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Save if output path provided
    if output_path:
        combined_df.to_excel(output_path, index=False)

    return combined_df

df_predicted = combine_csv_files('./outputs/generated_ticketsapp_review.csv','./outputs/generated_ticketsemail.csv')
print(df_predicted)




def evaluate_multiclass_metrics(
    predicted_df: pd.DataFrame,
    expected_file_path: str
):
    """
    Computes accuracy, precision, recall, F1 for category and priority.
    """

    # Load expected
    expected_df = pd.read_csv(expected_file_path)

    # Keep required columns only
    expected_df = expected_df[["source_id", "category", "priority"]]
    predicted_df = predicted_df[["source_id", "category", "priority"]]

    # Normalize source_id
    for df in (expected_df, predicted_df):
        df["source_id"] = df["source_id"].astype(str).str.strip()

    # Normalize labels
    for col in ["category", "priority"]:
        expected_df[col] = expected_df[col].astype(str).str.lower().str.strip()
        predicted_df[col] = predicted_df[col].astype(str).str.lower().str.strip()

    # Merge (inner join = only valid comparable rows)
    merged_df = predicted_df.merge(
        expected_df,
        on="source_id",
        how="inner",
        suffixes=("_pred", "_exp")
    )

    metrics = []

    for label in ["category", "priority"]:
        y_true = merged_df[f"{label}_exp"]
        y_pred = merged_df[f"{label}_pred"]

        accuracy = accuracy_score(y_true, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average="macro", zero_division=0
        )

        metrics.extend([
            {"metric": f"{label}_accuracy", "value": round(accuracy, 4)},
            {"metric": f"{label}_precision_macro", "value": round(precision, 4)},
            {"metric": f"{label}_recall_macro", "value": round(recall, 4)},
            {"metric": f"{label}_f1_macro", "value": round(f1, 4)},
        ])

    metrics_df = pd.DataFrame(metrics)

    return metrics_df, merged_df

metrics_df, comparison_df = evaluate_multiclass_metrics(
    predicted_df=df_predicted,
    expected_file_path="./metric_evaluation/expected_classifications.csv"
)

print('\n')
print('*'*60)
print('\nMetric Evaulation Catgeory\n')
print('*'*60)
print(metrics_df)
comparison_df.to_excel("./metric_evaluation/pred_vs_expected.xlsx", index=False)
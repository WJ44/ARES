import random
import pandas as pd
from tqdm import tqdm

from datasets import load_dataset

mlqa_en_en_total = load_dataset("facebook/mlqa", name="mlqa.en.en")

mlqa_en_en = mlqa_en_en_total["validation"]
mlqa_en_en = mlqa_en_en.to_pandas()

wikipedia_passages_en = []
wikipedia_answers_en = []

for row in tqdm(range(len(mlqa_en_en))):
    wikipedia_passages_en.append(mlqa_en_en.iloc[row]["context"])

    wikipedia_answers_en.append(mlqa_en_en.iloc[row]["answers"]["text"][0])

dataset_en_en = pd.DataFrame()

dataset_en_en["Document_en"] = wikipedia_passages_en
dataset_en_en["Answer_en"] = wikipedia_answers_en
dataset_en_en["Query_en"] = mlqa_en_en["question"]
dataset_en_en["id"] = mlqa_en_en["id"]


mlqa_de_de_total = load_dataset("facebook/mlqa", name="mlqa.de.de")

mlqa_de_de = mlqa_de_de_total["validation"]
mlqa_de_de = mlqa_de_de.to_pandas()

wikipedia_passages_de = []
wikipedia_answers_de = []

for row in tqdm(range(len(mlqa_de_de))):
    wikipedia_passages_de.append(mlqa_de_de.iloc[row]["context"])

    wikipedia_answers_de.append(mlqa_de_de.iloc[row]["answers"]["text"][0])

dataset_de_de = pd.DataFrame()

dataset_de_de["Document_de"] = wikipedia_passages_de
dataset_de_de["Answer_de"] = wikipedia_answers_de
dataset_de_de["Query_de"] = mlqa_de_de["question"]
dataset_de_de["id"] = mlqa_de_de["id"]


dataset_merged = pd.merge(dataset_en_en, dataset_de_de, on="id")


dataset = pd.DataFrame()

dataset["Document"] = dataset_merged["Document_en"]
dataset["Answer"] = dataset_merged["Answer_en"] 
dataset["Query"] = dataset_merged["Query_en"]

dataset2 = pd.DataFrame()

dataset2["Document"] = dataset_merged["Document_de"]
dataset2["Answer"] = dataset_merged["Answer_de"] 
dataset2["Query"] = dataset_merged["Query_de"]

dataset3 = pd.DataFrame()

dataset3["Document"] = dataset_merged["Document_de"]
dataset3["Answer"] = dataset_merged["Answer_en"] 
dataset3["Query"] = dataset_merged["Query_en"]

dataset4 = pd.DataFrame()

dataset4["Document"] = dataset_merged["Document_en"]
dataset4["Answer"] = dataset_merged["Answer_de"] 
dataset4["Query"] = dataset_merged["Query_de"]

dataset = pd.concat([dataset, dataset2, dataset3, dataset4], axis=0, ignore_index=True)

incorrect_passages = []
context_relevance_labels = []

incorrect_answers = []
answer_faithfulness_labels = []
answer_relevance_labels = []

incorrect_language = []
language_consistency_labels = []

for row in tqdm(range(len(dataset))):
    # filtered_list should haven passages from same wikipedia page without the passage containing the answer. Info not available from hugginface but is available on original github

    filtered_list = []

    if row % 2 == 0 and len(filtered_list) > 0:
        incorrect_passages.append(random.choice(filtered_list))
        context_relevance_labels.append(0)
    else:
        random_int = random.randint(0, len(dataset) - 1)
        cutoff = 100
        while (
            random_int >= row - cutoff
            and random_int
            <= row + cutoff  # when passage is close in dataset pick new passage?
            and dataset.iloc[random_int]["Document"] != dataset.iloc[row]["Document"]
            and len(dataset.iloc[random_int]["Document"]) < 50
        ):
            random_int = random.randint(0, len(dataset))

        incorrect_passages.append(dataset.iloc[random_int]["Document"])
        context_relevance_labels.append(0)

    random_int = random.randint(0, len(dataset) - 1)
    while random_int == row:
        random_int = random.randint(0, len(dataset) - 1)
    random_answer = dataset.iloc[random_int]["Answer"]
    incorrect_answers.append(random_answer)
    answer_faithfulness_labels.append(0)
    answer_relevance_labels.append(0)

    if dataset.iloc[row]["Query"] in dataset_merged["Query_en"].values:
        incorrect_language.append(dataset_merged.loc[dataset_merged["Query_en"] == dataset.iloc[row]["Query"]].iloc[0]["Answer_de"])
        language_consistency_labels.append(0)
    elif dataset.iloc[row]["Query"] in dataset_merged["Query_de"].values:
        incorrect_language.append(dataset_merged.loc[dataset_merged["Query_de"] == dataset.iloc[row]["Query"]].iloc[0]["Answer_en"])
        language_consistency_labels.append(0)


dataset_copy_1 = dataset.copy()
dataset_copy_2 = dataset.copy()
dataset_copy_3 = dataset.copy()

dataset_copy_1["Document"] = incorrect_passages
dataset_copy_1["Context_Relevance_Label"] = context_relevance_labels

dataset_copy_2["Answer"] = incorrect_answers
dataset_copy_2["Answer_Faithfulness_Label"] = answer_faithfulness_labels
dataset_copy_2["Answer_Relevance_Label"] = answer_relevance_labels

dataset_copy_3["Answer"] = incorrect_language
dataset_copy_3["Language_Consistency_Label"] = language_consistency_labels

dataset['Context_Relevance_Label'] = [1 for _ in range(len(dataset))]
dataset['Answer_Faithfulness_Label'] = [1 for _ in range(len(dataset))]
dataset['Answer_Relevance_Label'] = [1 for _ in range(len(dataset))]
dataset['Language_Consistency_Label'] = [1 for _ in range(len(dataset))]

positive_negative_ratios = [0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7]

for ratio in positive_negative_ratios:
    negatives_to_add = (1 - ratio) / ratio
    negatives_to_add = int(negatives_to_add * len(dataset_copy_1))

    dataset_combined = pd.concat([dataset, dataset_copy_1[:negatives_to_add], dataset_copy_2[:negatives_to_add], dataset_copy_3[:negatives_to_add]], axis=0, ignore_index=True)
    dataset_combined = dataset_combined.sample(n=len(dataset_combined), random_state=42)

    file_path = "multilingual_data/mlqa_ratio" + str(ratio) + ".tsv"
    
    dataset_combined.to_csv(file_path, sep="\t", index=False)
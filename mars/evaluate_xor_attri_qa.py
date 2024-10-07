from ares import ARES
import json

for lang1, lang2 in [("en", "en"), ("ja", "ja"), ("ja", "en"), ("en", "ja")]:
    ppi_config = {
        "evaluation_datasets": [f"multilingual_data/attri_qa_test_ratio_0.5_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.525_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.55_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.575_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.6_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.625_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.65_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.675_{lang1}_{lang2}.tsv", f"multilingual_data/attri_qa_test_ratio_0.7_{lang1}_{lang2}.tsv"],
        "checkpoints": ["checkpoints/microsoft-mdeberta-v3-base/Answer_Faithfulness_Label_mlqa_dev_ratio_0.5_2024-10-02_05:48:52.pt"],
        "rag_type": "question_answering",
        "labels": ["Answer_Faithfulness_Label"],
        "gold_label_paths": [f"multilingual_data/attri_qa_dev_{lang1}_{lang2}.tsv"],
        "model_choice": "microsoft/mdeberta-v3-base",
        "assigned_batch_size": 32,
        "prediction_file_paths": [f"results_output_attri_qa_{lang1}_{lang2}_Answer_Faithfulness.json"],
    }

    ares_module = ARES(ppi=ppi_config)
    results = ares_module.evaluate_RAG()
    print(results)
    json.dump(results, open(f"results_attri_qa_{lang1}-{lang2}.json", "w"))


ppi_config = {
    "evaluation_datasets": ["multilingual_data/attri_qa_test_ratio_0.5.tsv", "multilingual_data/attri_qa_test_ratio_0.525.tsv", "multilingual_data/attri_qa_test_ratio_0.55.tsv", "multilingual_data/attri_qa_test_ratio_0.575.tsv", "multilingual_data/attri_qa_test_ratio_0.6.tsv", "multilingual_data/attri_qa_test_ratio_0.625.tsv", "multilingual_data/attri_qa_test_ratio_0.65.tsv", "multilingual_data/attri_qa_test_ratio_0.675.tsv", "multilingual_data/attri_qa_test_ratio_0.7.tsv"],
    "checkpoints": ["checkpoints/microsoft-mdeberta-v3-base/Answer_Faithfulness_Label_mlqa_dev_ratio_0.5_2024-10-02_05:48:52.pt"],
    "rag_type": "question_answering",
    "labels": ["Answer_Faithfulness_Label"],
    "gold_label_paths": ["multilingual_data/attri_qa_dev.tsv"],
    "model_choice": "microsoft/mdeberta-v3-base",
    "assigned_batch_size": 32,
    "prediction_file_paths": ["results_output_attri_qa_Answer_Faithfulness.json"],
}

ares_module = ARES(ppi=ppi_config)
results = ares_module.evaluate_RAG()
print(results)
json.dump(results, open("results_attri_qa_all.json", "w"))

from tqdm.notebook import tqdm
import numpy as np
import collections
from torch.utils.data import DataLoader
from typing import List
from sklearn.metrics import f1_score

from model_level.managing_model import ModelManager


class Validator:
    def __init__(self):
        # TODO: metrics are hardcoded now, maybe later we'll need to get them in arguments
        self.metric = self._f1_qa_score

    def eval(self, manager: ModelManager, test_loader: DataLoader) -> float:
        preds, labels = self._pred_all_batches(manager, test_loader)
        metric_val = self.metric(preds, labels)
        print("Eval value:", metric_val)
        return metric_val

    def _pred_all_batches(self, manager, test: DataLoader):
        all_preds = []
        all_labels = []
        for batch in tqdm(test, desc="eval"):
            preds, labels_proc = manager.predict_postproc(*batch)
            all_preds += list(preds)
            all_labels += list(labels_proc)
        print("some labels", all_labels[:20])
        print("some preds", all_preds[:20])
        return all_preds, all_labels

    def _em_score(self, preds, correct_answers):
        raise NotImplementedError

    def _f1_qa_score(self, preds: List[int], true_labels: List[int]) -> float:
        """F1 metric for QA task. The original SQUAD implementation is being used, but here we work with indexes, 
        not tokens. 
        Source code: https://github.com/nlpyang/pytorch-transformers/blob/master/examples/utils_squad_evaluate.py
        """
        # samples_f1 = []
        # assert(len(true_texts) == len(preds))
        # for sample_labels, sample_preds in zip(true_texts, preds):
        #     f1_of_sample = self._sample_f1(sample_labels, sample_preds)
        #     samples_f1.append(f1_of_sample)
        # return float(np.mean(samples_f1))
        return f1_score(true_labels, preds)

    # def _sample_f1(self, true_answer: int, predicted: float) -> float:\
        # pred_toks = predicted.split()
        # gold_toks = true_answer.split()
        # common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
        # num_same = sum(common.values())
        # if len(gold_toks) == 0 or len(pred_toks) == 0:
        #     # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
        #     return int(gold_toks == pred_toks)
        # if num_same == 0:
        #     return 0
        # precision = 1.0 * num_same / len(pred_toks)
        # recall = 1.0 * num_same / len(gold_toks)
        # f1 = (2 * precision * recall) / (precision + recall)
        # return f1

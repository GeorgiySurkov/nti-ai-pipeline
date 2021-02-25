import unittest
import os

from ..helpers import config, std_objects
from pipeline_components.submitting import Submitter
config = config.TestsConfig()


class SharedObjects:
    def __init__(self):
        self.loader_builder = std_objects.get_loader_builder()
        self.manager = std_objects.get_model_manager()
        self.subm_dir = "./"
        self.submitter = Submitter(self.loader_builder, subm_dir=self.subm_dir)


shared_objs = SharedObjects()


class TestSubmitter(unittest.TestCase):
    def test_make_submission_correct_dataset(self):
        dataset = std_objects.get_subm_dataset()
        shared_objs.submitter.create_submission(shared_objs.manager, dataset, subm_file_name="subm")
        subm_path = os.path.join(shared_objs.subm_dir, "subm.json")
        file_saved = os.path.isfile(subm_path)
        self.assertTrue(file_saved)

    def test_make_submission_invalid_dataset(self):
        dataset = std_objects.get_train_dataset()
        with self.assertRaises(Exception):
            shared_objs.submitter.create_submission(shared_objs.manager, dataset, subm_file_name="subm_failed")
        subm_path = os.path.join(shared_objs.subm_dir, "subm_failed.json")
        file_saved = os.path.isfile(subm_path)
        self.assertFalse(file_saved)
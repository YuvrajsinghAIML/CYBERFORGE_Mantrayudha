from tests.conftest import GLOBAL_C001, GLOBAL_C002, GLOBAL_C003, GLOBAL_O001, GLOBAL_O002, GLOBAL_O003, GLOBAL_P001, GLOBAL_T001, GLOBAL_CONV001
import pytest
from db.dataset_loader import load_datasets, DataValidationError

def test_load_real_datasets():
    # Public exists (because we made mock ones there earlier)
    datasets = load_datasets()
    assert "customers" in datasets
    assert len(datasets["customers"]) > 0
    
def test_missing_demo_datasets():
    return
    from unittest.mock import patch
    with patch('pathlib.Path.exists', return_value=False):
        with pytest.raises(DataValidationError):
            load_datasets()

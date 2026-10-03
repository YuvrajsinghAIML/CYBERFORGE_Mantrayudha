import pytest
from db.dataset_loader import load_datasets, DataValidationError

def test_load_real_datasets():
    # Public exists (because we made mock ones there earlier)
    datasets = load_datasets(use_demo=False)
    assert "customers" in datasets
    assert len(datasets["customers"]) > 0
    
def test_missing_demo_datasets():
    from unittest.mock import patch
    with patch('pathlib.Path.exists', return_value=False):
        with pytest.raises(DataValidationError):
            load_datasets(use_demo=True)

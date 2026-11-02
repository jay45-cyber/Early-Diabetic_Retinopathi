"""Abstract Base Class for Retinal Dataset Ingestion Adapters."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd


class BaseDatasetAdapter(ABC):
    """Abstract class defining the contract for clinical dataset ingestion."""

    def __init__(self, data_dir: str | Path, metadata_file: str | Path | None = None):
        self.data_dir = Path(data_dir)
        self.metadata_file = Path(metadata_file) if metadata_file else None

    @abstractmethod
    def get_dataset_metadata(self) -> Dict[str, Any]:
        """Return dataset provenance, citation, license, and clinical suitability."""
        pass

    @abstractmethod
    def ingest(self) -> pd.DataFrame:
        """Parse raw metadata and directory structure into the unified manifest schema."""
        pass


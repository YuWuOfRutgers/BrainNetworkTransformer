import numpy as np
import torch
from .preprocess import StandardScaler
from omegaconf import DictConfig, open_dict


def load_synthetic_data(cfg: DictConfig):
    """
    Load synthetic brain network dataset.

    This dataset has the same structure as ABIDE but with different dimensions:
    - 1000 samples
    - 53 brain regions (ROIs)
    - 200 timepoints
    - Binary classification (0: HC, 1: ASD)

    Args:
        cfg: Hydra configuration object

    Returns:
        final_timeseires: [N, 53, 200] time series tensor
        final_pearson: [N, 53, 53] correlation matrix tensor
        labels: [N] label tensor
        site: [N] site ID array
    """
    data = np.load(cfg.dataset.path, allow_pickle=True).item()
    final_timeseires = data["timeseires"] # if the .npy doesn't have timeseires, let it to be an empty array.
    final_pearson = data["corr"]
    labels = data["label"]
    site = data['site']

    # Standardize time series
    scaler = StandardScaler(mean=np.mean(
        final_timeseires), std=np.std(final_timeseires))

    final_timeseires = scaler.transform(final_timeseires)

    # Convert to PyTorch tensors
    final_timeseires, final_pearson, labels = [torch.from_numpy(
        data).float() for data in (final_timeseires, final_pearson, labels)]

    # Add dataset dimensions to config dynamically
    with open_dict(cfg):
        cfg.dataset.node_sz, cfg.dataset.node_feature_sz = final_pearson.shape[1:]
        cfg.dataset.timeseries_sz = final_timeseires.shape[2]

    return final_timeseires, final_pearson, labels, site

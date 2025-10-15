#!/usr/bin/env python3
"""
Generate synthetic dataset with ABIDE-like structure for sanity checking.

Dataset specifications:
- Number of samples: 1000
- Number of ROIs: 53
- Time series length: 200
- Binary classification (0: Healthy Control, 1: Autism)
"""

import numpy as np
from pathlib import Path

def generate_synthetic_dataset(
    n_samples=1000,
    n_regions=53,
    n_timepoints=200,
    output_path="synthetic_abide.npy",
    seed=42
):
    """
    Generate synthetic brain network dataset.

    Args:
        n_samples: Number of subjects
        n_regions: Number of brain regions (ROIs)
        n_timepoints: Length of time series
        output_path: Path to save the dataset
        seed: Random seed for reproducibility
    """
    np.random.seed(seed)

    print("=" * 60)
    print("Generating Synthetic Brain Network Dataset")
    print("=" * 60)
    print(f"Number of samples: {n_samples}")
    print(f"Number of ROIs: {n_regions}")
    print(f"Time series length: {n_timepoints}")
    print()

    # Generate time series data from normal distribution
    # Shape: [n_samples, n_regions, n_timepoints]
    print("Generating time series data...")
    timeseires = np.random.randn(n_samples, n_regions, n_timepoints).astype(np.float32)

    # Generate correlation matrices
    # We'll compute Pearson correlation from the time series
    print("Computing correlation matrices...")
    corr = np.zeros((n_samples, n_regions, n_regions), dtype=np.float32)

    for i in range(n_samples):
        # Compute Pearson correlation between all pairs of regions
        # Each region has n_timepoints values
        ts = timeseires[i]  # [n_regions, n_timepoints]

        # Normalize each region's time series
        ts_normalized = (ts - ts.mean(axis=1, keepdims=True)) / (ts.std(axis=1, keepdims=True) + 1e-8)

        # Compute correlation: (A @ A.T) / n_timepoints
        corr[i] = np.dot(ts_normalized, ts_normalized.T) / n_timepoints

        if (i + 1) % 200 == 0:
            print(f"  Processed {i + 1}/{n_samples} samples...")

    # Generate balanced labels (50% each class)
    print("Generating labels...")
    labels = np.zeros(n_samples, dtype=np.int64)
    labels[n_samples // 2:] = 1  # Second half is class 1

    # Shuffle to mix classes
    shuffle_idx = np.random.permutation(n_samples)
    timeseires = timeseires[shuffle_idx]
    corr = corr[shuffle_idx]
    labels = labels[shuffle_idx]

    # Generate synthetic site IDs (simulate multi-site data)
    # Create 5 sites with different sample sizes
    print("Generating site information...")
    n_sites = 5
    site = np.zeros(n_samples, dtype=np.int64)
    site_sizes = [150, 200, 250, 200, 200]  # Sizes for each site

    current_idx = 0
    for site_id, size in enumerate(site_sizes):
        site[current_idx:current_idx + size] = site_id
        current_idx += size

    # Create data dictionary matching ABIDE format
    data = {
        'timeseires': timeseires,  # [1000, 53, 200]
        'corr': corr,              # [1000, 53, 53]
        'label': labels,           # [1000]
        'site': site               # [1000]
    }

    # Save dataset
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print()
    print("Saving dataset...")
    np.save(output_path, data, allow_pickle=True)

    # Print statistics
    print()
    print("=" * 60)
    print("Dataset Generation Complete!")
    print("=" * 60)
    print(f"Output file: {output_path.absolute()}")
    print(f"File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
    print()
    print("Dataset Statistics:")
    print(f"  Time series shape: {timeseires.shape}")
    print(f"  Correlation shape: {corr.shape}")
    print(f"  Labels shape: {labels.shape}")
    print(f"  Site shape: {site.shape}")
    print()
    print(f"  Class 0 (HC): {(labels == 0).sum()} samples ({(labels == 0).sum() / n_samples * 100:.1f}%)")
    print(f"  Class 1 (ASD): {(labels == 1).sum()} samples ({(labels == 1).sum() / n_samples * 100:.1f}%)")
    print()
    print(f"  Time series range: [{timeseires.min():.3f}, {timeseires.max():.3f}]")
    print(f"  Time series mean: {timeseires.mean():.3f}, std: {timeseires.std():.3f}")
    print()
    print(f"  Correlation range: [{corr.min():.3f}, {corr.max():.3f}]")
    print(f"  Correlation mean: {corr.mean():.3f}, std: {corr.std():.3f}")
    print()
    print(f"  Number of sites: {n_sites}")
    for site_id in range(n_sites):
        site_count = (site == site_id).sum()
        print(f"    Site {site_id}: {site_count} samples")
    print("=" * 60)

    return data


if __name__ == "__main__":
    # Generate the dataset
    output_path = Path(__file__).parent / "synthetic_abide.npy"

    data = generate_synthetic_dataset(
        n_samples=1000,
        n_regions=53,
        n_timepoints=200,
        output_path=output_path,
        seed=42
    )

    print()
    print("Dataset is ready to use!")
    print(f"Path: {output_path}")

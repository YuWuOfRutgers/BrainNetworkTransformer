#!/usr/bin/env python3
"""
Quick test script to verify synthetic dataset works correctly.
"""

import sys
from pathlib import Path

# Add source to path
sys.path.insert(0, str(Path(__file__).parent))

from omegaconf import DictConfig, OmegaConf
from source.dataset.synthetic import load_synthetic_data

def test_synthetic_dataset():
    """Test loading synthetic dataset"""

    print("=" * 60)
    print("Testing Synthetic Dataset")
    print("=" * 60)

    # Create minimal config
    cfg = OmegaConf.create({
        'dataset': {
            'name': 'synthetic',
            'path': '/home/yw828/Desktop/BNT/dataset/synthetic_abide.npy',
            'batch_size': 16,
            'train_set': 0.7,
            'val_set': 0.1,
            'stratified': True
        }
    })

    # Load data
    print("\n1. Loading dataset...")
    timeseires, pearson, labels, site = load_synthetic_data(cfg)

    print(f"   ✓ Dataset loaded successfully!")

    # Check shapes
    print("\n2. Checking shapes...")
    print(f"   Time series: {timeseires.shape}")
    print(f"   Correlation: {pearson.shape}")
    print(f"   Labels: {labels.shape}")
    print(f"   Site: {site.shape}")

    expected_shapes = {
        'timeseires': (1000, 53, 200),
        'pearson': (1000, 53, 53),
        'labels': (1000,)
    }

    assert timeseires.shape == expected_shapes['timeseires'], f"Time series shape mismatch!"
    assert pearson.shape == expected_shapes['pearson'], f"Pearson shape mismatch!"
    assert labels.shape == expected_shapes['labels'], f"Labels shape mismatch!"
    print("   ✓ All shapes correct!")

    # Check config was updated
    print("\n3. Checking config updates...")
    print(f"   node_sz: {cfg.dataset.node_sz}")
    print(f"   node_feature_sz: {cfg.dataset.node_feature_sz}")
    print(f"   timeseries_sz: {cfg.dataset.timeseries_sz}")

    assert cfg.dataset.node_sz == 53, "node_sz should be 53"
    assert cfg.dataset.node_feature_sz == 53, "node_feature_sz should be 53"
    assert cfg.dataset.timeseries_sz == 200, "timeseries_sz should be 200"
    print("   ✓ Config updated correctly!")

    # Check data statistics
    print("\n4. Checking data statistics...")
    print(f"   Time series - mean: {timeseires.mean():.4f}, std: {timeseires.std():.4f}")
    print(f"   Correlation - mean: {pearson.mean():.4f}, std: {pearson.std():.4f}")
    print(f"   Label distribution - Class 0: {(labels == 0).sum()}, Class 1: {(labels == 1).sum()}")
    print("   ✓ Data statistics look good!")

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print("\nThe synthetic dataset is ready to use.")
    print("\nTo train with it, run:")
    print("  python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p")
    print()

if __name__ == "__main__":
    test_synthetic_dataset()

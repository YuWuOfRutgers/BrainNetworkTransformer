# Synthetic Brain Network Dataset

This directory contains a synthetic dataset that mimics the structure of the ABIDE dataset but with different dimensions for sanity checking and testing purposes.

## Dataset Specifications

```
Total Dataset Shape:
├── Number of samples (N): 1000 subjects
├── Time series: [1000, 53, 200]
│   ├── 53 = number of brain regions/nodes (ROIs)
│   └── 200 = time series length (timepoints)
├── Correlation matrix: [1000, 53, 53]
│   └── Pearson correlation between all pairs of 53 regions
└── Labels: [1000]
    └── Binary: 0 (Healthy Control) or 1 (Autism)
```

## Data Statistics

- **Total samples**: 1000
- **Class distribution**:
  - Class 0 (Healthy Control): 500 samples (50%)
  - Class 1 (Autism): 500 samples (50%)
- **Number of sites**: 5 (for stratified splitting)
  - Site 0: 150 samples
  - Site 1: 200 samples
  - Site 2: 250 samples
  - Site 3: 200 samples
  - Site 4: 200 samples
- **Time series**: Sampled from standard normal distribution N(0,1)
- **Correlation matrices**: Computed from time series using Pearson correlation
- **File size**: ~51 MB

## Files

- `generate_synthetic_dataset.py` - Script to generate the synthetic dataset
- `synthetic_abide.npy` - The generated dataset file (51 MB)
- `SYNTHETIC_DATASET_README.md` - This file

## Generating the Dataset

To regenerate the dataset with different parameters:

```bash
cd /home/yw828/Desktop/BNT/dataset
python generate_synthetic_dataset.py
```

You can modify the parameters in the script:

```python
data = generate_synthetic_dataset(
    n_samples=1000,      # Number of subjects
    n_regions=53,        # Number of ROIs
    n_timepoints=200,    # Time series length
    output_path="synthetic_abide.npy",
    seed=42              # Random seed for reproducibility
)
```

## Using the Synthetic Dataset

### 1. Test Dataset Loading

Run the test script to verify the dataset loads correctly:

```bash
cd /home/yw828/Desktop/BNT/BrainNetworkTransformer
python test_synthetic_dataset.py
```

### 2. Train a Model

Train BrainNetCNN on the synthetic dataset:

```bash
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p
```

Train BNT (Brain Network Transformer):

```bash
python -m source dataset=SYNTHETIC model=bnt datasz=100p
```

### 3. Quick Sanity Check (2 epochs only)

For quick testing:

```bash
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p repeat_time=1 training.epochs=2
```

### 4. Compare Multiple Models

```bash
python -m source --multirun dataset=SYNTHETIC model=bnt,brainnetcnn,transformer datasz=100p repeat_time=3
```

## Configuration

The synthetic dataset configuration is located at:
`source/conf/dataset/SYNTHETIC.yaml`

```yaml
name: synthetic
batch_size: 16
test_batch_size: 16
val_batch_size: 16
train_set: 0.7        # 70% training (700 samples)
val_set: 0.1          # 10% validation (100 samples)
                      # 20% test (200 samples)
path: /home/yw828/Desktop/BNT/dataset/synthetic_abide.npy
stratified: True      # Stratified split by site
drop_last: True
```

## Data Splits

With the default configuration:
- **Training**: 700 samples (70%)
- **Validation**: 100 samples (10%)
- **Testing**: 200 samples (20%)

With `batch_size=16` and `drop_last=True`:
- **Training batches per epoch**: 43 batches (688 samples used, 12 dropped)
- **Validation batches**: 6 batches (96 samples used, 4 dropped)
- **Test batches**: 12 batches (192 samples used, 8 dropped)

## Dataset Loader

The dataset loader is implemented in:
`source/dataset/synthetic.py`

It follows the same interface as ABIDE and ABCD loaders:

```python
from source.dataset.synthetic import load_synthetic_data

timeseires, pearson, labels, site = load_synthetic_data(cfg)
# Returns:
#   timeseires: torch.Tensor [1000, 53, 200]
#   pearson: torch.Tensor [1000, 53, 53]
#   labels: torch.Tensor [1000]
#   site: numpy.ndarray [1000]
```

## Comparison with ABIDE

| Property | ABIDE | Synthetic |
|----------|-------|-----------|
| Samples | ~871 | 1000 |
| ROIs | 360 | 53 |
| Timepoints | ~200 | 200 |
| Classes | 2 (balanced) | 2 (balanced) |
| Sites | ~20 | 5 |
| Data source | Real fMRI | Random normal |
| File size | ~770 MB | ~51 MB |

## Use Cases

1. **Sanity checking**: Verify code runs without errors
2. **Quick testing**: Faster iteration during development
3. **Algorithm validation**: Test new architectures with known data properties
4. **Debugging**: Smaller dimensions make it easier to trace issues
5. **CI/CD**: Automated testing with lightweight dataset

## Notes

- The synthetic data is **randomly generated** and has no biological meaning
- Correlation matrices are **computed from the time series** (not independently generated)
- The dataset is **perfectly reproducible** (seed=42)
- Performance metrics on this dataset are **not meaningful** (random data)
- Use this for **code verification only**, not for scientific validation

## Extending to Other Dimensions

To create datasets with different dimensions, modify the parameters in `generate_synthetic_dataset.py`:

```python
# Example: Smaller dataset for faster testing
data = generate_synthetic_dataset(
    n_samples=100,       # Fewer samples
    n_regions=20,        # Fewer ROIs
    n_timepoints=50,     # Shorter time series
    seed=42
)

# Example: Larger dataset closer to original ABIDE
data = generate_synthetic_dataset(
    n_samples=871,       # Match ABIDE sample count
    n_regions=360,       # Match ABIDE ROIs
    n_timepoints=200,
    seed=42
)
```

## Troubleshooting

**Issue**: Module not found errors
```bash
# Solution: Use the bnt conda environment
/home/yw828/miniconda3/envs/bnt/bin/python -m source dataset=SYNTHETIC ...
```

**Issue**: Dataset path not found
```bash
# Solution: Check the path in SYNTHETIC.yaml matches the generated file
ls -lh /home/yw828/Desktop/BNT/dataset/synthetic_abide.npy
```

**Issue**: Out of memory during training
```bash
# Solution: Reduce batch size
python -m source dataset=SYNTHETIC model=brainnetcnn dataset.batch_size=8
```

## License

This synthetic dataset is for testing purposes only and inherits the license of the BrainNetworkTransformer project.

# Quick Start: Synthetic Dataset

## TL;DR - Run This Now! 🚀

```bash
cd /home/yw828/Desktop/BNT/BrainNetworkTransformer

# Test the dataset
python test_synthetic_dataset.py

# Quick 2-epoch training (30 seconds)
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p repeat_time=1 training.epochs=2
```

---

## Dataset Info

| Property | Value |
|----------|-------|
| Samples | 1000 |
| ROIs | 53 |
| Timepoints | 200 |
| Classes | 2 (balanced) |
| File size | 51 MB |

---

## Common Commands

### 1. Quick Sanity Check (30 sec)
```bash
python -m source dataset=SYNTHETIC model=brainnetcnn training.epochs=2
```

### 2. Full Training with BrainNetCNN
```bash
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p
```

### 3. Train BNT (Brain Network Transformer)
```bash
python -m source dataset=SYNTHETIC model=bnt datasz=100p
```

### 4. Compare All Models
```bash
python -m source --multirun dataset=SYNTHETIC model=bnt,brainnetcnn,transformer datasz=100p
```

### 5. Different Data Percentages
```bash
python -m source --multirun dataset=SYNTHETIC model=brainnetcnn datasz=10p,50p,100p
```

### 6. Custom Batch Size
```bash
python -m source dataset=SYNTHETIC model=brainnetcnn dataset.batch_size=32
```

---

## Expected Output (2 epochs)

```
[INFO] #model params: 274717
[INFO] Epoch[0/2] | Train Loss: 11.093 | Train Accuracy: 25.145% | ...
[INFO] Epoch[1/2] | Train Loss: 11.094 | Train Accuracy: 26.599% | ...
✓ Training complete!
```

**Note**: Performance is random (synthetic data) - this is expected!

---

## File Locations

```
BNT/
├── dataset/
│   ├── synthetic_abide.npy              # The dataset (51 MB)
│   ├── generate_synthetic_dataset.py    # Generation script
│   └── SYNTHETIC_DATASET_README.md      # Full documentation
│
└── BrainNetworkTransformer/
    ├── source/
    │   ├── conf/dataset/SYNTHETIC.yaml  # Config
    │   └── dataset/synthetic.py         # Loader
    │
    ├── test_synthetic_dataset.py        # Test script
    ├── SYNTHETIC_DATASET_SETUP.md       # Setup guide
    └── QUICK_START_SYNTHETIC.md         # This file
```

---

## Troubleshooting One-Liners

```bash
# Verify dataset loads
python test_synthetic_dataset.py

# Check file exists
ls -lh /home/yw828/Desktop/BNT/dataset/synthetic_abide.npy

# List available datasets
ls source/conf/dataset/

# Verify config
cat source/conf/dataset/SYNTHETIC.yaml

# Test with minimal settings
python -m source dataset=SYNTHETIC model=brainnetcnn training.epochs=1 dataset.batch_size=8
```

---

## Remember

✅ Use for: Code testing, debugging, algorithm development
❌ Don't use for: Scientific validation, real results

The data is **randomly generated** - performance metrics are meaningless!

---

## Need Help?

- Full docs: `SYNTHETIC_DATASET_SETUP.md`
- Dataset details: `BNT/dataset/SYNTHETIC_DATASET_README.md`
- Test script: `python test_synthetic_dataset.py`

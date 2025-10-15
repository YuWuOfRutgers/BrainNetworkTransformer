# Synthetic Dataset Setup - Complete Summary

## ✅ What Was Created

A synthetic brain network dataset with ABIDE-like structure for sanity checking and testing.

### Dataset Specifications
- **Samples**: 1000 subjects (500 per class)
- **ROIs**: 53 brain regions
- **Time series**: 200 timepoints
- **Format**: Same as ABIDE dataset
- **Size**: ~51 MB (vs. ABIDE's ~770 MB)

---

## 📁 Files Created

### 1. Dataset Files (in `/home/yw828/Desktop/BNT/dataset/`)
- ✅ `generate_synthetic_dataset.py` - Generation script
- ✅ `synthetic_abide.npy` - The dataset (51 MB)
- ✅ `SYNTHETIC_DATASET_README.md` - Detailed documentation

### 2. Configuration Files (in `source/conf/dataset/`)
- ✅ `SYNTHETIC.yaml` - Hydra config for synthetic dataset

### 3. Dataset Loader (in `source/dataset/`)
- ✅ `synthetic.py` - Loader following ABIDE/ABCD pattern
- ✅ `__init__.py` - Updated to include synthetic dataset

### 4. Test Script (in project root)
- ✅ `test_synthetic_dataset.py` - Verification script

---

## 🚀 How to Use

### Quick Test (Recommended First Step)
```bash
cd /home/yw828/Desktop/BNT/BrainNetworkTransformer
python test_synthetic_dataset.py
```

Expected output:
```
============================================================
Testing Synthetic Dataset
============================================================
...
✓ All tests passed!
```

### Train BrainNetCNN (2 epochs for quick sanity check)
```bash
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p repeat_time=1 training.epochs=2
```

### Train BNT (Brain Network Transformer)
```bash
python -m source dataset=SYNTHETIC model=bnt datasz=100p
```

### Full Training (100 epochs, 5 repeats)
```bash
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p
```

### Compare Multiple Models
```bash
python -m source --multirun dataset=SYNTHETIC model=bnt,brainnetcnn,transformer datasz=100p
```

---

## 📊 Data Structure

```python
data = {
    'timeseires': [1000, 53, 200],   # Time series
    'corr': [1000, 53, 53],          # Correlation matrices
    'label': [1000],                  # Binary labels (0/1)
    'site': [1000]                    # Site IDs (0-4)
}
```

### Data Splits (default config)
- Training: 700 samples (70%)
- Validation: 100 samples (10%)
- Testing: 200 samples (20%)

---

## 🔍 Verification

All components have been tested:

### ✅ Dataset Generation
```bash
cd /home/yw828/Desktop/BNT/dataset
/home/yw828/miniconda3/envs/bnt/bin/python generate_synthetic_dataset.py
```
Result: Generated 51 MB file with correct dimensions

### ✅ Dataset Loading
```bash
python test_synthetic_dataset.py
```
Result: All shapes and statistics correct

### ✅ End-to-End Training
```bash
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p repeat_time=1 training.epochs=2
```
Result: Training completed successfully with metrics logged

---

## 🛠️ Technical Details

### Dataset Generation
- **Time series**: Sampled from N(0, 1)
- **Correlation**: Computed via Pearson correlation from time series
- **Labels**: Balanced 50/50 split
- **Sites**: 5 sites with sizes [150, 200, 250, 200, 200]
- **Seed**: 42 (reproducible)

### Configuration Flow
```
SYNTHETIC.yaml
    ↓
dataset_factory(cfg)
    ↓
load_synthetic_data(cfg)
    ↓
Returns: (timeseires, pearson, labels, site)
    ↓
init_stratified_dataloader()
    ↓
DataLoader objects
```

### Model Compatibility
Works with all models in the framework:
- ✅ BrainNetCNN
- ✅ BrainNetworkTransformer (BNT)
- ✅ GraphTransformer
- ✅ FBNetGen

---

## 📝 Key Files Modified

1. **source/dataset/__init__.py**
   - Added `from .synthetic import load_synthetic_data`
   - Updated assertion: `assert cfg.dataset.name in ['abcd', 'abide', 'synthetic']`

2. **source/dataset/synthetic.py** (NEW)
   - Implements `load_synthetic_data()` function
   - Follows same interface as ABIDE/ABCD loaders

3. **source/conf/dataset/SYNTHETIC.yaml** (NEW)
   - Dataset configuration matching ABIDE.yaml structure

---

## 🎯 Use Cases

### 1. Sanity Checking
```bash
# Quick 2-epoch test
python -m source dataset=SYNTHETIC model=brainnetcnn training.epochs=2
```

### 2. Code Debugging
- Smaller dimensions (53 vs 360 ROIs)
- Faster loading (~51 MB vs ~770 MB)
- Known data properties (random normal)

### 3. Algorithm Development
- Test new models before using real data
- Verify training pipeline works
- Check data augmentation effects

### 4. Performance Profiling
```bash
# Compare different batch sizes
python -m source --multirun dataset=SYNTHETIC model=brainnetcnn dataset.batch_size=8,16,32
```

---

## 🔄 Regenerating Dataset

To create a new version with different parameters:

```bash
cd /home/yw828/Desktop/BNT/dataset
/home/yw828/miniconda3/envs/bnt/bin/python generate_synthetic_dataset.py
```

Edit `generate_synthetic_dataset.py` to modify:
- `n_samples` (default: 1000)
- `n_regions` (default: 53)
- `n_timepoints` (default: 200)
- `seed` (default: 42)

---

## ⚠️ Important Notes

1. **Not for Scientific Use**: Data is randomly generated, no biological meaning
2. **Performance Metrics**: Random data → random performance (expected)
3. **Purpose**: Code verification and testing only
4. **Environment**: Use `bnt` conda environment for all operations

---

## 🐛 Troubleshooting

### Issue: Module not found
**Solution**: Use the correct Python environment
```bash
/home/yw828/miniconda3/envs/bnt/bin/python -m source ...
```

### Issue: Path not found
**Solution**: Check path in config
```bash
cat source/conf/dataset/SYNTHETIC.yaml
ls -lh /home/yw828/Desktop/BNT/dataset/synthetic_abide.npy
```

### Issue: Training crashes
**Solution**: Check dimensions match config
```bash
python test_synthetic_dataset.py
```

---

## 📚 Additional Documentation

- Dataset details: `/home/yw828/Desktop/BNT/dataset/SYNTHETIC_DATASET_README.md`
- Original ABIDE: `source/conf/dataset/ABIDE.yaml`
- BNT Project: `readme.md`

---

## ✨ Summary

You now have:
1. ✅ Synthetic dataset generated (1000 samples, 53 ROIs, 200 timepoints)
2. ✅ Configuration files added
3. ✅ Dataset loader implemented
4. ✅ Everything tested and working
5. ✅ Ready to use for sanity checking

**Next Step**: Run your first training!
```bash
python -m source dataset=SYNTHETIC model=brainnetcnn datasz=100p repeat_time=1 training.epochs=2
```

Enjoy testing! 🎉

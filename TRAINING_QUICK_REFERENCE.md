# Quick Reference: Model Training

## Train Model with Your Resumes

### Step 1: Add Resume Files
Place resume files (PDF, DOCX, or TXT) in:
```
C:\Users\mdnur\Downloads\archive (2)\
```

### Step 2: Run Training Script
```bash
cd "C:\Users\mdnur\OneDrive\Desktop\ATS System\backend"
python train_with_resumes.py
```

### Step 3: Restart Backend
The system automatically detects and loads the trained model on startup.
```bash
cd "C:\Users\mdnur\OneDrive\Desktop\ATS System\backend"
python -m uvicorn main:app --reload
```

---

## Training Output Example

```
============================================================
ATS SBERT Model Training Pipeline
============================================================
✅ Using manual dataset from: C:\Users\mdnur\Downloads\archive (2)

Processing 1/5: Aline CV.txt ✅ → Data Scientist, Business Analyst
Processing 2/5: resume.pdf ✅ → Software Engineer, DevOps Engineer

✅ Created 18 training examples
   - Processed: 4 resumes
   - Positive pairs: 10
   - Negative pairs: 8

Training set: 14 examples
Validation set: 4 examples

100%|██████████| 6/6 [00:29<00:00, 4.99s/it]

============================================================
✅ Training Complete!
Model saved to: ./models/ats_sbert_finetuned
============================================================
```

---

## Job Categories (Auto-detected)

The training script automatically matches resumes to these categories:

### IT Roles
- Software Engineer
- Data Scientist
- DevOps Engineer
- Data Engineer
- Security Engineer
- QA Engineer
- Network Engineer

### Business Roles
- Business Analyst
- Product Manager
- UI/UX Designer

---

## Keyword Matching

Each category has associated keywords. Example:

**Software Engineer**:
- software, developer, programming, coding
- java, python, javascript, react, node
- api, backend, frontend, database

**Data Scientist**:
- data, analytics, machine learning, statistics
- python, sql, pandas, numpy
- ml, ai, tensorflow, pytorch

---

## Training Parameters

Edit these in `train_with_resumes.py`:

```python
trainer.train(
    epochs=3,        # Number of training iterations
    batch_size=8     # Samples processed together
)
```

**Recommended Settings**:
- **Few resumes (5-10)**: epochs=2, batch_size=4
- **Medium dataset (10-30)**: epochs=3, batch_size=8
- **Large dataset (30+)**: epochs=4, batch_size=16

---

## Model Files Location

```
backend/models/ats_sbert_finetuned/
├── config.json
├── config_sentence_transformers.json
├── model.safetensors (trained weights)
├── modules.json
├── sentence_bert_config.json
├── tokenizer.json
├── vocab.txt
└── 1_Pooling/config.json
```

---

## Verify Model is Loaded

When you start the backend, look for:

✅ **With trained model**:
```
Loading fine-tuned SBERT model from ./models/ats_sbert_finetuned...
✅ Fine-tuned SBERT model loaded successfully!
```

⚠️ **Without trained model**:
```
⚠️ Fine-tuned model not found, using base model (all-MiniLM-L6-v2)...
SBERT model loaded successfully!
```

---

## Troubleshooting

### "No resume files found"
**Solution**: Make sure files are in the correct directory:
```
C:\Users\mdnur\Downloads\archive (2)\
```

### "No training data available"
**Solution**: Resumes need to match at least 15% of keywords for a category. Add more diverse resumes.

### "ImportError: datasets"
**Solution**: Install missing dependency:
```bash
pip install datasets
```

### "Model not loading"
**Solution**: Check if model folder exists:
```bash
dir backend\models\ats_sbert_finetuned
```

---

## Performance Tips

### 1. More Data = Better Model
- Minimum: 5-10 resumes
- Good: 20-30 resumes
- Excellent: 50+ resumes

### 2. Diverse Resumes
Include various:
- Job roles (software, data, business, etc.)
- Experience levels (fresher, mid-level, senior)
- Industries (tech, finance, healthcare, etc.)

### 3. Training Time
- 5 resumes: ~30 seconds
- 30 resumes: ~2-3 minutes
- 50+ resumes: ~5-10 minutes

---

## Re-training

To update the model with new resumes:

1. Add new resume files to the dataset folder
2. Run training script again
3. Restart backend server

**Note**: Training overwrites the previous model.

---

## Backup Model

To keep a backup:
```bash
cd backend/models
cp -r ats_sbert_finetuned ats_sbert_finetuned_backup
```

---

## Check Current Model

```python
# In Python console:
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('./models/ats_sbert_finetuned')
print(model)
```

---

## Model Size

- Base model: ~90.9 MB
- Fine-tuned model: ~90.9 MB (same size, different weights)
- Training takes: ~100-200 MB RAM

---

## Questions?

Check the main documentation:
- [README.md](README.md) - Complete project overview
- [TRAINING_COMPLETE.md](TRAINING_COMPLETE.md) - Detailed training info
- [backend/TRAINING_GUIDE.md](backend/TRAINING_GUIDE.md) - Kaggle dataset guide

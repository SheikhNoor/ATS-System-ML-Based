"""
Train ATS SBERT Model using Resume Files
Optimized for local resume dataset without CSV files
"""

import os
import sys
import random
from pathlib import Path
from typing import List, Dict
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader

class ResumeModelTrainer:
    """Train SBERT model using resume files directly"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Job categories with keywords for matching
        self.job_categories = {
            'Software Engineer': ['software', 'developer', 'programming', 'coding', 'java', 'python', 
                                'javascript', 'react', 'node', 'api', 'backend', 'frontend'],
            'Data Scientist': ['data', 'analytics', 'machine learning', 'statistics', 'python', 'sql',
                             'ml', 'ai', 'tensorflow', 'pytorch', 'pandas', 'numpy'],
            'DevOps Engineer': ['devops', 'cloud', 'aws', 'docker', 'kubernetes', 'ci/cd', 'jenkins',
                              'ansible', 'terraform', 'linux', 'automation'],
            'Business Analyst': ['business', 'analysis', 'requirements', 'stakeholder', 'documentation',
                               'agile', 'scrum', 'project management'],
            'Network Engineer': ['network', 'cisco', 'routing', 'switching', 'firewall', 'tcp/ip',
                               'ccna', 'vpn', 'lan', 'wan'],
            'QA Engineer': ['testing', 'quality', 'qa', 'automation', 'selenium', 'test cases',
                          'junit', 'manual testing', 'regression'],
            'Data Engineer': ['data engineering', 'etl', 'spark', 'hadoop', 'pipeline', 'database',
                            'sql', 'nosql', 'airflow'],
            'Security Engineer': ['security', 'cybersecurity', 'penetration', 'vulnerability', 
                                'firewall', 'encryption', 'compliance'],
            'UI/UX Designer': ['ui', 'ux', 'design', 'figma', 'adobe', 'user experience', 
                              'wireframe', 'prototype'],
            'Product Manager': ['product', 'roadmap', 'features', 'stakeholder', 'agile',
                              'requirements', 'strategy']
        }
    
    def extract_resume_text(self, filepath: str) -> str:
        """Extract text from resume file"""
        try:
            if filepath.endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Check if it's tuple format from NER dataset
                    if content.strip().startswith('('):
                        # Extract text from tuple format: ("text", {entities})
                        try:
                            # Find text between first (' and ',
                            start_idx = content.find("('") + 2
                            end_idx = content.find("',", start_idx)
                            if start_idx > 1 and end_idx > start_idx:
                                text = content[start_idx:end_idx]
                                # Unescape some common patterns
                                text = text.replace('\\n', '\n').replace('â€¢', '•')
                                return text[:3000]  # Limit to 3000 chars
                        except:
                            pass
                    
                    # Plain text file
                    return content[:3000]
            
            elif filepath.endswith('.pdf'):
                import pdfplumber
                with pdfplumber.open(filepath) as pdf:
                    text = ''
                    for page in pdf.pages[:3]:  # First 3 pages only
                        text += page.extract_text() or ''
                    return text[:3000]
            
            elif filepath.endswith('.docx'):
                from docx import Document
                doc = Document(filepath)
                text = '\n'.join([para.text for para in doc.paragraphs])
                return text[:3000]
                
        except Exception as e:
            print(f"  ⚠️ Error reading {os.path.basename(filepath)}: {e}")
            return ""
        
        return ""
    
    def match_resume_to_jobs(self, resume_text: str) -> List[str]:
        """Match resume to relevant job categories based on keywords"""
        resume_lower = resume_text.lower()
        matched_jobs = []
        
        for job, keywords in self.job_categories.items():
            # Count keyword matches
            keyword_matches = sum(1 for kw in keywords if kw.lower() in resume_lower)
            match_ratio = keyword_matches / len(keywords)
            
            # If at least 15% of keywords match, consider it a match
            if match_ratio >= 0.15:
                matched_jobs.append((job, match_ratio))
        
        # Return top 3 matched jobs
        matched_jobs.sort(key=lambda x: x[1], reverse=True)
        return [job for job, _ in matched_jobs[:3]]
    
    def create_job_description(self, job_title: str) -> str:
        """Create a synthetic job description"""
        keywords = self.job_categories.get(job_title, [])
        
        templates = [
            f"We are looking for an experienced {job_title} with strong skills in {', '.join(keywords[:3])}. "
            f"The ideal candidate should have expertise in {', '.join(keywords[3:6])} and {keywords[6] if len(keywords) > 6 else 'related technologies'}.",
            
            f"Seeking a talented {job_title} to join our team. Must have proficiency in {', '.join(keywords[:4])}. "
            f"Experience with {', '.join(keywords[4:7])} is highly preferred.",
            
            f"{job_title} role requiring hands-on experience with {', '.join(keywords[:3])}. "
            f"Strong background in {', '.join(keywords[3:5])} and {keywords[5] if len(keywords) > 5 else 'industry standards'} needed."
        ]
        
        return random.choice(templates)
    
    def load_training_data(self) -> List[InputExample]:
        """Load and prepare training data from resume files"""
        print("\n" + "="*60)
        print("Loading Resume Data for Training")
        print("="*60)
        
        # Find all resume files
        resume_files = []
        for ext in ['.txt', '.pdf', '.docx']:
            resume_files.extend(Path(self.dataset_path).glob(f'*{ext}'))
        
        if not resume_files:
            print("❌ No resume files found!")
            return []
        
        print(f"Found {len(resume_files)} resume files")
        
        training_examples = []
        processed_count = 0
        
        # Process each resume
        for i, resume_file in enumerate(resume_files, 1):
            print(f"\nProcessing {i}/{len(resume_files)}: {resume_file.name}", end=' ')
            
            # Extract resume text
            resume_text = self.extract_resume_text(str(resume_file))
            
            if not resume_text or len(resume_text) < 100:
                print("❌ (too short)")
                continue
            
            # Match resume to job categories
            matched_jobs = self.match_resume_to_jobs(resume_text)
            
            if not matched_jobs:
                print("⚠️ (no matches)")
                continue
            
            print(f"✅ → {', '.join(matched_jobs)}")
            
            # Create POSITIVE pairs (resume with matching jobs)
            for job in matched_jobs:
                job_desc = self.create_job_description(job)
                training_examples.append(
                    InputExample(texts=[resume_text, job_desc], label=1.0)
                )
            
            # Create NEGATIVE pairs (resume with non-matching jobs)
            non_matched_jobs = [job for job in self.job_categories.keys() 
                              if job not in matched_jobs]
            
            if non_matched_jobs:
                # Create 1-2 negative pairs per resume
                num_neg = min(2, len(non_matched_jobs))
                neg_jobs = random.sample(non_matched_jobs, num_neg)
                
                for neg_job in neg_jobs:
                    neg_desc = self.create_job_description(neg_job)
                    training_examples.append(
                        InputExample(texts=[resume_text, neg_desc], label=0.0)
                    )
            
            processed_count += 1
            
            # Limit processing for faster training
            if processed_count >= 30:
                print(f"\n\n⚠️ Limited to 30 resumes for faster training")
                break
        
        print("\n" + "="*60)
        print(f"✅ Created {len(training_examples)} training examples")
        print(f"   - Processed: {processed_count} resumes")
        print(f"   - Positive pairs: {sum(1 for ex in training_examples if ex.label == 1.0)}")
        print(f"   - Negative pairs: {sum(1 for ex in training_examples if ex.label == 0.0)}")
        print("="*60)
        
        return training_examples
    
    def train(self, epochs: int = 3, batch_size: int = 8):
        """Train the model"""
        # Load training data
        training_examples = self.load_training_data()
        
        if len(training_examples) < 10:
            print("❌ Not enough training data!")
            return False
        
        # Split into train/validation (80/20)
        split_idx = int(len(training_examples) * 0.8)
        train_examples = training_examples[:split_idx]
        val_examples = training_examples[split_idx:]
        
        print(f"\nTraining set: {len(train_examples)} examples")
        print(f"Validation set: {len(val_examples)} examples")
        
        # Create data loader
        train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=batch_size)
        
        # Define loss function
        train_loss = losses.CosineSimilarityLoss(self.model)
        
        # Create evaluator
        val_sentences1 = [ex.texts[0] for ex in val_examples]
        val_sentences2 = [ex.texts[1] for ex in val_examples]
        val_scores = [ex.label for ex in val_examples]
        
        evaluator = EmbeddingSimilarityEvaluator(
            val_sentences1, val_sentences2, val_scores,
            name='ats-validation'
        )
        
        # Training
        print("\n" + "="*60)
        print("Starting Training")
        print("="*60)
        print(f"Epochs: {epochs}")
        print(f"Batch size: {batch_size}")
        print(f"Training samples: {len(train_examples)}")
        print("="*60 + "\n")
        
        output_path = './models/ats_sbert_finetuned'
        
        # Train
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            evaluator=evaluator,
            epochs=epochs,
            evaluation_steps=500,
            warmup_steps=100,
            output_path=output_path,
            save_best_model=True,
            show_progress_bar=True
        )
        
        print("\n" + "="*60)
        print("✅ Training Complete!")
        print(f"Model saved to: {output_path}")
        print("="*60)
        
        return True

def main():
    """Main training function"""
    print("\n" + "="*60)
    print("ATS SBERT Model Training Pipeline")
    print("="*60)
    
    # Check for manual dataset path
    manual_dataset_path = r"C:\Users\mdnur\Downloads\archive (2)"
    
    if os.path.exists(manual_dataset_path):
        print(f"✅ Using manual dataset from: {manual_dataset_path}")
        dataset_path = manual_dataset_path
    else:
        print("❌ Dataset not found!")
        return
    
    # Create trainer and train
    trainer = ResumeModelTrainer(dataset_path)
    success = trainer.train(epochs=3, batch_size=8)
    
    if success:
        print("\n✅ Model training completed successfully!")
        print("\nTo use the trained model:")
        print("1. Update ats_engine.py")
        print("2. Change model path from 'all-MiniLM-L6-v2' to './models/ats_sbert_finetuned'")
    else:
        print("\n❌ Training failed")

if __name__ == "__main__":
    main()

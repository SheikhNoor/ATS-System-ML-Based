"""
ATS Scoring Engine Module
Calculates match score between resume and job description.
Uses weighted scoring: Keywords (60%), Formatting (20%), Context (20%)
"""

import re
from typing import Dict, List, Tuple, Set
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from summary_analyzer import SummaryAnalyzer


class ATSEngine:
    """
    ATS Scoring Engine that analyzes resume against job role and experience level.
    Provides detailed scoring with keyword matching and recommendations.
    """

    # Role-specific keywords for different job roles
    ROLE_KEYWORDS = {
        # Software Development
        'Full Stack Developer': ['javascript', 'react', 'nodejs', 'express', 'mongodb', 'sql', 'api', 'rest', 'git', 'frontend', 'backend', 'html', 'css'],
        'Frontend Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'typescript', 'webpack', 'sass', 'responsive', 'ui', 'ux'],
        'Backend Developer': ['python', 'java', 'nodejs', 'api', 'database', 'sql', 'mongodb', 'rest', 'microservices', 'server', 'authentication'],
        'Mobile App Developer': ['android', 'ios', 'swift', 'kotlin', 'react native', 'flutter', 'mobile', 'app', 'firebase', 'api'],
        'DevOps Engineer': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'aws', 'azure', 'terraform', 'ansible', 'linux', 'monitoring', 'deployment'],
        'Software Architect': ['architecture', 'design patterns', 'scalability', 'microservices', 'cloud', 'system design', 'api', 'security', 'performance'],
        'UI/UX Developer': ['ui', 'ux', 'figma', 'sketch', 'adobe xd', 'html', 'css', 'javascript', 'prototyping', 'wireframes', 'user research'],
        
        # Data & AI
        'Data Scientist': ['python', 'r', 'machine learning', 'statistics', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'data analysis', 'visualization'],
        'Machine Learning Engineer': ['python', 'tensorflow', 'pytorch', 'keras', 'deep learning', 'neural networks', 'ml', 'algorithms', 'model training'],
        'Data Analyst': ['sql', 'excel', 'python', 'tableau', 'power bi', 'data visualization', 'statistics', 'analytics', 'reporting', 'insights'],
        'AI Engineer': ['artificial intelligence', 'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'python'],
        'Business Intelligence Analyst': ['sql', 'tableau', 'power bi', 'data warehouse', 'etl', 'analytics', 'reporting', 'dashboards', 'kpi'],
        'Data Engineer': ['python', 'sql', 'spark', 'hadoop', 'etl', 'data pipeline', 'aws', 'big data', 'airflow', 'kafka'],
        
        # Cloud & Infrastructure
        'Cloud Solutions Architect': ['aws', 'azure', 'gcp', 'cloud architecture', 'serverless', 'microservices', 'security', 'scalability', 'cost optimization'],
        'Cloud Engineer (AWS/Azure/GCP)': ['aws', 'azure', 'gcp', 'ec2', 's3', 'lambda', 'cloud', 'infrastructure', 'terraform', 'devops'],
        'Site Reliability Engineer': ['sre', 'monitoring', 'kubernetes', 'docker', 'automation', 'incident management', 'reliability', 'performance', 'linux'],
        'System Administrator': ['linux', 'windows', 'server', 'networking', 'active directory', 'scripting', 'backup', 'security', 'troubleshooting'],
        'Network Engineer': ['networking', 'tcp/ip', 'routing', 'switching', 'cisco', 'firewall', 'vpn', 'lan', 'wan', 'network security'],
        
        # Security
        'Cybersecurity Analyst': ['security', 'threat analysis', 'vulnerability', 'siem', 'incident response', 'penetration testing', 'compliance', 'firewall'],
        'Security Engineer': ['security', 'encryption', 'firewall', 'iam', 'vulnerability assessment', 'security audit', 'compliance', 'threat modeling'],
        'Penetration Tester': ['penetration testing', 'ethical hacking', 'vulnerability assessment', 'security', 'exploitation', 'owasp', 'kali linux'],
        'Information Security Manager': ['security management', 'compliance', 'risk assessment', 'security policy', 'iso 27001', 'audit', 'governance'],
        
        # Management
        'Product Manager': ['product management', 'roadmap', 'agile', 'scrum', 'stakeholder management', 'user stories', 'prioritization', 'market research'],
        'Project Manager': ['project management', 'agile', 'scrum', 'pmp', 'stakeholder management', 'risk management', 'budgeting', 'planning'],
        'Operations Manager': ['operations', 'process improvement', 'team management', 'budgeting', 'efficiency', 'strategy', 'coordination'],
        'Team Lead': ['leadership', 'team management', 'mentoring', 'communication', 'coordination', 'agile', 'decision making'],
        
        # Business
        'Business Analyst': ['business analysis', 'requirements gathering', 'stakeholder management', 'data analysis', 'process improvement', 'documentation'],
        'Financial Analyst': ['financial analysis', 'excel', 'forecasting', 'budgeting', 'financial modeling', 'reporting', 'accounting'],
        'Accountant': ['accounting', 'bookkeeping', 'gaap', 'financial statements', 'tax', 'audit', 'quickbooks', 'excel'],
        
        # Marketing
        'Digital Marketing Manager': ['digital marketing', 'seo', 'sem', 'social media', 'content marketing', 'analytics', 'campaign management', 'google ads'],
        'Content Strategist': ['content strategy', 'copywriting', 'seo', 'content marketing', 'editorial', 'social media', 'analytics'],
        'Sales Manager': ['sales', 'business development', 'crm', 'negotiation', 'team management', 'revenue growth', 'pipeline management'],
        
        # Design
        'UI/UX Designer': ['ui', 'ux', 'figma', 'sketch', 'adobe xd', 'user research', 'prototyping', 'wireframes', 'design thinking', 'usability'],
        'Product Designer': ['product design', 'ui', 'ux', 'user research', 'prototyping', 'design systems', 'figma', 'user-centered design'],
        'Graphic Designer': ['graphic design', 'adobe photoshop', 'adobe illustrator', 'typography', 'branding', 'visual design', 'creative'],
        
        # Other Tech
        'QA Engineer': ['testing', 'qa', 'automation', 'selenium', 'test cases', 'bug tracking', 'quality assurance', 'jira', 'manual testing'],
        'Technical Writer': ['technical writing', 'documentation', 'api documentation', 'user manuals', 'editing', 'content creation'],
        'Database Administrator': ['database', 'sql', 'mysql', 'postgresql', 'oracle', 'database design', 'backup', 'performance tuning', 'dba'],
    }

    # Experience-based keywords
    FRESHER_KEYWORDS = ['internship', 'project', 'coursework', 'academic', 'training', 'certification', 'learning', 'student', 'graduate']
    EXPERIENCED_KEYWORDS = ['experience', 'led', 'managed', 'delivered', 'implemented', 'architected', 'years', 'senior', 'leadership', 'mentored']

    # Formatting indicators (good resume structure)
    FORMATTING_INDICATORS = [
        'experience', 'education', 'skills', 'projects', 'certifications',
        'achievements', 'summary', 'objective', 'work history'
    ]

    def __init__(self):
        """Initialize the ATS Engine with SBERT model."""
        self.keyword_weight = 0.60  # 60%
        self.formatting_weight = 0.20  # 20%
        self.context_weight = 0.20  # 20%
        self.summary_analyzer = SummaryAnalyzer()
        
        # Load Siamese BERT (SBERT) Bi-Encoder model
        # Check if fine-tuned model exists, otherwise use base model
        import os
        model_path = './models/ats_sbert_finetuned'
        
        if os.path.exists(model_path):
            print(f"Loading fine-tuned SBERT model from {model_path}...")
            self.sbert_model = SentenceTransformer(model_path)
            print("✅ Fine-tuned SBERT model loaded successfully!")
        else:
            # all-MiniLM-L6-v2: 384-dimensional dense embeddings, optimized for semantic search
            print("⚠️ Fine-tuned model not found, using base model (all-MiniLM-L6-v2)...")
            self.sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("SBERT model loaded successfully!")

    def analyze(self, resume_text: str, job_role: str, job_category: str = "IT", experience_level: str = "Experienced") -> Dict:
        """
        Main analysis method that scores resume against job role and experience level.

        Args:
            resume_text (str): Cleaned resume text
            job_role (str): Target job role
            job_category (str): Job category ("IT" or "Non-IT")
            experience_level (str): Experience level ("Fresher" or "Experienced")

        Returns:
            Dict: Complete analysis with scores, missing keywords, and verdict
        """
        # Normalize inputs
        resume_lower = resume_text.lower()

        # Calculate individual scores
        keyword_score, keyword_details = self._calculate_keyword_score(
            resume_lower, job_role, job_category, experience_level
        )
        formatting_score = self._calculate_formatting_score(resume_lower)
        context_score = self._calculate_context_score(resume_lower, job_role, experience_level)

        # Calculate weighted total score
        total_score = (
            keyword_score * self.keyword_weight +
            formatting_score * self.formatting_weight +
            context_score * self.context_weight
        )

        # Round to 2 decimal places
        total_score = round(total_score, 2)

        # Determine verdict
        verdict = self._get_verdict(total_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            total_score, keyword_score, formatting_score, context_score, keyword_details
        )

        # Analyze summary and get suggestions
        summary_analysis = self.summary_analyzer.analyze_summary(
            resume_text, job_role, job_category, experience_level
        )

        return {
            "overall_score": total_score,
            "breakdown": {
                "keyword_score": round(keyword_score, 2),
                "formatting_score": round(formatting_score, 2),
                "context_score": round(context_score, 2)
            },
            "verdict": verdict,
            "matched_keywords": keyword_details["matched"],
            "missing_keywords": keyword_details["missing"],
            "recommendations": recommendations,
            "job_category": job_category,
            "job_role": job_role,
            "experience_level": experience_level,
            "summary_analysis": summary_analysis
        }

    def _calculate_keyword_score(
        self, resume: str, job_role: str, job_category: str, experience_level: str
    ) -> Tuple[float, Dict]:
        """
        Calculate keyword matching score (0-100).

        Args:
            resume (str): Resume text (lowercase)
            job_role (str): Target job role
            job_category (str): Job category
            experience_level (str): Experience level

        Returns:
            Tuple[float, Dict]: Score and keyword details
        """
        # Get role-specific keywords
        role_keywords = self.ROLE_KEYWORDS.get(job_role, [])
        
        # Add experience-based keywords
        if experience_level == 'Fresher':
            experience_keywords = self.FRESHER_KEYWORDS
        else:
            experience_keywords = self.EXPERIENCED_KEYWORDS
        
        # Combine all expected keywords
        all_keywords = list(set(role_keywords + experience_keywords))

        if not all_keywords:
            # Fallback: extract general keywords if role not found
            all_keywords = ['skill', 'experience', 'project', 'work']

        # Check which keywords are in resume
        matched_keywords = []
        missing_keywords = []

        for keyword in all_keywords:
            # Use word boundary matching to avoid partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, resume):
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)

        # Calculate match rate
        match_rate = len(matched_keywords) / len(all_keywords) if all_keywords else 0
        score = match_rate * 100

        keyword_details = {
            "matched": matched_keywords,
            "missing": missing_keywords,
            "match_rate": round(match_rate, 2),
            "total_keywords": len(all_keywords)
        }

        return score, keyword_details

    def _calculate_formatting_score(self, resume: str) -> float:
        """
        Calculate formatting/structure score (0-100).

        Args:
            resume (str): Resume text (lowercase)

        Returns:
            float: Formatting score
        """
        score = 0
        total_indicators = len(self.FORMATTING_INDICATORS)

        # Check for section headers
        for indicator in self.FORMATTING_INDICATORS:
            pattern = r'\b' + re.escape(indicator) + r'\b'
            if re.search(pattern, resume):
                score += 1

        # Check for email
        email_pattern = r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b'
        if re.search(email_pattern, resume):
            score += 1
            total_indicators += 1

        # Check for phone
        phone_pattern = r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}'
        if re.search(phone_pattern, resume):
            score += 1
            total_indicators += 1

        # Check for bullet points or structured content
        if '•' in resume or '-' in resume or re.search(r'\n\s*[\*\-\•]', resume):
            score += 2
            total_indicators += 2

        # Calculate percentage
        formatting_score = (score / total_indicators) * 100 if total_indicators > 0 else 50

        return min(formatting_score, 100)  # Cap at 100

    def _calculate_context_score(self, resume: str, job_role: str, experience_level: str) -> float:
        """
        Calculate contextual similarity score using TF-IDF and cosine similarity (0-100).

        Args:
            resume (str): Resume text
            job_role (str): Target job role
            experience_level (str): Experience level

        Returns:
            float: Context similarity score
        """
        try:
            # Create a synthetic job description from role and experience level
            job_text = f"{job_role} {experience_level} " + " ".join(self.ROLE_KEYWORDS.get(job_role, []))
            
            # Ensure we have at least 2 documents for comparison
            if not resume.strip() or not job_text.strip():
                return 50.0

            # Generate 384-dimensional dense embeddings using SBERT Bi-Encoder
            # all-MiniLM-L6-v2 model produces semantic embeddings optimized for similarity tasks
            try:
                # Encode texts into dense vector embeddings
                resume_embedding = self.sbert_model.encode(resume, convert_to_tensor=False)
                job_embedding = self.sbert_model.encode(job_text, convert_to_tensor=False)
                
                # Reshape for cosine similarity calculation
                resume_embedding = resume_embedding.reshape(1, -1)
                job_embedding = job_embedding.reshape(1, -1)
            except Exception as embed_error:
                print(f"Embedding error: {embed_error}")
                return 50.0

            # Calculate cosine similarity between embeddings
            # Measures the cosine of the angle between two vectors in 384-dimensional space
            similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]

            # Convert to percentage (0-100) and ensure it's a Python float
            score = float(similarity * 100)

            return round(score, 2)

        except Exception as e:
            # On any error, return a neutral score
            print(f"Error in context scoring: {e}")
            return 50.0

    def _get_verdict(self, score: float) -> str:
        """
        Determine verdict based on score.

        Args:
            score (float): Overall ATS score

        Returns:
            str: Verdict (Perfect, Good, or Weak)
        """
        if score >= 80:
            return "Perfect"
        elif score >= 60:
            return "Good"
        else:
            return "Weak"

    def _generate_recommendations(
        self,
        total_score: float,
        keyword_score: float,
        formatting_score: float,
        context_score: float,
        keyword_details: Dict
    ) -> List[str]:
        """
        Generate actionable recommendations based on scores.

        Args:
            total_score (float): Overall score
            keyword_score (float): Keyword matching score
            formatting_score (float): Formatting score
            context_score (float): Context similarity score
            keyword_details (Dict): Keyword matching details

        Returns:
            List[str]: List of recommendations
        """
        recommendations = []

        # Keyword recommendations
        if keyword_score < 60:
            recommendations.append(
                f"Low keyword match ({keyword_score:.0f}%). Add more relevant keywords from the job description."
            )
            if keyword_details["missing"]:
                missing_count = min(5, len(keyword_details["missing"]))
                top_missing = keyword_details["missing"][:missing_count]
                recommendations.append(
                    f"Missing key terms: {', '.join(top_missing)}"
                )

        # Formatting recommendations
        if formatting_score < 70:
            recommendations.append(
                "Improve resume structure. Include clear sections: Experience, Education, Skills, Projects."
            )
            recommendations.append(
                "Use bullet points to highlight achievements and responsibilities."
            )

        # Context recommendations
        if context_score < 60:
            recommendations.append(
                "Tailor your resume content to better match the job description. Use similar terminology and phrasing."
            )

        # Overall recommendations
        if total_score >= 80:
            recommendations.append(
                "Excellent match! Your resume aligns well with the job requirements."
            )
        elif total_score >= 60:
            recommendations.append(
                "Good foundation. Make the suggested improvements to increase your chances."
            )
        else:
            recommendations.append(
                "Significant improvements needed. Focus on adding relevant keywords and improving structure."
            )

        return recommendations

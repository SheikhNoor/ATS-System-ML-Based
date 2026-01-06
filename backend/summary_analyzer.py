"""
Summary Analyzer Module
Analyzes resume summaries and provides AI-powered suggestions for improvement.
"""

import re
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class SummaryAnalyzer:
    """
    Analyzes resume summaries and provides intelligent suggestions.
    """

    # Strong action words for summaries
    STRONG_ACTION_WORDS = [
        'led', 'managed', 'developed', 'created', 'implemented', 'designed',
        'architected', 'optimized', 'improved', 'increased', 'reduced',
        'delivered', 'launched', 'established', 'drove', 'spearheaded',
        'executed', 'coordinated', 'facilitated', 'achieved', 'accomplished'
    ]

    # Weak words to avoid
    WEAK_WORDS = [
        'responsible for', 'worked on', 'helped with', 'assisted in',
        'participated in', 'involved in', 'tasked with', 'tried to'
    ]

    # Professional buzzwords by category
    PROFESSIONAL_TERMS = {
        'IT': [
            'full-stack', 'scalable', 'cloud-native', 'agile', 'devops',
            'microservices', 'api', 'automation', 'ci/cd', 'architecture'
        ],
        'Non-IT': [
            'strategic', 'cross-functional', 'stakeholder', 'analytical',
            'results-driven', 'customer-focused', 'data-driven', 'leadership'
        ]
    }

    def __init__(self):
        """Initialize the Summary Analyzer."""
        pass

    def analyze_summary(
        self,
        resume_text: str,
        job_role: str,
        job_category: str,
        experience_level: str
    ) -> Dict:
        """
        Analyze the resume summary and provide suggestions.

        Args:
            resume_text: Full resume text
            job_role: Target job role
            job_category: IT or Non-IT
            experience_level: Fresher or Experienced

        Returns:
            Dict with analysis results and suggestions
        """
        # Extract summary section
        summary_text = self._extract_summary(resume_text)

        if not summary_text:
            return {
                "has_summary": False,
                "score": 0,
                "quality": "Missing",
                "suggestions": [
                    "❌ No summary/objective section found",
                    "✓ Add a professional summary at the top of your resume",
                    "✓ Keep it 3-5 sentences highlighting your key strengths",
                    f"✓ Mention '{job_role}' explicitly to show role alignment"
                ],
                "analysis": {
                    "length": 0,
                    "has_action_words": False,
                    "has_numbers": False,
                    "role_mentioned": False
                }
            }

        # Perform detailed analysis
        analysis = self._analyze_summary_content(
            summary_text, job_role, job_category, experience_level
        )

        # Calculate overall score
        score = self._calculate_summary_score(analysis, experience_level)

        # Generate suggestions
        suggestions = self._generate_suggestions(
            analysis, job_role, job_category, experience_level, summary_text
        )

        # Determine quality rating
        quality = self._get_quality_rating(score)

        return {
            "has_summary": True,
            "summary_text": summary_text,
            "score": score,
            "quality": quality,
            "suggestions": suggestions,
            "analysis": analysis,
            "improved_example": self._generate_improved_example(
                summary_text, job_role, job_category, experience_level, analysis
            )
        }

    def _extract_summary(self, resume_text: str) -> str:
        """
        Extract the summary/objective section from resume.

        Args:
            resume_text: Full resume text

        Returns:
            Extracted summary text
        """
        text_lower = resume_text.lower()

        # Common summary section headers
        summary_patterns = [
            r'(?:professional\s+)?summary\s*[:\-]?\s*(.*?)(?=\n\s*[A-Z\-]{2,}|\n\s*education|\n\s*experience|\n\s*skills|$)',
            r'(?:career\s+)?objective\s*[:\-]?\s*(.*?)(?=\n\s*[A-Z\-]{2,}|\n\s*education|\n\s*experience|\n\s*skills|$)',
            r'profile\s*[:\-]?\s*(.*?)(?=\n\s*[A-Z\-]{2,}|\n\s*education|\n\s*experience|\n\s*skills|$)',
            r'about\s+me\s*[:\-]?\s*(.*?)(?=\n\s*[A-Z\-]{2,}|\n\s*education|\n\s*experience|\n\s*skills|$)'
        ]

        for pattern in summary_patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                summary = match.group(1).strip()
                # Get the actual text (not lowercased)
                start_idx = match.start(1)
                end_idx = match.end(1)
                return resume_text[start_idx:end_idx].strip()

        return ""

    def _analyze_summary_content(
        self,
        summary_text: str,
        job_role: str,
        job_category: str,
        experience_level: str
    ) -> Dict:
        """
        Analyze the content of the summary.

        Args:
            summary_text: The summary text
            job_role: Target job role
            job_category: IT or Non-IT
            experience_level: Fresher or Experienced

        Returns:
            Dictionary with analysis metrics
        """
        summary_lower = summary_text.lower()
        words = summary_text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', summary_text) if s.strip()]

        # Check for action words
        action_words_found = [
            word for word in self.STRONG_ACTION_WORDS
            if word in summary_lower
        ]

        # Check for weak words
        weak_words_found = [
            phrase for phrase in self.WEAK_WORDS
            if phrase in summary_lower
        ]

        # Check for numbers/metrics
        numbers_found = re.findall(r'\d+\+?', summary_text)

        # Check for role mention
        role_mentioned = job_role.lower() in summary_lower

        # Check for professional terms
        prof_terms = self.PROFESSIONAL_TERMS.get(job_category, [])
        prof_terms_found = [
            term for term in prof_terms
            if term in summary_lower
        ]

        # Check for years of experience mention
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience'
        years_match = re.search(years_pattern, summary_lower)

        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "action_words": action_words_found,
            "weak_words": weak_words_found,
            "numbers": numbers_found,
            "role_mentioned": role_mentioned,
            "professional_terms": prof_terms_found,
            "has_action_words": len(action_words_found) > 0,
            "has_weak_words": len(weak_words_found) > 0,
            "has_numbers": len(numbers_found) > 0,
            "has_years_mentioned": years_match is not None,
            "length_category": self._get_length_category(len(words))
        }

    def _get_length_category(self, word_count: int) -> str:
        """Categorize summary length."""
        if word_count < 30:
            return "Too Short"
        elif word_count <= 80:
            return "Good"
        elif word_count <= 120:
            return "Acceptable"
        else:
            return "Too Long"

    def _calculate_summary_score(self, analysis: Dict, experience_level: str) -> float:
        """
        Calculate a score for the summary quality (0-100).

        Args:
            analysis: Analysis results
            experience_level: Fresher or Experienced

        Returns:
            Score out of 100
        """
        score = 0

        # Length score (20 points)
        if analysis["length_category"] == "Good":
            score += 20
        elif analysis["length_category"] == "Acceptable":
            score += 15
        elif analysis["length_category"] == "Too Short":
            score += 5
        else:  # Too Long
            score += 10

        # Action words (20 points)
        if len(analysis["action_words"]) >= 3:
            score += 20
        elif len(analysis["action_words"]) >= 2:
            score += 15
        elif len(analysis["action_words"]) >= 1:
            score += 10

        # Professional terms (15 points)
        if len(analysis["professional_terms"]) >= 2:
            score += 15
        elif len(analysis["professional_terms"]) >= 1:
            score += 10

        # Role mention (15 points)
        if analysis["role_mentioned"]:
            score += 15

        # Numbers/metrics (15 points)
        if len(analysis["numbers"]) >= 2:
            score += 15
        elif len(analysis["numbers"]) >= 1:
            score += 10

        # Years of experience for experienced candidates (10 points)
        if experience_level == "Experienced":
            if analysis["has_years_mentioned"]:
                score += 10
        else:
            score += 10  # Freshers get this automatically

        # Penalty for weak words (up to -10 points)
        score -= min(len(analysis["weak_words"]) * 5, 10)

        # Ensure score is between 0 and 100
        return max(0, min(100, score))

    def _get_quality_rating(self, score: float) -> str:
        """Convert score to quality rating."""
        if score >= 80:
            return "Excellent"
        elif score >= 65:
            return "Good"
        elif score >= 50:
            return "Needs Improvement"
        else:
            return "Poor"

    def _generate_suggestions(
        self,
        analysis: Dict,
        job_role: str,
        job_category: str,
        experience_level: str,
        summary_text: str
    ) -> List[str]:
        """
        Generate actionable suggestions for improvement.

        Args:
            analysis: Analysis results
            job_role: Target job role
            job_category: IT or Non-IT
            experience_level: Fresher or Experienced
            summary_text: Original summary text

        Returns:
            List of suggestions
        """
        suggestions = []

        # Length suggestions
        if analysis["length_category"] == "Too Short":
            suggestions.append(
                f"⚠️ Summary is too brief ({analysis['word_count']} words). "
                "Expand to 50-80 words for better impact"
            )
        elif analysis["length_category"] == "Too Long":
            suggestions.append(
                f"⚠️ Summary is too long ({analysis['word_count']} words). "
                "Condense to 50-80 words for better readability"
            )

        # Action words suggestions
        if len(analysis["action_words"]) < 2:
            suggestions.append(
                "✓ Add strong action words like: " +
                ", ".join(self.STRONG_ACTION_WORDS[:5])
            )

        # Weak words warning
        if analysis["has_weak_words"]:
            suggestions.append(
                f"❌ Avoid weak phrases: {', '.join(analysis['weak_words'][:3])}. "
                "Use stronger action verbs instead"
            )

        # Role mention
        if not analysis["role_mentioned"]:
            suggestions.append(
                f"✓ Explicitly mention '{job_role}' to show clear role alignment"
            )

        # Numbers/metrics
        if not analysis["has_numbers"]:
            suggestions.append(
                "✓ Add quantifiable achievements (e.g., '5+ years', '10+ projects')"
            )

        # Professional terms
        if len(analysis["professional_terms"]) < 2:
            prof_terms = self.PROFESSIONAL_TERMS.get(job_category, [])
            suggestions.append(
                f"✓ Include industry terms: {', '.join(prof_terms[:5])}"
            )

        # Experience level specific
        if experience_level == "Experienced" and not analysis["has_years_mentioned"]:
            suggestions.append(
                "✓ Mention years of experience (e.g., '5+ years of experience in...')"
            )

        # General best practices
        if analysis["sentence_count"] < 2:
            suggestions.append(
                "✓ Use 3-4 sentences for better structure and flow"
            )

        return suggestions if suggestions else ["✅ Your summary looks great!"]

    def _generate_improved_example(
        self,
        original_summary: str,
        job_role: str,
        job_category: str,
        experience_level: str,
        analysis: Dict
    ) -> str:
        """
        Generate an improved version of the summary.

        Args:
            original_summary: Original summary text
            job_role: Target job role
            job_category: IT or Non-IT
            experience_level: Fresher or Experienced
            analysis: Analysis results

        Returns:
            Improved summary example
        """
        # This is a template-based improvement
        # In production, this could use a more sophisticated NLP model

        if experience_level == "Experienced":
            template = (
                f"Results-driven {job_role} with 5+ years of experience in "
                f"{job_category.lower()} industry. Proven track record of "
                f"delivering high-impact projects and leading cross-functional teams. "
                f"Expertise in modern technologies and agile methodologies, "
                f"with strong focus on scalable solutions and continuous improvement."
            )
        else:
            template = (
                f"Motivated and detail-oriented {job_role} with strong foundation "
                f"in {job_category.lower()} concepts. Successfully completed multiple "
                f"academic and personal projects demonstrating proficiency in "
                f"modern technologies. Eager to contribute technical skills and "
                f"fresh perspectives to innovative development teams."
            )

        return template


def train_summary_model(training_data: List[Dict]) -> Dict:
    """
    Train the summary evaluation model on sample data.
    This is a placeholder for future ML model training.

    Args:
        training_data: List of training examples with summaries and scores

    Returns:
        Model metrics
    """
    # Placeholder for future implementation
    # Could use classification models, LLMs, or transformer-based approaches
    return {
        "status": "Model training not yet implemented",
        "samples": len(training_data) if training_data else 0
    }

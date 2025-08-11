"""
Comprehensive Citation and Reference Management System
Author: Academic Research Assistant
Date: 2025-08-11

A robust citation management tool supporting multiple academic citation formats
with features for format conversion, validation, and bibliography generation.
"""

import re
import csv
import json
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import unicodedata


class CitationManager:
    """Main class for managing citations and references."""
    
    def __init__(self):
        self.reference_database = []
        self.supported_formats = ['apa', 'vancouver', 'mla', 'chicago', 'ieee']
        
    def load_references_from_csv(self, filepath: str) -> bool:
        """Load references from CSV file."""
        try:
            df = pd.read_csv(filepath)
            self.reference_database = df.to_dict('records')
            return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False
    
    def load_references_from_json(self, filepath: str) -> bool:
        """Load references from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.reference_database = json.load(file)
            return True
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return False
    
    def save_references_to_csv(self, filepath: str) -> bool:
        """Save references to CSV file."""
        try:
            if not self.reference_database:
                print("No references to save.")
                return False
            
            df = pd.DataFrame(self.reference_database)
            df.to_csv(filepath, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return False
    
    def format_authors_apa(self, authors: str) -> str:
        """Format authors for APA style."""
        if not authors:
            return ""
        
        author_list = [name.strip() for name in authors.split(',')]
        if len(author_list) == 1:
            return self._format_single_author_apa(author_list[0])
        elif len(author_list) == 2:
            return f"{self._format_single_author_apa(author_list[0])}, & {self._format_single_author_apa(author_list[1])}"
        else:
            formatted_authors = [self._format_single_author_apa(name) for name in author_list[:-1]]
            return ", ".join(formatted_authors) + f", & {self._format_single_author_apa(author_list[-1])}"
    
    def _format_single_author_apa(self, name: str) -> str:
        """Format single author name for APA style (Last, F. M.)."""
        parts = name.strip().split()
        if len(parts) < 2:
            return name
        
        last_name = parts[-1]
        first_names = parts[:-1]
        initials = ". ".join([n[0].upper() for n in first_names if n]) + "."
        return f"{last_name}, {initials}"
    
    def format_authors_vancouver(self, authors: str) -> str:
        """Format authors for Vancouver style."""
        if not authors:
            return ""
        
        author_list = [name.strip() for name in authors.split(',')]
        formatted_authors = []
        
        for name in author_list:
            parts = name.strip().split()
            if len(parts) >= 2:
                last_name = parts[-1]
                initials = "".join([n[0].upper() for n in parts[:-1] if n])
                formatted_authors.append(f"{last_name} {initials}")
            else:
                formatted_authors.append(name)
        
        return ", ".join(formatted_authors)
    
    def format_authors_mla(self, authors: str) -> str:
        """Format authors for MLA style."""
        if not authors:
            return ""
        
        author_list = [name.strip() for name in authors.split(',')]
        if len(author_list) == 1:
            parts = author_list[0].strip().split()
            if len(parts) >= 2:
                return f"{parts[-1]}, {' '.join(parts[:-1])}"
            return author_list[0]
        else:
            # First author: Last, First. Subsequent authors: First Last
            first_author = author_list[0].strip().split()
            if len(first_author) >= 2:
                formatted_first = f"{first_author[-1]}, {' '.join(first_author[:-1])}"
            else:
                formatted_first = author_list[0]
            
            other_authors = [name.strip() for name in author_list[1:]]
            return formatted_first + ", and " + ", and ".join(other_authors)
    
    def generate_apa_citation(self, reference: Dict) -> str:
        """Generate APA format citation."""
        citation_parts = []
        
        # Authors
        if reference.get('authors'):
            authors = self.format_authors_apa(reference['authors'])
            citation_parts.append(authors)
        
        # Year
        if reference.get('year'):
            citation_parts.append(f"({reference['year']})")
        
        # Title
        if reference.get('title'):
            title = reference['title']
            if not title.endswith('.'):
                title += '.'
            citation_parts.append(title)
        
        # Journal and publication details
        if reference.get('journal'):
            journal_part = f"*{reference['journal']}*"
            
            # Volume and issue
            if reference.get('volume'):
                journal_part += f", *{reference['volume']}*"
                if reference.get('issue'):
                    journal_part += f"({reference['issue']})"
            
            # Pages
            if reference.get('pages'):
                journal_part += f", {reference['pages']}"
            
            citation_parts.append(journal_part + ".")
        
        # DOI or URL
        if reference.get('doi'):
            citation_parts.append(f"https://doi.org/{reference['doi']}")
        elif reference.get('url'):
            citation_parts.append(reference['url'])
        
        return " ".join(citation_parts)
    
    def generate_vancouver_citation(self, reference: Dict, citation_number: int) -> str:
        """Generate Vancouver format citation."""
        citation_parts = []
        
        # Authors
        if reference.get('authors'):
            authors = self.format_authors_vancouver(reference['authors'])
            citation_parts.append(authors + ".")
        
        # Title
        if reference.get('title'):
            title = reference['title']
            if not title.endswith('.'):
                title += '.'
            citation_parts.append(title)
        
        # Journal
        if reference.get('journal'):
            journal_name = reference['journal']
            # Abbreviate common journal names (basic implementation)
            journal_abbrev = self._abbreviate_journal_vancouver(journal_name)
            citation_parts.append(journal_abbrev + ".")
        
        # Year, Volume, Issue, Pages
        pub_details = []
        if reference.get('year'):
            pub_details.append(str(reference['year']))
        
        if reference.get('volume'):
            volume_part = str(reference['volume'])
            if reference.get('issue'):
                volume_part += f"({reference['issue']})"
            pub_details.append(volume_part)
        
        if reference.get('pages'):
            pub_details.append(f":{reference['pages']}")
        
        if pub_details:
            citation_parts.append("".join(pub_details) + ".")
        
        # Add citation number at the beginning
        return f"{citation_number}. " + " ".join(citation_parts)
    
    def _abbreviate_journal_vancouver(self, journal_name: str) -> str:
        """Basic journal name abbreviation for Vancouver style."""
        # This is a simplified version - in practice, you'd use official abbreviations
        abbreviations = {
            "Journal of the American College of Cardiology": "J Am Coll Cardiol",
            "New England Journal of Medicine": "N Engl J Med",
            "The Lancet": "Lancet",
            "Nature": "Nature",
            "Science": "Science",
            "PLOS ONE": "PLoS One",
            "IEEE Transactions": "IEEE Trans"
        }
        return abbreviations.get(journal_name, journal_name)
    
    def generate_mla_citation(self, reference: Dict) -> str:
        """Generate MLA format citation."""
        citation_parts = []
        
        # Authors
        if reference.get('authors'):
            authors = self.format_authors_mla(reference['authors'])
            citation_parts.append(authors + ".")
        
        # Title (in quotes for articles)
        if reference.get('title'):
            title = f'"{reference["title"]}"'
            citation_parts.append(title)
        
        # Container (Journal)
        if reference.get('journal'):
            citation_parts.append(f"*{reference['journal']}*,")
        
        # Volume and issue
        if reference.get('volume'):
            vol_part = f"vol. {reference['volume']}"
            if reference.get('issue'):
                vol_part += f", no. {reference['issue']}"
            citation_parts.append(vol_part + ",")
        
        # Date
        if reference.get('year'):
            citation_parts.append(f"{reference['year']},")
        
        # Pages
        if reference.get('pages'):
            pages = reference['pages'].replace('-', '-')  # En dash
            citation_parts.append(f"pp. {pages}.")
        
        return " ".join(citation_parts)
    
    def generate_chicago_citation(self, reference: Dict) -> str:
        """Generate Chicago format citation (Notes-Bibliography)."""
        citation_parts = []
        
        # Authors (different format for Chicago)
        if reference.get('authors'):
            author_list = [name.strip() for name in reference['authors'].split(',')]
            if len(author_list) == 1:
                citation_parts.append(author_list[0].strip())
            else:
                citation_parts.append(", ".join(author_list))
        
        # Title
        if reference.get('title'):
            title = f'"{reference["title"]}"'
            citation_parts.append(title)
        
        # Journal
        if reference.get('journal'):
            citation_parts.append(f"*{reference['journal']}*")
        
        # Volume and issue
        if reference.get('volume'):
            vol_part = str(reference['volume'])
            if reference.get('issue'):
                vol_part += f", no. {reference['issue']}"
            citation_parts.append(vol_part)
        
        # Date and pages
        date_page = []
        if reference.get('year'):
            date_page.append(f"({reference['year']})")
        if reference.get('pages'):
            date_page.append(f": {reference['pages']}")
        
        if date_page:
            citation_parts.append("".join(date_page) + ".")
        
        return " ".join(citation_parts)
    
    def generate_ieee_citation(self, reference: Dict, citation_number: int) -> str:
        """Generate IEEE format citation."""
        citation_parts = []
        
        # Authors (initials first)
        if reference.get('authors'):
            author_list = [name.strip() for name in reference['authors'].split(',')]
            ieee_authors = []
            for name in author_list:
                parts = name.strip().split()
                if len(parts) >= 2:
                    first_initials = ". ".join([n[0].upper() for n in parts[:-1]]) + "."
                    ieee_authors.append(f"{first_initials} {parts[-1]}")
                else:
                    ieee_authors.append(name)
            citation_parts.append(", ".join(ieee_authors) + ",")
        
        # Title
        if reference.get('title'):
            title = f'"{reference["title"]},"'
            citation_parts.append(title)
        
        # Journal (italicized)
        if reference.get('journal'):
            citation_parts.append(f"*{reference['journal']}*,")
        
        # Volume, issue, pages, year
        pub_info = []
        if reference.get('volume'):
            pub_info.append(f"vol. {reference['volume']}")
        if reference.get('issue'):
            pub_info.append(f"no. {reference['issue']}")
        if reference.get('pages'):
            pub_info.append(f"pp. {reference['pages']}")
        if reference.get('year'):
            pub_info.append(str(reference['year']))
        
        if pub_info:
            citation_parts.append(", ".join(pub_info) + ".")
        
        return f"[{citation_number}] " + " ".join(citation_parts)
    
    def format_citation(self, reference: Dict, style: str, citation_number: int = 1) -> str:
        """Format a single citation in the specified style."""
        style = style.lower()
        
        if style == 'apa':
            return self.generate_apa_citation(reference)
        elif style == 'vancouver':
            return self.generate_vancouver_citation(reference, citation_number)
        elif style == 'mla':
            return self.generate_mla_citation(reference)
        elif style == 'chicago':
            return self.generate_chicago_citation(reference)
        elif style == 'ieee':
            return self.generate_ieee_citation(reference, citation_number)
        else:
            raise ValueError(f"Unsupported citation style: {style}")
    
    def generate_bibliography(self, style: str, sort_alphabetical: bool = True) -> List[str]:
        """Generate complete bibliography in specified format."""
        if not self.reference_database:
            return []
        
        citations = []
        references = self.reference_database.copy()
        
        # Sort references
        if sort_alphabetical and style.lower() in ['apa', 'mla', 'chicago']:
            references.sort(key=lambda x: x.get('authors', '').split(',')[0].strip())
        
        # Generate citations
        for i, ref in enumerate(references, 1):
            try:
                citation = self.format_citation(ref, style, i)
                citations.append(citation)
            except Exception as e:
                print(f"Error formatting reference {i}: {e}")
                continue
        
        return citations
    
    def convert_citation_format(self, citation_text: str, from_style: str, to_style: str) -> str:
        """Convert citation from one format to another."""
        # This is a simplified implementation
        # In practice, this would require sophisticated parsing
        parsed_ref = self.parse_citation(citation_text, from_style)
        if parsed_ref:
            return self.format_citation(parsed_ref, to_style)
        else:
            return "Error: Could not parse citation"
    
    def parse_citation(self, citation_text: str, style: str) -> Optional[Dict]:
        """Parse citation text to extract components."""
        # Simplified parsing - would need more sophisticated regex patterns
        parsed = {}
        
        # Basic patterns for different elements
        doi_pattern = r'(?:https?://)?(?:dx\.)?doi\.org/([^\s]+)'
        year_pattern = r'\b(19|20)\d{2}\b'
        
        # Extract DOI
        doi_match = re.search(doi_pattern, citation_text)
        if doi_match:
            parsed['doi'] = doi_match.group(1)
        
        # Extract year
        year_match = re.search(year_pattern, citation_text)
        if year_match:
            parsed['year'] = year_match.group()
        
        # This would need much more sophisticated parsing for each style
        return parsed if parsed else None
    
    def extract_citations_from_text(self, text: str) -> List[str]:
        """Extract citation references from text."""
        citations = []
        
        # Pattern for numbered citations [1], [2], etc.
        numbered_pattern = r'\[(\d+(?:,\s*\d+)*(?:-\d+)?)\]'
        numbered_matches = re.findall(numbered_pattern, text)
        citations.extend([f"[{match}]" for match in numbered_matches])
        
        # Pattern for author-year citations (Smith, 2020)
        author_year_pattern = r'\([A-Za-z]+(?:\s+(?:et\s+al\.?|&\s+[A-Za-z]+))?,\s*\d{4}[a-z]?\)'
        author_year_matches = re.findall(author_year_pattern, text)
        citations.extend(author_year_matches)
        
        return list(set(citations))  # Remove duplicates
    
    def check_duplicate_references(self) -> List[Tuple[int, int]]:
        """Check for duplicate references in the database."""
        duplicates = []
        
        for i in range(len(self.reference_database)):
            for j in range(i + 1, len(self.reference_database)):
                ref1 = self.reference_database[i]
                ref2 = self.reference_database[j]
                
                # Check for duplicates based on title and DOI
                if (ref1.get('title') and ref2.get('title') and 
                    ref1['title'].lower().strip() == ref2['title'].lower().strip()):
                    duplicates.append((i, j))
                elif (ref1.get('doi') and ref2.get('doi') and 
                      ref1['doi'] == ref2['doi']):
                    duplicates.append((i, j))
        
        return duplicates
    
    def validate_doi(self, doi: str) -> bool:
        """Validate DOI by checking if it resolves."""
        try:
            if not doi:
                return False
            
            # Clean DOI
            doi = doi.strip()
            if doi.startswith('http'):
                doi = doi.split('doi.org/')[-1]
            
            # Basic DOI format check
            doi_pattern = r'^10\.\d+/.+'
            if not re.match(doi_pattern, doi):
                return False
            
            # Try to resolve DOI (optional - requires internet)
            try:
                response = requests.head(f'https://doi.org/{doi}', timeout=5)
                return response.status_code == 200
            except:
                # If internet check fails, just validate format
                return True
                
        except Exception:
            return False
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format and accessibility."""
        try:
            if not url:
                return False
            
            # Basic URL format check
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Try to access URL (optional)
            try:
                response = requests.head(url, timeout=5)
                return response.status_code == 200
            except:
                # If internet check fails, just validate format
                return True
                
        except Exception:
            return False
    
    def validate_references(self) -> Dict:
        """Validate all references in the database."""
        validation_results = {
            'total_references': len(self.reference_database),
            'valid_dois': 0,
            'invalid_dois': 0,
            'valid_urls': 0,
            'invalid_urls': 0,
            'missing_fields': [],
            'duplicates': []
        }
        
        required_fields = ['authors', 'title', 'year']
        
        for i, ref in enumerate(self.reference_database):
            # Check required fields
            missing = [field for field in required_fields if not ref.get(field)]
            if missing:
                validation_results['missing_fields'].append({
                    'reference_index': i,
                    'missing': missing,
                    'title': ref.get('title', 'No title')
                })
            
            # Validate DOI
            if ref.get('doi'):
                if self.validate_doi(ref['doi']):
                    validation_results['valid_dois'] += 1
                else:
                    validation_results['invalid_dois'] += 1
            
            # Validate URL
            if ref.get('url'):
                if self.validate_url(ref['url']):
                    validation_results['valid_urls'] += 1
                else:
                    validation_results['invalid_urls'] += 1
        
        # Check for duplicates
        validation_results['duplicates'] = self.check_duplicate_references()
        
        return validation_results
    
    def export_bibliography_to_file(self, filepath: str, style: str, format_type: str = 'text') -> bool:
        """Export bibliography to file."""
        try:
            bibliography = self.generate_bibliography(style)
            
            if format_type.lower() == 'text':
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(f"Bibliography - {style.upper()} Format\n")
                    file.write("=" * 50 + "\n\n")
                    for citation in bibliography:
                        file.write(citation + "\n\n")
            
            elif format_type.lower() == 'html':
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write("<html><head><title>Bibliography</title></head><body>\n")
                    file.write(f"<h1>Bibliography - {style.upper()} Format</h1>\n<ol>\n")
                    for citation in bibliography:
                        file.write(f"<li>{citation}</li>\n")
                    file.write("</ol></body></html>")
            
            return True
        except Exception as e:
            print(f"Error exporting bibliography: {e}")
            return False


def main():
    """Example usage of the CitationManager."""
    manager = CitationManager()
    
    # Example reference data
    sample_references = [
        {
            'authors': 'Smith, John A., Johnson, Mary B.',
            'title': 'Machine Learning Applications in Medical Imaging',
            'journal': 'Journal of Medical AI',
            'year': '2023',
            'volume': '15',
            'issue': '3',
            'pages': '245-260',
            'doi': '10.1000/182',
            'abstract': 'This study explores the application of machine learning...',
            'keywords': 'machine learning, medical imaging, AI',
            'notes': 'Important paper for methodology',
            'citation_count': '45',
            'read_status': 'Read'
        },
        {
            'authors': 'Brown, Sarah C.',
            'title': 'Deep Learning for Cardiac Image Analysis',
            'journal': 'Cardiology Research',
            'year': '2024',
            'volume': '28',
            'issue': '2',
            'pages': '112-128',
            'doi': '10.1000/183',
            'url': 'https://example.com/paper2',
            'abstract': 'A comprehensive review of deep learning methods...',
            'keywords': 'deep learning, cardiology, image analysis',
            'notes': 'Good review paper',
            'citation_count': '23',
            'read_status': 'To Read'
        }
    ]
    
    manager.reference_database = sample_references
    
    # Generate citations in different formats
    print("APA Format:")
    apa_citations = manager.generate_bibliography('apa')
    for citation in apa_citations:
        print(citation)
    
    print("\nVancouver Format:")
    vancouver_citations = manager.generate_bibliography('vancouver')
    for citation in vancouver_citations:
        print(citation)
    
    print("\nMLA Format:")
    mla_citations = manager.generate_bibliography('mla')
    for citation in mla_citations:
        print(citation)
    
    # Validate references
    print("\nValidation Results:")
    validation = manager.validate_references()
    print(f"Total references: {validation['total_references']}")
    print(f"Valid DOIs: {validation['valid_dois']}")
    print(f"Invalid DOIs: {validation['invalid_dois']}")
    print(f"Duplicates found: {len(validation['duplicates'])}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Filmhub Electronic Press Kit (EPK) Generator
Production-ready version with consistent, high-quality output
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass

# PDF generation
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Image processing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of asset validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class EPKGenerator:
    """Production EPK Generator with consistent output"""
    
    # Output templates for consistency
    GENRE_COLORS = {
        'horror': {'primary': '#8B0000', 'secondary': '#2C2C2C', 'accent': '#FF4444'},
        'sci-fi': {'primary': '#1E3A8A', 'secondary': '#0F172A', 'accent': '#60A5FA'},
        'fantasy': {'primary': '#7C3AED', 'secondary': '#1E1B4B', 'accent': '#A78BFA'},
        'comedy': {'primary': '#F59E0B', 'secondary': '#78350F', 'accent': '#FBBF24'},
        'drama': {'primary': '#374151', 'secondary': '#1F2937', 'accent': '#9CA3AF'},
        'action': {'primary': '#DC2626', 'secondary': '#18181B', 'accent': '#EF4444'},
        'documentary': {'primary': '#059669', 'secondary': '#064E3B', 'accent': '#10B981'},
        'romance': {'primary': '#DB2777', 'secondary': '#831843', 'accent': '#F472B6'},
        'thriller': {'primary': '#4B5563', 'secondary': '#111827', 'accent': '#6B7280'},
    }
    
    DEFAULT_COLORS = {'primary': '#2563EB', 'secondary': '#1E293B', 'accent': '#3B82F6'}
    
    def __init__(self, project_dir: str, optimize_images: bool = True):
        self.project_dir = Path(project_dir)
        self.config = {}
        self.assets_dir = self.project_dir / "assets"
        self.output_dir = self.project_dir / "output"
        self.optimize_images = optimize_images and PIL_AVAILABLE
        
    def setup_project_structure(self):
        """Create standardized folder structure"""
        folders = [
            "assets/images/posters",
            "assets/images/stills",
            "assets/images/cast",
            "assets/images/crew",
            "assets/images/logos",
            "assets/videos",
            "assets/downloads",
            "output/html",
            "output/pdf"
        ]
        
        for folder in folders:
            (self.project_dir / folder).mkdir(parents=True, exist_ok=True)
            
        logger.info(f"✅ Project structure created: {self.project_dir.name}")
        
    def load_config(self, config_file: str) -> Dict:
        """Load and validate film configuration"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        logger.info(f"✅ Configuration loaded: {self.config.get('metadata', {}).get('title', 'Unknown')}")
        return self.config
    
    def validate_assets(self) -> ValidationResult:
        """
        Comprehensive asset validation
        Returns ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        meta = self.config.get('metadata', {})
        
        # Required metadata fields
        required_fields = {
            'title': 'Film title',
            'logline': 'Logline',
            'synopsis': 'Synopsis',
            'genre': 'Genre',
            'runtime': 'Runtime'
        }
        
        for field, label in required_fields.items():
            if not meta.get(field):
                errors.append(f"Missing required field: {label}")
        
        # Validate poster
        poster_dir = self.assets_dir / "images" / "posters"
        if not poster_dir.exists() or not list(poster_dir.glob("*.[jp][pn][g]")):
            errors.append("Poster image required (JPG or PNG)")
        elif PIL_AVAILABLE:
            poster_files = list(poster_dir.glob("*.[jp][pn][g]"))
            if poster_files:
                try:
                    img = Image.open(poster_files[0])
                    if img.width < 1000 or img.height < 1500:
                        warnings.append(f"Poster resolution low ({img.width}x{img.height}px). Recommended: 2000x3000px")
                except Exception as e:
                    warnings.append(f"Could not validate poster: {e}")
        
        # Validate stills
        stills_dir = self.assets_dir / "images" / "stills"
        if stills_dir.exists():
            stills = list(stills_dir.glob("*.[jp][pn][g]"))
            if len(stills) < 8:
                warnings.append(f"Only {len(stills)} stills found. Recommended: 8-12")
            
            # Check still dimensions
            if PIL_AVAILABLE and stills:
                for still in stills[:3]:  # Check first 3
                    try:
                        img = Image.open(still)
                        if img.width < 1280:
                            warnings.append(f"Still '{still.name}' resolution low. Recommended: 1920x1080px")
                            break
                    except:
                        pass
        else:
            warnings.append("No production stills folder found")
        
        # Validate contact info
        contact = self.config.get('contact', {})
        if not contact.get('email'):
            errors.append("Contact email required")
        
        # Check synopsis length
        synopsis = meta.get('synopsis', '')
        if synopsis and len(synopsis) < 200:
            warnings.append(f"Synopsis is short ({len(synopsis)} chars). Recommended: 200-400 words")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(is_valid, errors, warnings)
    
    def optimize_image(self, image_path: Path, max_width: int = 1920) -> Path:
        """Optimize image for web"""
        if not PIL_AVAILABLE or not self.optimize_images or not image_path.exists():
            return image_path
        
        try:
            img = Image.open(image_path)
            
            # Skip if already optimized
            if img.width <= max_width:
                return image_path
            
            # Calculate new dimensions
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert RGBA to RGB
            if img.mode == 'RGBA':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            
            # Save optimized
            optimized_path = image_path.parent / f"opt_{image_path.name}"
            img.save(optimized_path, 'JPEG', quality=85, optimize=True)
            
            return optimized_path
        except Exception as e:
            logger.warning(f"Could not optimize {image_path.name}: {e}")
            return image_path
    
    def generate_html(self, output_name: str = "index.html", for_pdf: bool = False) -> Path:
        """Generate consistent HTML EPK"""
        config = self.config
        meta = config.get('metadata', {})
        
        # Store for_pdf flag for use in generation methods
        self._for_pdf = for_pdf
        
        # Get genre-based colors
        genre = meta.get('genre', '').lower()
        colors = self._get_colors_for_genre(genre)
        
        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta.get('title', 'Film')} - Electronic Press Kit</title>
    <meta name="description" content="{meta.get('logline', '')}">
    <style>{self._generate_css(colors)}</style>
</head>
<body>
    <div class="container">
        {self._generate_cover()}
        {self._generate_synopsis()}
        {self._generate_reviews()}
        {self._generate_festivals()}
        {self._generate_press()}
        {self._generate_team()}
        {self._generate_distribution()}
        {self._generate_technical()}
        {self._generate_gallery()}
        {self._generate_downloads()}
        {self._generate_contact()}
    </div>
</body>
</html>"""
        
        output_path = self.output_dir / "html" / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ HTML generated: {output_path.name}")
        return output_path
    
    def generate_pdf(self, html_file: Optional[Path] = None, output_name: str = "epk.pdf", use_playwright: bool = True) -> Optional[Path]:
        """Generate print-ready PDF using Playwright (preferred) or WeasyPrint"""
        
        # Try Playwright first (better rendering)
        if use_playwright and PLAYWRIGHT_AVAILABLE:
            return self._generate_pdf_playwright(html_file, output_name)
        
        # Fall back to WeasyPrint
        if WEASYPRINT_AVAILABLE:
            return self._generate_pdf_weasyprint(html_file, output_name)
        
        logger.warning("âš  No PDF generator available.")
        logger.info("   Install Playwright: pip install playwright && playwright install chromium")
        logger.info("   OR install WeasyPrint: pip install weasyprint")
        return None
    
    def _generate_pdf_playwright(self, html_file: Optional[Path] = None, output_name: str = "epk.pdf") -> Optional[Path]:
        """Generate PDF using Playwright (Chrome rendering engine)"""
        try:
            if html_file is None:
                html_file = self.generate_html("temp_for_pdf.html", for_pdf=True)
            
            output_path = self.output_dir / "pdf" / output_name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info("Generating PDF with Playwright...")
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Load the HTML file
                page.goto(f"file://{html_file.resolve()}")
                
                # Generate PDF with print CSS
                page.pdf(
                    path=str(output_path),
                    format='Letter',
                    margin={
                        'top': '0.75in',
                        'right': '0.75in',
                        'bottom': '0.75in',
                        'left': '0.75in'
                    },
                    print_background=True,
                    display_header_footer=False,
                    prefer_css_page_size=False
                )
                
                browser.close()
            
            logger.info(f"✅ PDF generated: {output_path.name}")
            return output_path
            
        except Exception as e:
            logger.error(f"✅— Playwright PDF generation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _generate_pdf_weasyprint(self, html_file: Optional[Path] = None, output_name: str = "epk.pdf") -> Optional[Path]:
        """Generate PDF using WeasyPrint (fallback option)"""
        try:
            if html_file is None:
                html_file = self.generate_html("temp_for_pdf.html", for_pdf=True)
            
            output_path = self.output_dir / "pdf" / output_name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info("Generating PDF with WeasyPrint...")
            
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # PDF-specific CSS - simplified approach
            pdf_css_string = """
                @page {
                    size: Letter;
                    margin: 0.5in;
                }
                @page :first {
                    margin: 0;
                }
                
                .cover {
                    page-break-after: always;
                    page-break-inside: avoid !important;
                    min-height: 100vh;
                    margin: 0;
                }
                
                .cover-content {
                    page-break-inside: avoid !important;
                }
                
                .poster-container {
                    page-break-inside: avoid !important;
                    page-break-after: avoid !important;
                }
                
                .film-title {
                    page-break-before: avoid !important;
                    page-break-after: avoid !important;
                }
                
                .section {
                    page-break-inside: auto;
                }
                
                .team-section {
                    page-break-inside: avoid;
                }
                
                .team-section h2 {
                    page-break-after: avoid !important;
                }
                
                .team-section .team-grid {
                    page-break-before: avoid !important;
                }
                
                .team-member {
                    page-break-inside: avoid !important;
                }
                
                .review-card {
                    page-break-inside: avoid;
                }
                
                .laurels {
                    page-break-inside: avoid;
                }
                
                .still-img {
                    page-break-inside: avoid;
                }
            """
            
            # Create HTML document from string
            base_url = self.project_dir.resolve().as_uri() + '/'
            html_doc = HTML(string=html_content, base_url=base_url)
            
            # Create CSS object
            pdf_css = CSS(string=pdf_css_string)
            
            # Write PDF
            html_doc.write_pdf(str(output_path), stylesheets=[pdf_css])
            
            logger.info(f"✅ PDF generated: {output_path.name}")
            return output_path
            
        except Exception as e:
            logger.error(f"✅— WeasyPrint PDF generation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _get_colors_for_genre(self, genre: str) -> Dict[str, str]:
        """Get consistent colors for genre"""
        for key, colors in self.GENRE_COLORS.items():
            if key in genre:
                return colors
        return self.DEFAULT_COLORS
    
    def _generate_css(self, colors: Dict[str, str]) -> str:
        """Generate consistent CSS"""
        return f"""
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #1F2937;
    background: #F9FAFB;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
}}

.section {{
    padding: 40px 20px;
    background: white;
    margin-bottom: 2px;
}}

/* Cover Section */
.cover {{
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {colors['secondary']} 0%, {colors['primary']} 100%);
    color: white;
    text-align: center;
    padding: 40px 20px;
    page-break-inside: avoid;
}}

.cover-content {{
    max-width: 900px;
    page-break-inside: avoid;
}}

.poster-container {{
    max-width: 400px;
    margin: 0 auto 20px;
    page-break-inside: avoid;
    page-break-after: avoid;
}}

.poster-container img {{
    width: 100%;
    height: auto;
    border-radius: 8px;
    display: block;
}}

.film-title {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: -1px;
    line-height: 1.1;
    page-break-before: avoid;
    page-break-after: avoid;
}}

.tagline {{
    font-size: 1.3rem;
    margin-bottom: 20px;
    opacity: 0.9;
    font-style: italic;
    page-break-before: avoid;
}}

.film-meta {{
    font-size: 1.1rem;
    margin-top: 15px;
    opacity: 0.9;
    page-break-before: avoid;
}}

.laurels {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 40px;
}}

.laurel {{
    background: rgba(255, 255, 255, 0.1);
    padding: 15px 25px;
    border-radius: 8px;
    font-size: 0.9rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin: 10px;
}}

.laurel-title {{
    font-weight: 700;
    display: block;
    margin-bottom: 5px;
}}

/* Typography */
h2 {{
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: {colors['primary']};
    text-align: center;
    font-weight: 700;
}}

h3 {{
    font-size: 1.8rem;
    color: {colors['primary']};
    margin-bottom: 20px;
}}

.logline {{
    font-size: 1.3rem;
    font-weight: 600;
    text-align: center;
    max-width: 800px;
    margin: 0 auto 30px;
    color: {colors['primary']};
    line-height: 1.8;
}}

.synopsis-text {{
    font-size: 1.1rem;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.9;
    text-align: justify;
}}

/* Reviews Section */
.reviews {{
    background: {colors['secondary']};
    color: white;
}}

.reviews h2 {{
    color: white;
}}

.review-grid {{
    max-width: 1000px;
    margin: 0 auto;
}}

.review-card {{
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 8px;
    border-left: 4px solid {colors['accent']};
    margin-bottom: 20px;
}}

.review-quote {{
    font-size: 1.2rem;
    font-style: italic;
    margin-bottom: 15px;
    line-height: 1.6;
}}

.review-source {{
    font-weight: 600;
    font-size: 1rem;
    opacity: 0.9;
}}

.review-rating {{
    color: {colors['accent']};
    margin-bottom: 10px;
    font-size: 1.1rem;
}}

/* Team Section */
.team-grid {{
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 40px 60px;
    text-align: center;
    margin-top: 0;
}}

.team-member {{
    width: 280px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.team-photo {{
    width: 200px;
    height: 200px;
    border-radius: 50%;
    object-fit: cover;
    margin: 0 auto 20px;
    display: block;
    border: 4px solid {colors['accent']};
    object-position: center;
}}

.member-name {{
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 5px;
    color: {colors['primary']};
}}

.member-role {{
    font-size: 1rem;
    color: #6B7280;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}}

.member-bio {{
    font-size: 0.95rem;
    line-height: 1.6;
    text-align: left;
    color: #4B5563;
}}

/* Gallery */
.stills-gallery {{
    margin: 0 -10px;
}}

.still-img {{
    width: 32%;
    height: 250px;
    object-fit: cover;
    border-radius: 8px;
    margin: 10px 0.5%;
    display: inline-block;
    vertical-align: top;
}}

/* Technical Specs */
.tech-specs {{
    background: #F3F4F6;
    padding: 30px;
    border-radius: 8px;
    max-width: 700px;
    margin: 0 auto;
}}

.spec-row {{
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #D1D5DB;
}}

.spec-row:last-child {{
    border-bottom: none;
}}

.spec-label {{
    font-weight: 600;
    color: {colors['primary']};
}}

.spec-value {{
    color: #374151;
}}

/* Contact Section */
.contact {{
    background: {colors['primary']};
    color: white;
    text-align: center;
}}

.contact h2 {{
    color: white;
}}

.contact-info {{
    font-size: 1.2rem;
    margin: 20px 0;
}}

.contact-info p {{
    margin: 10px 0;
}}

.contact-link {{
    color: white;
    text-decoration: none;
    border-bottom: 2px solid {colors['accent']};
    padding-bottom: 2px;
}}

.contact-link:hover {{
    opacity: 0.8;
}}

/* Print Styles */
@media print {{
    .cover {{
        page-break-after: always;
    }}
    
    .section {{
        page-break-inside: avoid;
    }}
}}
"""
    
    def _generate_cover(self) -> str:
        """Generate cover page"""
        meta = self.config.get('metadata', {})
        awards = self.config.get('awards', [])[:4]
        
        # Find poster
        poster_dir = self.assets_dir / "images" / "posters"
        poster_path = None
        if poster_dir.exists():
            posters = list(poster_dir.glob("*.[jp][pn][g]"))
            if posters:
                if getattr(self, '_for_pdf', False):
                    # Use absolute file path for PDF
                    poster_path = posters[0].resolve().as_uri()
                else:
                    # Use relative path for HTML
                    poster_path = Path("../../") / posters[0].relative_to(self.project_dir)
        
        poster_html = f'<img src="{poster_path}" alt="Poster">' if poster_path else ''
        
        # Only show laurels on cover for HTML, not for PDF
        laurels_html = ""
        if awards and not getattr(self, '_for_pdf', False):
            laurels_html = '<div class="laurels">'
            for award in awards:
                laurels_html += f'''
                <div class="laurel">
                    <span class="laurel-title">{award.get('award', '')}</span>
                    {award.get('festival_name', '')} {award.get('year', '')}
                </div>
                '''
            laurels_html += '</div>'
        
        # Adjust spacing for PDF - much tighter
        title_margin = 'margin-bottom: 10px;' if getattr(self, '_for_pdf', False) else ''
        tagline_margin = 'margin-bottom: 15px;' if getattr(self, '_for_pdf', False) else ''
        meta_margin = 'margin-top: 10px;' if getattr(self, '_for_pdf', False) else ''
        
        return f'''
        <div class="cover">
            <div class="cover-content">
                <div class="poster-container">
                    {poster_html}
                </div>
                <h1 class="film-title" style="{title_margin}">{meta.get('title', '')}</h1>
                {f'<p class="tagline" style="{tagline_margin}">{meta.get("tagline")}</p>' if meta.get('tagline') else ''}
                <p class="film-meta" style="{meta_margin}">
                    {meta.get('genre', '')} | {meta.get('runtime', '')} | {meta.get('rating', 'NR')}
                </p>
                {laurels_html}
            </div>
        </div>
        '''
    
    def _generate_synopsis(self) -> str:
        """Generate synopsis section"""
        meta = self.config.get('metadata', {})
        
        return f'''
        <div class="section">
            <h2>Synopsis</h2>
            <p class="logline">{meta.get('logline', '')}</p>
            <div class="synopsis-text">
                {self._format_paragraphs(meta.get('synopsis', ''))}
            </div>
        </div>
        '''
    
    def _generate_reviews(self) -> str:
        """Generate reviews section"""
        reviews = self.config.get('reviews', [])
        if not reviews:
            return ""
        
        cards = ""
        for review in reviews:
            rating_html = ''
            if review.get('rating'):
                rating_html = f'<div class="review-rating">{"â˜…" * int(review.get("rating", "0"))}</div>'
            
            cards += f'''
            <div class="review-card">
                {rating_html}
                <p class="review-quote">"{review.get('quote', '')}"</p>
                <p class="review-source">â€” {review.get('source', '')}</p>
            </div>
            '''
        
        return f'''
        <div class="section reviews">
            <h2>Press & Reviews</h2>
            <div class="review-grid">
                {cards}
            </div>
        </div>
        '''
    
    def _generate_festivals(self) -> str:
        """Generate festivals section"""
        festivals = self.config.get('festivals', [])
        awards = self.config.get('awards', [])
        
        if not festivals and not awards:
            return ""
        
        content = ""
        
        if awards:
            content += '<h3 style="text-align: center; margin-bottom: 30px;">Awards</h3>'
            content += '<div class="laurels" style="margin-bottom: 50px;">'
            for award in awards:
                content += f'''
                <div class="laurel">
                    <span class="laurel-title">{award.get('award', '')}</span>
                    {award.get('festival_name', '')} {award.get('year', '')}
                </div>
                '''
            content += '</div>'
        
        if festivals:
            content += '<h3 style="text-align: center; margin-bottom: 20px;">Festival Screenings</h3>'
            content += '<div style="max-width: 800px; margin: 0 auto;"><ul style="list-style: none; padding: 0;">'
            for fest in festivals:
                selection = f" - {fest.get('selection_type', '')}" if fest.get('selection_type') else ""
                content += f'''
                <li style="padding: 15px 0; border-bottom: 1px solid #E5E7EB; font-size: 1.1rem;">
                    <strong>{fest.get('festival_name', '')}</strong> {fest.get('year', '')}{selection}
                </li>
                '''
            content += '</ul></div>'
        
        return f'''
        <div class="section">
            <div style="page-break-inside: avoid;">
                <h2>Festivals & Awards</h2>
                {content}
            </div>
        </div>
        ''' if content else ""
    
    def _generate_press(self) -> str:
        """Generate press coverage section"""
        press = self.config.get('press_coverage', [])
        if not press:
            return ""
        
        items = ""
        for item in press:
            url_html = f'<a href="{item["url"]}" target="_blank" style="color: inherit; text-decoration: none; border-bottom: 2px solid currentColor;">Read Article â†’</a>' if item.get('url') else ''
            
            items += f'''
            <div style="background: #F9FAFB; padding: 25px; border-radius: 8px; border-left: 4px solid #3B82F6; margin-bottom: 20px;">
                <div style="font-size: 0.9rem; color: #6B7280; margin-bottom: 10px; text-transform: uppercase;">
                    {item.get('publication', '')} â€¢ {item.get('date', '')}
                </div>
                <h4 style="font-size: 1.3rem; margin-bottom: 15px;">{item.get('title', '')}</h4>
                {f'<p style="margin-bottom: 15px; line-height: 1.6;">{item.get("excerpt", "")}</p>' if item.get('excerpt') else ''}
                {url_html}
            </div>
            '''
        
        return f'''
        <div class="section">
            <h2>Press Coverage</h2>
            <div style="max-width: 900px; margin: 0 auto;">
                {items}
            </div>
        </div>
        '''
    
    def _generate_team(self) -> str:
        """Generate team section"""
        team = self.config.get('team', [])
        if not team:
            return ""
        
        members = ""
        for member in team:
            photo_html = ''
            if member.get('photo'):
                photo_path = self.project_dir / member['photo']
                if photo_path.exists():
                    if getattr(self, '_for_pdf', False):
                        # Use absolute file path for PDF
                        rel_path = photo_path.resolve().as_uri()
                    else:
                        # Use relative path for HTML
                        rel_path = Path("../../") / photo_path.relative_to(self.project_dir)
                    photo_html = f'<img src="{rel_path}" alt="{member.get("name")}" class="team-photo">'
            
            members += f'''
            <div class="team-member">
                {photo_html}
                <h3 class="member-name">{member.get('name', '')}</h3>
                <p class="member-role">{member.get('role', '')}</p>
                {f'<p class="member-bio">{member.get("bio", "")}</p>' if member.get('bio') else ''}
            </div>
            '''

        return f'''
        <div class="section">
            <div style="page-break-inside: avoid;">
                <h2>Cast & Crew</h2>
                <div class="team-grid">
                    {members}
                </div>
            </div>
        </div>
        '''
    
    def _generate_distribution(self) -> str:
        """Generate distribution section"""
        dist = self.config.get('distribution', {})
        if not dist:
            return ""
        
        content = '<div style="max-width: 800px; margin: 0 auto;">'
        
        # Release dates
        if dist.get('theatrical_release') or dist.get('digital_release'):
            content += '<div style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); color: white; padding: 40px; border-radius: 12px; text-align: center; margin-bottom: 30px;">'
            
            if dist.get('theatrical_release'):
                content += f'<div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">THEATRICAL RELEASE</div>'
                content += f'<div style="font-size: 2rem; margin-bottom: 20px;">{dist["theatrical_release"]}</div>'
            
            if dist.get('digital_release'):
                content += f'<div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">DIGITAL RELEASE</div>'
                content += f'<div style="font-size: 2rem;">{dist["digital_release"]}</div>'
            
            content += '</div>'
        
        # Platforms
        if dist.get('platforms'):
            content += '<div style="text-align: center; margin-bottom: 30px;">'
            content += '<h3 style="font-size: 1.5rem; margin-bottom: 20px;">Available On</h3>'
            content += '<div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;">'
            for platform in dist['platforms']:
                content += f'<div style="background: #1F2937; color: white; padding: 15px 30px; border-radius: 8px; font-weight: 600;">{platform}</div>'
            content += '</div></div>'
        
        content += '</div>'
        
        return f'''
        <div class="section">
            <h2>Distribution & Availability</h2>
            {content}
        </div>
        ''' if dist else ""
    
    def _generate_technical(self) -> str:
        """Generate technical specs"""
        meta = self.config.get('metadata', {})
        tech = self.config.get('technical', {})
        
        specs = [
            ('Runtime', meta.get('runtime', '')),
            ('Genre', meta.get('genre', '')),
            ('Rating', meta.get('rating', '')),
            ('Language', meta.get('language', '')),
            ('Country', meta.get('country', '')),
            ('Release Date', meta.get('release_date', '')),
            ('Aspect Ratio', tech.get('aspect_ratio', '')),
            ('Sound', tech.get('sound', '')),
            ('Color', tech.get('color', '')),
        ]
        
        rows = ""
        for label, value in specs:
            if value:
                rows += f'''
                <div class="spec-row">
                    <span class="spec-label">{label}</span>
                    <span class="spec-value">{value}</span>
                </div>
                '''
        
        return f'''
        <div class="section">
            <h2>Technical Information</h2>
            <div class="tech-specs">
                {rows}
            </div>
        </div>
        '''
    
    def _generate_gallery(self) -> str:
        """Generate stills gallery"""
        stills_dir = self.assets_dir / "images" / "stills"
        if not stills_dir.exists():
            return ""
        
        stills = sorted(stills_dir.glob("*.[jp][pn][g]"))[:12]
        if not stills:
            return ""
        
        gallery = ""
        for still in stills:
            if getattr(self, '_for_pdf', False):
                # Use absolute file path for PDF
                rel_path = still.resolve().as_uri()
            else:
                # Use relative path for HTML
                rel_path = Path("../../") / still.relative_to(self.project_dir)
            gallery += f'<img src="{rel_path}" alt="Still" class="still-img">'
        
        return f'''
        <div class="section">
            <h2>Production Stills</h2>
            <div class="stills-gallery">
                {gallery}
            </div>
        </div>
        '''
    
    def _generate_downloads(self) -> str:
        """Generate downloads section"""
        downloads_dir = self.assets_dir / "downloads"
        if not downloads_dir.exists():
            return ""
        
        files = list(downloads_dir.glob("*"))
        if not files:
            return ""
        
        items = ""
        for file in files:
            size_mb = file.stat().st_size / (1024 * 1024)
            if getattr(self, '_for_pdf', False):
                # Use absolute file path for PDF
                rel_path = file.resolve().as_uri()
            else:
                # Use relative path for HTML
                rel_path = Path("../../") / file.relative_to(self.project_dir)
            
            ext = file.suffix.lower()
            icon = {'jpg': 'ðŸ–¼ï¸', 'png': 'ðŸ–¼ï¸', 'pdf': 'ðŸ“„', 'mp4': 'ðŸŽ¬', 'zip': 'ðŸ“¦'}.get(ext[1:], 'ðŸ“Ž')
            
            items += f'''
            <a href="{rel_path}" download style="display: flex; align-items: center; padding: 20px; background: #F9FAFB; border-radius: 8px; margin-bottom: 15px; text-decoration: none; color: inherit;">
                <span style="font-size: 2rem; margin-right: 20px;">{icon}</span>
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 5px;">{file.name}</div>
                    <div style="font-size: 0.9rem; color: #6B7280;">{size_mb:.1f} MB</div>
                </div>
                <span style="font-size: 1.5rem;">â¬‡ï¸</span>
            </a>
            '''
        
        return f'''
        <div class="section">
            <h2>Download Press Materials</h2>
            <div style="max-width: 700px; margin: 0 auto;">
                {items}
            </div>
        </div>
        '''
    
    def _generate_contact(self) -> str:
        """Generate contact section"""
        contact = self.config.get('contact', {})
        
        return f'''
        <div class="section contact">
            <h2>Contact</h2>
            <div class="contact-info">
                <p><strong>Distribution:</strong> {contact.get('distribution_company', 'Filmhub')}</p>
                {f'<p><strong>Contact:</strong> {contact.get("name", "")}</p>' if contact.get('name') else ''}
                <p><strong>Email:</strong> <a href="mailto:{contact.get('email', '')}" class="contact-link">{contact.get('email', '')}</a></p>
                {f'<p><strong>Phone:</strong> {contact.get("phone", "")}</p>' if contact.get('phone') else ''}
                {f'<p><strong>Website:</strong> <a href="{contact.get("website", "")}" class="contact-link" target="_blank">{contact.get("website", "")}</a></p>' if contact.get('website') else ''}
            </div>
        </div>
        '''
    
    def _format_paragraphs(self, text: str) -> str:
        """Format text into HTML paragraphs"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return ''.join(f'<p style="margin-bottom: 20px;">{p}</p>' for p in paragraphs)
    
    def generate_config_template(self, output_file: str = "film_config.json"):
        """Generate comprehensive config template"""
        template = {
            "metadata": {
                "title": "Your Film Title",
                "tagline": "A compelling tagline",
                "logline": "One or two sentences that capture the essence of your film",
                "synopsis": "Full synopsis (2-3 paragraphs). Tell the story, characters, and what makes this film unique.",
                "genre": "Drama",
                "runtime": "90 minutes",
                "rating": "NR",
                "release_date": "2025",
                "language": "English",
                "country": "USA",
                "director": "Director Name"
            },
            "team": [
                {
                    "name": "Director Name",
                    "role": "Writer/Director",
                    "bio": "Brief bio highlighting relevant experience",
                    "photo": "assets/images/crew/director.jpg"
                }
            ],
            "awards": [
                {
                    "festival_name": "Sundance Film Festival",
                    "award": "Jury Award - Best Feature",
                    "year": "2025"
                }
            ],
            "festivals": [
                {
                    "festival_name": "Tribeca Film Festival",
                    "year": "2025",
                    "selection_type": "World Premiere"
                }
            ],
            "reviews": [
                {
                    "quote": "A masterpiece of modern cinema",
                    "source": "The Hollywood Reporter",
                    "rating": "5"
                }
            ],
            "press_coverage": [
                {
                    "title": "Article Title",
                    "publication": "Publication Name",
                    "date": "January 2025",
                    "url": "https://...",
                    "excerpt": "Brief excerpt..."
                }
            ],
            "distribution": {
                "theatrical_release": "March 15, 2025",
                "digital_release": "May 1, 2025",
                "platforms": ["Apple TV", "Prime Video", "YouTube"],
                "territories": ["USA", "Canada"]
            },
            "technical": {
                "aspect_ratio": "16:9",
                "sound": "5.1 Surround",
                "color": "Color"
            },
            "contact": {
                "distribution_company": "Filmhub",
                "name": "Your Name",
                "email": "contact@filmhub.com",
                "phone": "(555) 123-4567",
                "website": "https://filmhub.com"
            }
        }
        
        output_path = self.project_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2)
        
        logger.info(f"✅ Configuration template created: {output_file}")
        return output_path


class BatchProcessor:
    """Batch process multiple films"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.results = []
    
    def find_projects(self) -> List[Path]:
        """Find all film projects"""
        projects = []
        for item in self.root_dir.iterdir():
            if item.is_dir() and (item / "film_config.json").exists():
                projects.append(item)
        return projects
    
    def process_all(self) -> List[Dict]:
        """Process all films"""
        projects = self.find_projects()
        
        if not projects:
            logger.warning("No film projects found")
            return []
        
        logger.info(f"Found {len(projects)} projects to process")
        logger.info("="*60)
        
        for project in projects:
            result = self._process_single(project)
            self.results.append(result)
        
        self._print_summary()
        return self.results
    
    def _process_single(self, project_dir: Path) -> Dict:
        """Process single film"""
        result = {
            'film': project_dir.name,
            'success': False,
            'html_path': None,
            'pdf_path': None,
            'errors': [],
            'warnings': []
        }
        
        try:
            logger.info(f"\nProcessing: {project_dir.name}")
            
            epk = EPKGenerator(project_dir)
            config_file = project_dir / "film_config.json"
            epk.load_config(config_file)
            
            # Validate
            validation = epk.validate_assets()
            result['errors'] = validation.errors
            result['warnings'] = validation.warnings
            
            if not validation.is_valid:
                logger.error(f"  ✅— Validation failed:")
                for error in validation.errors:
                    logger.error(f"    - {error}")
                return result
            
            if validation.warnings:
                for warning in validation.warnings:
                    logger.warning(f"  âš  {warning}")
            
            # Generate
            html_path = epk.generate_html()
            result['html_path'] = str(html_path)
            
            pdf_path = epk.generate_pdf()
            if pdf_path:
                result['pdf_path'] = str(pdf_path)
            
            result['success'] = True
            logger.info(f"  ✅“ Completed: {project_dir.name}")
            
        except Exception as e:
            logger.error(f"  ✅— Failed: {e}")
            result['errors'].append(str(e))
        
        return result
    
    def _print_summary(self):
        """Print summary"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        failed = total - successful
        
        logger.info("\n" + "="*60)
        logger.info("BATCH PROCESSING SUMMARY")
        logger.info("="*60)
        logger.info(f"Total: {total} | Success: {successful} | Failed: {failed}")
        
        if failed > 0:
            logger.info("\nFailed Films:")
            for result in self.results:
                if not result['success']:
                    logger.info(f"  - {result['film']}")
                    for error in result['errors']:
                        logger.info(f"      {error}")
        
        logger.info("="*60)


def main():
    """Main CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate professional film EPKs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Setup new project
  python epk_generator.py "My-Film" --setup --template

  # Generate EPK
  python epk_generator.py "My-Film" --config film_config.json --pdf

  # Validate only
  python epk_generator.py "My-Film" --config film_config.json --validate

  # Batch process
  python epk_generator.py films/ --batch
        """
    )
    
    parser.add_argument('project_dir', help='Project directory')
    parser.add_argument('--setup', action='store_true', help='Setup project structure')
    parser.add_argument('--template', action='store_true', help='Generate config template')
    parser.add_argument('--config', help='Config file path')
    parser.add_argument('--output', default='index.html', help='Output HTML filename')
    parser.add_argument('--pdf', action='store_true', help='Generate PDF')
    parser.add_argument('--validate', action='store_true', help='Validate only')
    parser.add_argument('--batch', action='store_true', help='Batch process')
    parser.add_argument('--no-optimize', action='store_true', help='Skip image optimization')
    
    args = parser.parse_args()
    
    # Batch processing
    if args.batch:
        processor = BatchProcessor(args.project_dir)
        results = processor.process_all()
        
        # Save results
        results_file = Path(args.project_dir) / "batch_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"\n✅“ Results saved: {results_file}")
        return
    
    # Single film
    epk = EPKGenerator(args.project_dir, optimize_images=not args.no_optimize)
    
    if args.setup:
        epk.setup_project_structure()
    
    if args.template:
        epk.generate_config_template()
        return
    
    if args.config:
        epk.load_config(args.config)
        
        # Validate
        validation = epk.validate_assets()
        
        if validation.errors:
            logger.error("\nâŒ Validation Errors:")
            for error in validation.errors:
                logger.error(f"  - {error}")
        
        if validation.warnings:
            logger.warning("\nâš ï¸ Warnings:")
            for warning in validation.warnings:
                logger.warning(f"  - {warning}")
        
        if args.validate:
            if validation.is_valid:
                logger.info("\n✅“ All validation checks passed!")
            return
        
        if not validation.is_valid:
            logger.error("\n✅— Cannot generate EPK due to validation errors")
            return
        
        # Generate
        logger.info("\n" + "="*60)
        logger.info("GENERATING EPK")
        logger.info("="*60)
        
        html_path = epk.generate_html(args.output)
        
        if args.pdf:
            # Always generate a separate HTML file for PDF with absolute paths
            pdf_path = epk.generate_pdf()  # Don't pass html_path - let it generate its own
        
        logger.info("\n" + "="*60)
        logger.info("✅ EPK GENERATION COMPLETE")
        logger.info("="*60)
        logger.info(f"HTML: {html_path}")
        if args.pdf and WEASYPRINT_AVAILABLE:
            logger.info(f"PDF: {pdf_path}")
        logger.info("="*60 + "\n")


if __name__ == "__main__":
    main()
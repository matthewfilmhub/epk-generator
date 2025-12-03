// Client-side EPK HTML Generator
// Generates professional EPK HTML directly in the browser

export const generateEPKHTML = (config, assets) => {
  const meta = config.metadata || {};
  const genre = meta.genre?.toLowerCase() || 'drama';
  
  // Genre-based colors
  const genreColors = {
    'horror': { primary: '#8B0000', secondary: '#2C2C2C', accent: '#FF4444' },
    'sci-fi': { primary: '#1E3A8A', secondary: '#0F172A', accent: '#60A5FA' },
    'fantasy': { primary: '#7C3AED', secondary: '#1E1B4B', accent: '#A78BFA' },
    'comedy': { primary: '#F59E0B', secondary: '#78350F', accent: '#FBBF24' },
    'drama': { primary: '#374151', secondary: '#1F2937', accent: '#9CA3AF' },
    'action': { primary: '#DC2626', secondary: '#18181B', accent: '#EF4444' },
    'documentary': { primary: '#059669', secondary: '#064E3B', accent: '#10B981' },
    'romance': { primary: '#DB2777', secondary: '#831843', accent: '#F472B6' },
    'thriller': { primary: '#4B5563', secondary: '#111827', accent: '#6B7280' },
  };
  
  const colors = genreColors[genre] || { primary: '#2563EB', secondary: '#1E293B', accent: '#3B82F6' };
  
  // Convert uploaded images to data URLs
  const posterDataUrl = assets.poster ? URL.createObjectURL(assets.poster) : '';
  const stillsDataUrls = assets.stills.map(still => URL.createObjectURL(still));
  
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${meta.title || 'Film'} - Electronic Press Kit</title>
    <meta name="description" content="${meta.logline || ''}">
    <style>
        ${generateCSS(colors)}
    </style>
</head>
<body>
    <div class="container">
        ${generateCover(meta, posterDataUrl, config.awards, colors)}
        ${generateSynopsis(meta)}
        ${generateReviews(config.reviews || [])}
        ${generateFestivals(config.festivals || [], config.awards || [])}
        ${generatePress(config.press_coverage || [])}
        ${generateTeam(config.team || [])}
        ${generateDistribution(config.distribution || {})}
        ${generateTechnical(meta, config.technical || {})}
        ${generateGallery(stillsDataUrls)}
        ${generateContact(config.contact || {})}
    </div>
</body>
</html>`;
  
  return html;
};

const generateCSS = (colors) => `
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #1F2937;
    background: #F9FAFB;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.section {
    padding: 40px 20px;
    background: white;
    margin-bottom: 2px;
}

.cover {
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, ${colors.secondary} 0%, ${colors.primary} 100%);
    color: white;
    text-align: center;
    padding: 40px 20px;
}

.cover-content {
    max-width: 900px;
}

.poster-container {
    max-width: 400px;
    margin: 0 auto 20px;
}

.poster-container img {
    width: 100%;
    height: auto;
    border-radius: 8px;
    display: block;
}

.film-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: -1px;
    line-height: 1.1;
}

.tagline {
    font-size: 1.3rem;
    margin-bottom: 20px;
    opacity: 0.9;
    font-style: italic;
}

.film-meta {
    font-size: 1.1rem;
    margin-top: 15px;
    opacity: 0.9;
}

.laurels {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 40px;
    gap: 15px;
}

.laurel {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px 25px;
    border-radius: 8px;
    font-size: 0.9rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.laurel-title {
    font-weight: 700;
    display: block;
    margin-bottom: 5px;
}

h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: ${colors.primary};
    text-align: center;
    font-weight: 700;
}

h3 {
    font-size: 1.8rem;
    color: ${colors.primary};
    margin-bottom: 20px;
}

.logline {
    font-size: 1.3rem;
    font-weight: 600;
    text-align: center;
    max-width: 800px;
    margin: 0 auto 30px;
    color: ${colors.primary};
    line-height: 1.8;
}

.synopsis-text {
    font-size: 1.1rem;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.9;
    text-align: justify;
}

.synopsis-text p {
    margin-bottom: 20px;
}

.reviews {
    background: ${colors.secondary};
    color: white;
}

.reviews h2 {
    color: white;
}

.review-grid {
    max-width: 1000px;
    margin: 0 auto;
}

.review-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 8px;
    border-left: 4px solid ${colors.accent};
    margin-bottom: 20px;
}

.review-quote {
    font-size: 1.2rem;
    font-style: italic;
    margin-bottom: 15px;
    line-height: 1.6;
}

.review-source {
    font-weight: 600;
    font-size: 1rem;
    opacity: 0.9;
}

.review-rating {
    color: ${colors.accent};
    margin-bottom: 10px;
    font-size: 1.1rem;
}

.team-grid {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 40px 60px;
    text-align: center;
}

.team-member {
    width: 280px;
}

.member-name {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 5px;
    color: ${colors.primary};
}

.member-role {
    font-size: 1rem;
    color: #6B7280;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

.member-bio {
    font-size: 0.95rem;
    line-height: 1.6;
    text-align: left;
    color: #4B5563;
}

.stills-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.still-img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    border-radius: 8px;
}

.tech-specs {
    background: #F3F4F6;
    padding: 30px;
    border-radius: 8px;
    max-width: 700px;
    margin: 0 auto;
}

.spec-row {
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #D1D5DB;
}

.spec-row:last-child {
    border-bottom: none;
}

.spec-label {
    font-weight: 600;
    color: ${colors.primary};
}

.spec-value {
    color: #374151;
}

.contact {
    background: ${colors.primary};
    color: white;
    text-align: center;
}

.contact h2 {
    color: white;
}

.contact-info {
    font-size: 1.2rem;
    margin: 20px 0;
}

.contact-info p {
    margin: 10px 0;
}

.contact-link {
    color: white;
    text-decoration: none;
    border-bottom: 2px solid ${colors.accent};
    padding-bottom: 2px;
}

@media print {
    .cover {
        page-break-after: always;
    }
    .section {
        page-break-inside: avoid;
    }
}
`;

const generateCover = (meta, posterUrl, awards, colors) => {
  const posterHtml = posterUrl ? `<img src="${posterUrl}" alt="Poster">` : '';
  
  const laurelsHtml = awards && awards.length > 0 ? `
    <div class="laurels">
      ${awards.slice(0, 4).map(award => `
        <div class="laurel">
          <span class="laurel-title">${award.award || ''}</span>
          ${award.festival_name || ''} ${award.year || ''}
        </div>
      `).join('')}
    </div>
  ` : '';
  
  return `
    <div class="cover">
      <div class="cover-content">
        ${posterUrl ? `<div class="poster-container">${posterHtml}</div>` : ''}
        <h1 class="film-title">${meta.title || ''}</h1>
        ${meta.tagline ? `<p class="tagline">${meta.tagline}</p>` : ''}
        <p class="film-meta">
          ${meta.genre || ''} | ${meta.runtime || ''} | ${meta.rating || 'NR'}
        </p>
        ${laurelsHtml}
      </div>
    </div>
  `;
};

const generateSynopsis = (meta) => `
  <div class="section">
    <h2>Synopsis</h2>
    <p class="logline">${meta.logline || ''}</p>
    <div class="synopsis-text">
      ${meta.synopsis ? meta.synopsis.split('\n\n').map(p => `<p>${p}</p>`).join('') : ''}
    </div>
  </div>
`;

const generateReviews = (reviews) => {
  if (!reviews || reviews.length === 0) return '';
  
  return `
    <div class="section reviews">
      <h2>Press & Reviews</h2>
      <div class="review-grid">
        ${reviews.map(review => `
          <div class="review-card">
            ${review.rating ? `<div class="review-rating">${'★'.repeat(parseInt(review.rating))}</div>` : ''}
            <p class="review-quote">"${review.quote || ''}"</p>
            <p class="review-source">— ${review.source || ''}</p>
          </div>
        `).join('')}
      </div>
    </div>
  `;
};

const generateFestivals = (festivals, awards) => {
  if ((!festivals || festivals.length === 0) && (!awards || awards.length === 0)) return '';
  
  let content = '';
  
  if (awards && awards.length > 0) {
    content += `
      <h3 style="text-align: center; margin-bottom: 30px;">Awards</h3>
      <div class="laurels" style="margin-bottom: 50px;">
        ${awards.map(award => `
          <div class="laurel" style="background: #F3F4F6; color: #1F2937; border-color: #D1D5DB;">
            <span class="laurel-title">${award.award || ''}</span>
            ${award.festival_name || ''} ${award.year || ''}
          </div>
        `).join('')}
      </div>
    `;
  }
  
  if (festivals && festivals.length > 0) {
    content += `
      <h3 style="text-align: center; margin-bottom: 20px;">Festival Screenings</h3>
      <div style="max-width: 800px; margin: 0 auto;">
        <ul style="list-style: none; padding: 0;">
          ${festivals.map(fest => `
            <li style="padding: 15px 0; border-bottom: 1px solid #E5E7EB; font-size: 1.1rem;">
              <strong>${fest.festival_name || ''}</strong> ${fest.year || ''}${fest.selection_type ? ` - ${fest.selection_type}` : ''}
            </li>
          `).join('')}
        </ul>
      </div>
    `;
  }
  
  return `<div class="section"><h2>Festivals & Awards</h2>${content}</div>`;
};

const generatePress = (press) => {
  if (!press || press.length === 0) return '';
  
  return `
    <div class="section">
      <h2>Press Coverage</h2>
      <div style="max-width: 900px; margin: 0 auto;">
        ${press.map(item => `
          <div style="background: #F9FAFB; padding: 25px; border-radius: 8px; border-left: 4px solid #3B82F6; margin-bottom: 20px;">
            <div style="font-size: 0.9rem; color: #6B7280; margin-bottom: 10px; text-transform: uppercase;">
              ${item.publication || ''} • ${item.date || ''}
            </div>
            <h4 style="font-size: 1.3rem; margin-bottom: 15px;">${item.title || ''}</h4>
            ${item.excerpt ? `<p style="margin-bottom: 15px; line-height: 1.6;">${item.excerpt}</p>` : ''}
            ${item.url ? `<a href="${item.url}" target="_blank" style="color: inherit; text-decoration: none; border-bottom: 2px solid currentColor;">Read Article →</a>` : ''}
          </div>
        `).join('')}
      </div>
    </div>
  `;
};

const generateTeam = (team) => {
  if (!team || team.length === 0) return '';
  
  return `
    <div class="section">
      <h2>Cast & Crew</h2>
      <div class="team-grid">
        ${team.map(member => `
          <div class="team-member">
            <h3 class="member-name">${member.name || ''}</h3>
            <p class="member-role">${member.role || ''}</p>
            ${member.bio ? `<p class="member-bio">${member.bio}</p>` : ''}
          </div>
        `).join('')}
      </div>
    </div>
  `;
};

const generateDistribution = (dist) => {
  if (!dist || Object.keys(dist).length === 0) return '';
  
  let content = '<div style="max-width: 800px; margin: 0 auto;">';
  
  if (dist.theatrical_release || dist.digital_release) {
    content += '<div style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); color: white; padding: 40px; border-radius: 12px; text-align: center; margin-bottom: 30px;">';
    
    if (dist.theatrical_release) {
      content += `
        <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">THEATRICAL RELEASE</div>
        <div style="font-size: 2rem; margin-bottom: 20px;">${dist.theatrical_release}</div>
      `;
    }
    
    if (dist.digital_release) {
      content += `
        <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">DIGITAL RELEASE</div>
        <div style="font-size: 2rem;">${dist.digital_release}</div>
      `;
    }
    
    content += '</div>';
  }
  
  if (dist.platforms && dist.platforms.length > 0) {
    content += `
      <div style="text-align: center; margin-bottom: 30px;">
        <h3 style="font-size: 1.5rem; margin-bottom: 20px;">Available On</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;">
          ${dist.platforms.map(platform => `
            <div style="background: #1F2937; color: white; padding: 15px 30px; border-radius: 8px; font-weight: 600;">${platform}</div>
          `).join('')}
        </div>
      </div>
    `;
  }
  
  content += '</div>';
  
  return `<div class="section"><h2>Distribution & Availability</h2>${content}</div>`;
};

const generateTechnical = (meta, tech) => {
  const specs = [
    ['Runtime', meta.runtime],
    ['Genre', meta.genre],
    ['Rating', meta.rating],
    ['Language', meta.language],
    ['Country', meta.country],
    ['Release Date', meta.release_date],
    ['Aspect Ratio', tech.aspect_ratio],
    ['Sound', tech.sound],
    ['Color', tech.color],
  ].filter(([_, value]) => value);
  
  return `
    <div class="section">
      <h2>Technical Information</h2>
      <div class="tech-specs">
        ${specs.map(([label, value]) => `
          <div class="spec-row">
            <span class="spec-label">${label}</span>
            <span class="spec-value">${value}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `;
};

const generateGallery = (stillsUrls) => {
  if (!stillsUrls || stillsUrls.length === 0) return '';
  
  return `
    <div class="section">
      <h2>Production Stills</h2>
      <div class="stills-gallery">
        ${stillsUrls.map(url => `
          <img src="${url}" alt="Still" class="still-img">
        `).join('')}
      </div>
    </div>
  `;
};

const generateContact = (contact) => `
  <div class="section contact">
    <h2>Contact</h2>
    <div class="contact-info">
      <p><strong>Distribution:</strong> ${contact.distribution_company || 'Filmhub'}</p>
      ${contact.name ? `<p><strong>Contact:</strong> ${contact.name}</p>` : ''}
      <p><strong>Email:</strong> <a href="mailto:${contact.email || ''}" class="contact-link">${contact.email || ''}</a></p>
      ${contact.phone ? `<p><strong>Phone:</strong> ${contact.phone}</p>` : ''}
      ${contact.website ? `<p><strong>Website:</strong> <a href="${contact.website}" class="contact-link" target="_blank">${contact.website}</a></p>` : ''}
    </div>
  </div>
`;

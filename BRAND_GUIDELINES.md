# EPK Generator - Brand Guidelines

## Filmhub Brand Colors

The EPK Generator UI has been designed to align with Filmhub's brand identity, created by STUDIO HERRSTRÖM. The color palette is inspired by cinema, particularly the iconic Braun Nizo S800 camera designed by Dieter Rams.

### Primary Colors

**Filmhub Orange** - `#FF6B35`
- Primary action color
- Used for: Buttons, links, interactive elements, progress indicators
- Purpose: Highlights key messaging and calls-to-action
- Represents: Energy, creativity, action

**Black** - `#000000`
- Primary background color
- Used for: Main background, navigation, headers
- Purpose: Professional, cinematic foundation
- Represents: Sophistication, cinema, professionalism

### Secondary Colors

**Gray Scale**
- Light Gray: `#E5E5E5` - Borders, subtle backgrounds
- Medium Gray: `#9E9E9E` - Secondary text, disabled states  
- Dark Gray: `#424242` - Tertiary backgrounds, cards
- Purpose: Neutral tones that support content hierarchy
- Represents: Clarity, balance, timelessness

**White** - `#FFFFFF`
- Content backgrounds
- Primary text on dark backgrounds
- Used for: Forms, cards, text input areas
- Purpose: Maximum readability and contrast
- Represents: Clarity, simplicity, focus

### Color Usage Guidelines

#### Do's ✅
- Use Orange for primary actions (submit, download, proceed)
- Use Black/Dark Gray for backgrounds to create cinematic feel
- Use White for content areas and text on dark backgrounds
- Maintain high contrast for accessibility
- Use Gray tones for secondary actions and disabled states

#### Don'ts ❌
- Don't use bright, saturated colors outside the palette
- Don't use Orange for large background areas
- Don't place Orange text on White backgrounds (fails contrast)
- Don't mix the Filmhub palette with other brand colors
- Don't use pure black (#000) for body text (use dark gray instead)

### Implementation in Code

#### Tailwind Classes
```jsx
// Primary actions
className="bg-orange-500 hover:bg-orange-600"

// Backgrounds
className="bg-black"
className="bg-gray-900"

// Text
className="text-white"
className="text-gray-400"

// Borders and inputs
className="border-gray-300 focus:ring-orange-500 focus:border-orange-500"
```

#### Custom Filmhub Colors (Tailwind Config)
```javascript
colors: {
  filmhub: {
    orange: '#FF6B35',
    black: '#000000',
    gray: {
      light: '#E5E5E5',
      DEFAULT: '#9E9E9E',
      dark: '#424242',
    },
    white: '#FFFFFF',
  },
}
```

### Typography

**Font Family**: System fonts for performance and consistency
- Primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- Monospace: For code or technical content
- Maintains Filmhub's emphasis on clarity and control

**Font Weights**
- Regular (400): Body text
- Semibold (600): Subheadings, buttons
- Bold (700-800): Main headings, emphasis

### UI Component Colors

#### Buttons

**Primary Button**
```jsx
<button className="bg-orange-500 hover:bg-orange-600 text-white">
  Primary Action
</button>
```

**Secondary Button**
```jsx
<button className="bg-gray-700 hover:bg-gray-600 text-white">
  Secondary Action
</button>
```

**Disabled Button**
```jsx
<button className="bg-gray-400 text-white cursor-not-allowed" disabled>
  Disabled
</button>
```

#### Form Inputs
```jsx
<input 
  className="border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
/>
```

#### Progress Indicators
- Active step: Orange background (`bg-orange-500`)
- Inactive step: Dark gray (`bg-gray-700`)
- Completed step: Orange with checkmark

#### Alerts
- Success: Green with dark background
- Warning: Yellow/Orange with dark background
- Error: Red with dark background
- Info: Blue with dark background

### Accessibility

**Contrast Ratios**
- Orange on Black: 5.8:1 (AA)
- White on Black: 21:1 (AAA)
- Gray on Black: Varies by shade (min 4.5:1 for text)

**Focus States**
- Always visible orange ring (`ring-orange-500`)
- 2px width for keyboard navigation
- Consistent across all interactive elements

**Dark Mode Support**
The palette is inherently dark-mode friendly:
- Black/dark gray backgrounds reduce eye strain
- Orange provides sufficient contrast
- White text on dark is easier to read in low light

### Brand Personality

The color palette reflects:
- **Credibility**: Neutral blacks and grays
- **Innovation**: Purposeful orange highlights  
- **Cinema**: Film-inspired aesthetic
- **Trust**: Professional, minimal palette
- **Artistry**: Balanced composition

### Design Principles

1. **Function Over Form**: Orange used purposefully for actions
2. **Simplification**: Limited palette reduces decision fatigue
3. **Clarity**: High contrast for readability
4. **Cinema-First**: Colors drawn from film equipment
5. **Timeless**: Neutral base with accent color

### Comparison with Generic Design

**Before (Generic Purple)**
- Purple: Common tech startup color
- Less distinctive
- No connection to film industry

**After (Filmhub Orange)**
- Orange: Unique, memorable
- Directly inspired by cinema equipment
- Aligns with Filmhub brand identity
- Professional and artistic balance

### Using Colors in Different Contexts

#### Backgrounds
```
Primary: #000000 (Black)
Secondary: #424242 (Dark Gray)
Cards/Panels: #1F2937 (Gray-900 in Tailwind)
```

#### Text
```
Primary: #FFFFFF (White)
Secondary: #9E9E9E (Medium Gray)
Disabled: #6B7280 (Gray-500 in Tailwind)
```

#### Interactive Elements
```
Primary Action: #FF6B35 (Orange)
Hover State: Darker orange (#E55A2B)
Focus Ring: Orange with opacity
```

#### Status Indicators
```
Active/Selected: Orange
Inactive: Dark Gray
Disabled: Medium Gray
```

### Implementation Checklist

When building new components:
- [ ] Primary actions use orange
- [ ] Backgrounds use black/dark gray
- [ ] Text maintains contrast ratio > 4.5:1
- [ ] Focus states are visible (orange ring)
- [ ] Hover states darken by ~10-15%
- [ ] Disabled states use medium gray
- [ ] No colors outside approved palette

### Maintaining Brand Consistency

**Regular Reviews**
- Quarterly color audit of all UI elements
- Ensure no drift from brand colors
- Check new features follow guidelines

**Team Training**
- All designers/developers know brand colors
- Reference this guide when building features
- Test color contrast for accessibility

**Version Control**
- Document any approved color additions
- Update Tailwind config for team-wide use
- Keep this guide current with changes

---

## Summary

The EPK Generator uses Filmhub's cinema-inspired color palette:
- **Orange** (#FF6B35): Primary actions and highlights
- **Black** (#000000): Main backgrounds
- **Gray tones**: Supporting elements
- **White** (#FFFFFF): Content and text

This palette creates a professional, cinematic experience that aligns with Filmhub's brand identity while maintaining excellent accessibility and usability.

For questions or updates, refer to Filmhub's main brand guidelines or contact the design team.

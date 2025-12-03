# Filmhub Brand Color Palette

## Quick Reference

### Primary Palette

```
┌─────────────────────────────────────────────┐
│  FILMHUB ORANGE                             │
│  #FF6B35                                    │
│  RGB: 255, 107, 53                          │
│  Use: Buttons, CTAs, Highlights             │
│  🟠🟠🟠🟠🟠                                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  BLACK                                      │
│  #000000                                    │
│  RGB: 0, 0, 0                               │
│  Use: Primary Backgrounds                   │
│  ⬛⬛⬛⬛⬛                                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  WHITE                                      │
│  #FFFFFF                                    │
│  RGB: 255, 255, 255                         │
│  Use: Content Areas, Primary Text           │
│  ⬜⬜⬜⬜⬜                                  │
└─────────────────────────────────────────────┘
```

### Gray Scale

```
┌─────────────────────────────────────────────┐
│  LIGHT GRAY                                 │
│  #E5E5E5                                    │
│  Use: Borders, Subtle Backgrounds           │
│  ◽◽◽◽◽                                     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  MEDIUM GRAY                                │
│  #9E9E9E                                    │
│  Use: Secondary Text, Icons                 │
│  ◻◻◻◻◻                                      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  DARK GRAY                                  │
│  #424242                                    │
│  Use: Cards, Secondary Backgrounds          │
│  ◼◼◼◼◼                                      │
└─────────────────────────────────────────────┘
```

## Hex Codes for Designers

Copy and paste these into your design tools:

```
Primary:
#FF6B35  (Filmhub Orange)
#000000  (Black)
#FFFFFF  (White)

Grayscale:
#E5E5E5  (Light Gray)
#9E9E9E  (Medium Gray)  
#424242  (Dark Gray)

Additional UI Colors (from Tailwind):
#111827  (Gray-900 - Dark backgrounds)
#1F2937  (Gray-800 - Card backgrounds)
#374151  (Gray-700 - Secondary buttons)
#6B7280  (Gray-500 - Disabled text)
```

## Tailwind CSS Classes

### Backgrounds
```css
bg-orange-500      /* #FF6B35 - Primary buttons */
bg-orange-600      /* #E55A2B - Button hover */
bg-black           /* #000000 - Page background */
bg-gray-900        /* #111827 - Dark sections */
bg-gray-800        /* #1F2937 - Cards */
bg-gray-700        /* #374151 - Secondary buttons */
bg-white           /* #FFFFFF - Content areas */
```

### Text
```css
text-orange-500    /* #FF6B35 - Accent text */
text-white         /* #FFFFFF - Primary text on dark */
text-gray-400      /* #9CA3AF - Secondary text */
text-gray-500      /* #6B7280 - Tertiary text */
text-gray-900      /* #111827 - Text on light */
```

### Borders
```css
border-orange-500  /* #FF6B35 - Active borders */
border-gray-300    /* #D1D5DB - Input borders */
border-gray-700    /* #374151 - Dark borders */
```

### Focus States
```css
focus:ring-orange-500       /* Orange focus ring */
focus:border-orange-500     /* Orange border on focus */
```

## Color Combinations

### High Contrast (Accessible)
```
✓ White text on Black background      (21:1)
✓ Orange on Black background           (5.8:1)
✓ White text on Orange background      (3.6:1)
✓ Gray-400 text on Black background    (8.5:1)
```

### Button States
```
Default:  bg-orange-500 text-white
Hover:    bg-orange-600 text-white
Active:   bg-orange-700 text-white
Disabled: bg-gray-400 text-white
```

### Form Inputs
```
Default:  border-gray-300 bg-white
Focus:    border-orange-500 ring-orange-500
Error:    border-red-500 ring-red-500
Success:  border-green-500 ring-green-500
```

## Usage Examples

### Primary Button
```jsx
<button className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg">
  Create EPK
</button>
```

### Secondary Button
```jsx
<button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg">
  Cancel
</button>
```

### Input Field
```jsx
<input 
  className="border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 rounded-lg px-4 py-2"
/>
```

### Progress Step (Active)
```jsx
<div className="bg-orange-500 text-white w-10 h-10 rounded-full flex items-center justify-center">
  1
</div>
```

### Progress Step (Inactive)
```jsx
<div className="bg-gray-700 text-white w-10 h-10 rounded-full flex items-center justify-center">
  2
</div>
```

## Design System Integration

### Figma
1. Create color styles named: `Filmhub/Orange`, `Filmhub/Black`, etc.
2. Use these HEX codes exactly
3. Share library with team

### Sketch
1. Add to document colors
2. Create symbols for buttons/components
3. Use color variables

### Adobe XD
1. Add to Assets panel
2. Create component library
3. Apply to all new designs

## Brand Inspiration

The color palette is inspired by:
- **Braun Nizo S800 camera** by Dieter Rams
- **Cinema equipment** and film industry aesthetics
- **Minimalist design** principles
- **High-contrast** cinematic looks

## Do's and Don'ts

### ✅ Do
- Use orange sparingly for emphasis
- Maintain black backgrounds for cinematic feel
- Ensure text contrast meets WCAG AA standards
- Use grays for hierarchy and depth

### ❌ Don't
- Don't use bright, saturated colors
- Don't use orange for large areas
- Don't mix with other brand colors
- Don't use low-contrast combinations

## Testing Colors

### Contrast Checker
Use WebAIM Contrast Checker to verify:
- Normal text: 4.5:1 minimum
- Large text: 3:1 minimum
- UI components: 3:1 minimum

### Browser Testing
Test in:
- Chrome DevTools (color vision deficiency simulation)
- Safari (various displays)
- Firefox (reader mode)
- Mobile devices (outdoor/bright light)

---

## Need Help?

- Full brand guidelines: [BRAND_GUIDELINES.md](computer:///mnt/user-data/outputs/BRAND_GUIDELINES.md)
- Design questions: Refer to Filmhub brand team
- Implementation: See component examples in App.jsx

**Version**: 1.0 (December 2024)
**Last Updated**: Based on STUDIO HERRSTRÖM brand identity

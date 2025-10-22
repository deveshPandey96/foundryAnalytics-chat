# Theme Toggle Feature Documentation

## Overview

The Azure LLM Analytics Dashboard now includes a comprehensive theme system with light and dark modes. The dark theme features professional styling with red accents, perfect for analytics applications.

## Features

### 🎨 Theme Toggle Button
- **Location**: Fixed position in the top-right corner of the page
- **Icons**: 
  - 🌙 Moon icon when in light mode (click to switch to dark)
  - ☀️ Sun icon when in dark mode (click to switch to light)
- **Responsive**: Fully functional on all screen sizes
- **Interactive**: Hover effects with scale animation and red accent glow

### 🌓 Two Professional Themes

#### Light Theme (Default)
- Clean white backgrounds
- Professional gray accents
- Blue interactive elements
- Optimized for daytime use and well-lit environments

#### Dark Theme
- Professional dark backgrounds (#0e1117)
- Light text for excellent readability
- **Red accents (#ff4b4b)** for:
  - Primary action buttons
  - Links and interactive elements
  - Active tabs and selections
  - Hover states
  - Key metrics and CTAs
- Optimized for low-light environments and reduced eye strain
- WCAG AA compliant contrast ratios

### 💾 Persistent State Management

The theme system intelligently manages user preferences:

1. **localStorage Persistence**: Your theme choice is saved locally and restored on subsequent visits
2. **System Preference Detection**: On first visit, automatically detects your OS theme preference
3. **Priority Order**:
   - User's saved preference (if exists)
   - System preference (`prefers-color-scheme` media query)
   - Default to light theme

### ✨ Smooth Transitions

All theme changes feature smooth 0.3s ease transitions for:
- Background colors
- Text colors
- Border colors
- All interactive elements

## Technical Implementation

### Files Modified/Added

1. **theme_manager.py** (NEW)
   - `ThemeManager` class with theme definitions
   - `get_theme_css()` - Generates CSS for the specified theme
   - `get_theme_toggle_script()` - JavaScript for theme toggle functionality
   - `get_theme_toggle_button()` - HTML for the toggle button

2. **streamlit_dashboard.py** (MODIFIED)
   - Integrated ThemeManager
   - Added theme initialization logic
   - Syncs theme with URL parameters and localStorage

### CSS Variables

All theme colors are defined as CSS variables for easy maintenance:

```css
:root {
    --theme-background
    --theme-secondary-background
    --theme-text-primary
    --theme-text-secondary
    --theme-border
    --theme-accent
    --theme-link
    /* ... and more */
}
```

### JavaScript Functions

The theme system includes JavaScript functions for:
- `getInitialTheme()` - Determines initial theme based on localStorage or system preference
- `saveTheme(theme)` - Saves theme preference to localStorage
- `toggleTheme()` - Switches between light and dark themes

## Usage

### For End Users

Simply click the theme toggle button (🌙/☀️) in the top-right corner to switch themes. Your preference will be automatically saved.

### For Developers

#### Customizing Theme Colors

Edit the `LIGHT_THEME` or `DARK_THEME` dictionaries in `theme_manager.py`:

```python
DARK_THEME = {
    'name': 'dark',
    'background': '#0e1117',
    'accent': '#ff4b4b',  # Red accent
    # ... other colors
}
```

#### Adding New Themed Elements

1. Add CSS in the `get_theme_css()` method using CSS variables:

```css
.my-element {
    background-color: var(--theme-background);
    color: var(--theme-text-primary);
    border-color: var(--theme-accent);
    transition: all 0.3s ease;
}
```

2. The element will automatically respond to theme changes

#### Accessing Current Theme in Python

```python
current_theme = st.session_state.theme
# Returns 'light' or 'dark'
```

## Browser Compatibility

The theme system works in all modern browsers that support:
- CSS Variables (Custom Properties)
- localStorage API
- CSS Media Queries (`prefers-color-scheme`)

Supported browsers:
- Chrome/Edge 49+
- Firefox 31+
- Safari 9.1+
- Opera 36+

## Accessibility

The theme system is designed with accessibility in mind:

- ✅ **WCAG AA Compliant**: All color combinations meet WCAG AA contrast ratio requirements
- ✅ **Keyboard Navigation**: Theme toggle button is keyboard accessible
- ✅ **Screen Reader Support**: Button includes aria-label for screen readers
- ✅ **System Preference**: Respects user's OS-level theme preference
- ✅ **No Motion Sensitivity Issues**: Smooth transitions can be disabled via OS settings

## Mobile Responsiveness

The theme system is fully responsive:

- ✅ Toggle button properly positioned on all screen sizes
- ✅ Touch-friendly button size (50x50px)
- ✅ Tested on mobile viewports (375px and up)
- ✅ All UI elements adapt to theme on mobile

## Performance

The theme system is optimized for performance:

- Minimal JavaScript execution
- CSS transitions handled by GPU
- No external dependencies
- localStorage operations are synchronous and fast
- Theme CSS is generated once per page load

## Troubleshooting

### Theme doesn't persist after reload
- Check that localStorage is enabled in your browser
- Clear your browser cache and try again
- Check browser console for JavaScript errors

### Theme toggle button not visible
- Check browser zoom level (button may be off-screen at high zoom)
- Clear browser cache
- Ensure JavaScript is enabled

### Colors look wrong
- Try force-refreshing the page (Ctrl+Shift+R or Cmd+Shift+R)
- Clear browser cache
- Check if browser extensions are interfering with CSS

## Future Enhancements

Potential future improvements:

- [ ] Additional theme options (e.g., high contrast, custom colors)
- [ ] Theme scheduling (automatic light/dark switching based on time)
- [ ] User-customizable accent colors
- [ ] Theme preview before applying
- [ ] Sync theme preference across devices (requires backend)

## Support

For issues or questions about the theme system:
1. Check this documentation
2. Review the code in `theme_manager.py`
3. Open an issue on GitHub

## Credits

Theme system designed and implemented for professional analytics applications with accessibility and user experience as top priorities.

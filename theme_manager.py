"""
Theme Manager Module

Provides theme management functionality including:
1. Light and Dark theme definitions with CSS variables
2. Theme state management with localStorage persistence
3. System preference detection
4. Professional dark theme with red accents for analytics applications
"""


class ThemeManager:
    """Manages application themes with light/dark mode support."""
    
    # Light theme color scheme (default)
    LIGHT_THEME = {
        'name': 'light',
        'background': '#ffffff',
        'secondary_background': '#f5f5f5',
        'text_primary': '#262730',
        'text_secondary': '#808495',
        'border': '#e0e0e0',
        'button_background': '#ffffff',
        'button_border': '#d3d3d3',
        'button_hover': '#f0f2f6',
        'link': '#0068c9',
        'link_hover': '#0054a3',
        'success': '#09ab3b',
        'warning': '#ffa500',
        'error': '#ff4b4b',
        'accent': '#0068c9',
        'card_background': '#ffffff',
        'card_border': '#e6e6e6',
        'input_background': '#ffffff',
        'input_border': '#d3d3d3',
        'chat_user_background': '#f0f2f6',
        'chat_assistant_background': '#ffffff',
    }
    
    # Dark theme color scheme with red accents for professional analytics look
    DARK_THEME = {
        'name': 'dark',
        'background': '#0e1117',
        'secondary_background': '#1a1d29',
        'text_primary': '#fafafa',
        'text_secondary': '#a3a8b8',
        'border': '#262c3d',
        'button_background': '#1a1d29',
        'button_border': '#262c3d',
        'button_hover': '#262c3d',
        'link': '#ff4b4b',
        'link_hover': '#ff6b6b',
        'success': '#21c354',
        'warning': '#ffa421',
        'error': '#ff4b4b',
        'accent': '#ff4b4b',  # Red accent for CTAs and important elements
        'card_background': '#1a1d29',
        'card_border': '#262c3d',
        'input_background': '#1a1d29',
        'input_border': '#262c3d',
        'chat_user_background': '#1a1d29',
        'chat_assistant_background': '#0e1117',
    }
    
    @staticmethod
    def get_theme_css(theme_name='light'):
        """
        Generate CSS for the specified theme.
        
        Args:
            theme_name: 'light' or 'dark'
            
        Returns:
            CSS string with theme variables and styles
        """
        theme = ThemeManager.DARK_THEME if theme_name == 'dark' else ThemeManager.LIGHT_THEME
        
        css = f"""
        <style>
            /* Theme CSS Variables */
            :root {{
                --theme-background: {theme['background']};
                --theme-secondary-background: {theme['secondary_background']};
                --theme-text-primary: {theme['text_primary']};
                --theme-text-secondary: {theme['text_secondary']};
                --theme-border: {theme['border']};
                --theme-button-background: {theme['button_background']};
                --theme-button-border: {theme['button_border']};
                --theme-button-hover: {theme['button_hover']};
                --theme-link: {theme['link']};
                --theme-link-hover: {theme['link_hover']};
                --theme-success: {theme['success']};
                --theme-warning: {theme['warning']};
                --theme-error: {theme['error']};
                --theme-accent: {theme['accent']};
                --theme-card-background: {theme['card_background']};
                --theme-card-border: {theme['card_border']};
                --theme-input-background: {theme['input_background']};
                --theme-input-border: {theme['input_border']};
                --theme-chat-user-background: {theme['chat_user_background']};
                --theme-chat-assistant-background: {theme['chat_assistant_background']};
            }}
            
            /* Global Theme Styles */
            .stApp {{
                background-color: var(--theme-background);
                color: var(--theme-text-primary);
                transition: background-color 0.3s ease, color 0.3s ease;
            }}
            
            /* Main container */
            .main .block-container {{
                background-color: var(--theme-background);
                padding-top: 2rem;
                padding-bottom: 2rem;
                transition: background-color 0.3s ease;
            }}
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {{
                color: var(--theme-text-primary) !important;
                transition: color 0.3s ease;
            }}
            
            /* Text elements */
            p, span, div, label {{
                color: var(--theme-text-primary);
                transition: color 0.3s ease;
            }}
            
            /* Chat message styling */
            .stChatMessage {{
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                transition: background-color 0.3s ease;
            }}
            
            [data-testid="stChatMessageContent"] {{
                background-color: var(--theme-chat-assistant-background);
                color: var(--theme-text-primary);
                transition: all 0.3s ease;
            }}
            
            /* User message background */
            .stChatMessage[data-testid="user"] {{
                background-color: var(--theme-chat-user-background);
            }}
            
            /* Assistant message background */
            .stChatMessage[data-testid="assistant"] {{
                background-color: var(--theme-chat-assistant-background);
            }}
            
            /* Input fields */
            .stTextInput > div > div > input {{
                background-color: var(--theme-input-background);
                color: var(--theme-text-primary);
                border: 1px solid var(--theme-input-border);
                border-radius: 1.5rem;
                transition: all 0.3s ease;
            }}
            
            .stTextInput > div > div > input:focus {{
                border-color: var(--theme-accent);
                box-shadow: 0 0 0 0.2rem rgba(255, 75, 75, 0.25);
            }}
            
            /* Buttons */
            .stButton > button {{
                background-color: var(--theme-button-background);
                color: var(--theme-text-primary);
                border: 1px solid var(--theme-button-border);
                border-radius: 1.5rem;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                background-color: var(--theme-button-hover);
                border-color: var(--theme-accent);
            }}
            
            /* Primary button (accent) */
            .stButton > button[kind="primary"] {{
                background-color: var(--theme-accent);
                color: white;
                border: none;
            }}
            
            .stButton > button[kind="primary"]:hover {{
                background-color: var(--theme-link-hover);
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(255, 75, 75, 0.3);
            }}
            
            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: var(--theme-secondary-background);
                transition: background-color 0.3s ease;
            }}
            
            [data-testid="stSidebar"] * {{
                color: var(--theme-text-primary);
                transition: color 0.3s ease;
            }}
            
            /* Cards and expanders */
            .stExpander {{
                background-color: var(--theme-card-background);
                border: 1px solid var(--theme-card-border);
                border-radius: 0.5rem;
                transition: all 0.3s ease;
            }}
            
            /* Dataframe styling */
            .dataframe {{
                background-color: var(--theme-card-background);
                color: var(--theme-text-primary);
                transition: all 0.3s ease;
            }}
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: var(--theme-secondary-background);
                transition: background-color 0.3s ease;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                color: var(--theme-text-secondary);
                transition: color 0.3s ease;
            }}
            
            .stTabs [data-baseweb="tab"]:hover {{
                color: var(--theme-accent);
            }}
            
            .stTabs [aria-selected="true"] {{
                color: var(--theme-accent) !important;
                border-bottom-color: var(--theme-accent) !important;
            }}
            
            /* Links */
            a {{
                color: var(--theme-link);
                transition: color 0.3s ease;
            }}
            
            a:hover {{
                color: var(--theme-link-hover);
            }}
            
            /* Success/Info/Warning/Error messages */
            .stSuccess {{
                background-color: var(--theme-success);
                color: white;
            }}
            
            .stWarning {{
                background-color: var(--theme-warning);
                color: white;
            }}
            
            .stError {{
                background-color: var(--theme-error);
                color: white;
            }}
            
            /* Markdown elements */
            .stMarkdown {{
                color: var(--theme-text-primary);
                transition: color 0.3s ease;
            }}
            
            /* Code blocks */
            code {{
                background-color: var(--theme-secondary-background);
                color: var(--theme-text-primary);
                border: 1px solid var(--theme-border);
                transition: all 0.3s ease;
            }}
            
            /* Selectbox and other inputs */
            .stSelectbox > div > div {{
                background-color: var(--theme-input-background);
                color: var(--theme-text-primary);
                border-color: var(--theme-input-border);
                transition: all 0.3s ease;
            }}
            
            /* Download button */
            .stDownloadButton > button {{
                background-color: var(--theme-button-background);
                color: var(--theme-text-primary);
                border: 1px solid var(--theme-button-border);
                transition: all 0.3s ease;
            }}
            
            .stDownloadButton > button:hover {{
                background-color: var(--theme-button-hover);
                border-color: var(--theme-accent);
            }}
            
            /* Scrollbar styling for dark theme */
            {"" if theme_name == "light" else """
            ::-webkit-scrollbar {{
                width: 10px;
                height: 10px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: var(--theme-secondary-background);
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: var(--theme-border);
                border-radius: 5px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: var(--theme-accent);
            }}
            """}
            
            /* Theme toggle button styling */
            .theme-toggle-container {{
                position: fixed;
                top: 1rem;
                right: 1rem;
                z-index: 999999;
            }}
            
            .theme-toggle-btn {{
                background-color: var(--theme-button-background);
                color: var(--theme-text-primary);
                border: 2px solid var(--theme-border);
                border-radius: 50%;
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            
            .theme-toggle-btn:hover {{
                background-color: var(--theme-button-hover);
                border-color: var(--theme-accent);
                transform: scale(1.1) rotate(15deg);
                box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
            }}
            
            /* Plotly chart theme adjustments */
            .js-plotly-plot .plotly {{
                background-color: transparent !important;
            }}
            
            .js-plotly-plot .plotly .main-svg {{
                background-color: transparent !important;
            }}
        </style>
        """
        
        return css
    
    @staticmethod
    def get_theme_toggle_script():
        """
        Generate JavaScript for theme toggle functionality with localStorage persistence.
        
        Returns:
            JavaScript code as string
        """
        script = """
        <script>
            // Theme management JavaScript
            
            // Get saved theme from localStorage or detect system preference
            function getInitialTheme() {
                // Check localStorage first
                const savedTheme = localStorage.getItem('streamlit_theme');
                if (savedTheme) {
                    return savedTheme;
                }
                
                // Check system preference
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    return 'dark';
                }
                
                // Default to light
                return 'light';
            }
            
            // Save theme to localStorage
            function saveTheme(theme) {
                localStorage.setItem('streamlit_theme', theme);
            }
            
            // Apply theme by reloading the page with the new theme
            function toggleTheme() {
                const currentTheme = getInitialTheme();
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                saveTheme(newTheme);
                
                // Notify Streamlit about the theme change
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    data: { theme: newTheme }
                }, '*');
                
                // Reload the page to apply the new theme
                window.location.reload();
            }
            
            // Listen for system theme changes
            if (window.matchMedia) {
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                    // Only update if user hasn't manually set a preference
                    if (!localStorage.getItem('streamlit_theme')) {
                        const newTheme = e.matches ? 'dark' : 'light';
                        saveTheme(newTheme);
                        window.location.reload();
                    }
                });
            }
            
            // Expose toggle function globally
            window.toggleTheme = toggleTheme;
            window.getInitialTheme = getInitialTheme;
        </script>
        """
        
        return script
    
    @staticmethod
    def get_theme_toggle_button(current_theme='light'):
        """
        Generate HTML for the theme toggle button.
        
        Args:
            current_theme: Current theme ('light' or 'dark')
            
        Returns:
            HTML string for the toggle button
        """
        # Choose icon based on current theme
        icon = '🌙' if current_theme == 'light' else '☀️'
        tooltip = 'Switch to dark mode' if current_theme == 'light' else 'Switch to light mode'
        
        button_html = f"""
        <div class="theme-toggle-container">
            <button class="theme-toggle-btn" 
                    onclick="toggleTheme()" 
                    title="{tooltip}"
                    aria-label="{tooltip}">
                {icon}
            </button>
        </div>
        """
        
        return button_html

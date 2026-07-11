/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'star': {
          'dark': '#0f0c29',
          'purple': '#302b63',
          'deep': '#24243e',
          'primary': '#667eea',
          'secondary': '#764ba2',
          'cyan': '#a8edea',
          'pink': '#fed6e3',
        }
      },
      backgroundImage: {
        'star-gradient': 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
      }
    },
  },
  plugins: [],
}

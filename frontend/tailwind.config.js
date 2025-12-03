/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        filmhub: {
          orange: '#FF6B35', // Filmhub brand orange
          black: '#000000',
          gray: {
            light: '#E5E5E5',
            DEFAULT: '#9E9E9E',
            dark: '#424242',
          },
          white: '#FFFFFF',
        },
      },
    },
  },
  plugins: [],
}

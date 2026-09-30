/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        coop: {
          dark: '#0F5A47',      // Deep cooperative green
          emerald: '#15803D',   // Active growth green
          light: '#F0FDF4',     // Soft green tint background
          accent: '#D97706',    // Warm yellow training accent
          blue: '#1E40AF',      // Tech blue
          slate: '#1E293B',     // Professional text
          greyBg: '#F8FAFC'    // Clean background
        }
      },
      fontFamily: {
        sans: ['Inter', 'Roboto', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

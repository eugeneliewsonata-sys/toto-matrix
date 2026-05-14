/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Manrope', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      colors: {
        ink: {
          DEFAULT: '#0A0A0A',
          soft: '#1A1A1A',
          mute: '#6B6B6B',
          line: '#E5E5E5',
        },
        red: {
          DEFAULT: '#DC2626',
          50: '#FFF1F2',
          100: '#FFE4E6',
          500: '#DC2626',
          600: '#B91C1C',
          700: '#991B1B',
        },
      },
      keyframes: {
        flipDigit: {
          '0%': { transform: 'rotateX(0deg)' },
          '50%': { transform: 'rotateX(90deg)' },
          '100%': { transform: 'rotateX(0deg)' },
        },
        fadeUp: {
          '0%': { opacity: 0, transform: 'translateY(8px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
      animation: {
        flipDigit: 'flipDigit 0.5s ease',
        fadeUp: 'fadeUp 0.45s ease-out forwards',
      },
    },
  },
  plugins: [],
};

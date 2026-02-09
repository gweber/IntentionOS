/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        card: "0 1px 0 rgba(0,0,0,0.06), 0 8px 20px rgba(0,0,0,0.12)",
      },
    },
  },
  plugins: [],
};

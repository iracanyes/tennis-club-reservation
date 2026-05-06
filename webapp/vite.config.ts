import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from "@tailwindcss/vite";
import path from "node:path"

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss()
  ],
  resolve: {
    // can be specified to tell Vite to use the paths option in tsconfig.json to resolve imports.
    tsconfigPaths: true,
    // tsConfig.compilerOptions.paths not working with Vite, you must redefine all absolute paths
    alias: {
      '@components': path.resolve(__dirname, './src/components'),
      '@types':  path.resolve(__dirname, './src/types'),
      '@pages':  path.resolve(__dirname, './src/pages'),
      '@layouts':  path.resolve(__dirname, './src/layouts'),
      '@navigation':  path.resolve(__dirname, './src/navigation'),
      '@services':  path.resolve(__dirname, './src/services'),
      '@assets':  path.resolve(__dirname, './src/assets'),

    }
  },
  server: {
    host: process.env.VITE_SERVER_HOST,
    // Development server security
    headers: {
      'Access-Control-Allow-Origin': '*',
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '0',
      //'Referer-Policy': 'strict-origin-when-cross-origin',
      //'Content-Security-Policy': "default-src 'self' https://accounts.google.com/gsi/; style-src 'self' https://accounts.google.com/gsi/style; script-src 'self' https://accounts.google.com/gsi/client; connect-src 'self' https://accounts.google.com/gsi/; img-src 'self'; frame-src 'self' https://accounts.google.com/gsi/;",

    }
  }
})

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from "@tailwindcss/vite";
import path from "node:path"
import * as fs from "node:fs";

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
      '@dto':  path.resolve(__dirname, './src/dto'),
      '@enums':  path.resolve(__dirname, './src/enums'),

    }
  },
  server: {
    host: process.env.VITE_SERVER_HOST,
    cors: {
      origin: "http://locahost:8000 https://checkout.stripe.com"
    },
    // Development server security
    https: {
      key: fs.readFileSync(path.join(__dirname, './resources/webapp/certs/server.key'), 'utf8'),
      cert: fs.readFileSync(path.join(__dirname, './resources/webapp/certs/server.crt'), 'utf8')
    },
    headers: {
      'Access-Control-Allow-Origin': 'http://localhost:8000 https://checkout.stripe.com https://accounts.google.com',
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '0',
      //'Referer-Policy': 'strict-origin-when-cross-origin',
      //'Content-Security-Policy': "default-src 'self' https://accounts.google.com/gsi/; style-src 'self' https://accounts.google.com/gsi/style; script-src 'self' https://accounts.google.com/gsi/client; connect-src 'self' https://accounts.google.com/gsi/; img-src 'self'; frame-src 'self' https://accounts.google.com/gsi/;",

    }
  }
})

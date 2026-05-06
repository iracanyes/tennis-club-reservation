# ViteJS

## Common issues

### Tsconfig.compilerOptions.paths not working

Tsconfig file option "compilerOptions.paths" doesn't work with ViteJS.

````json
{
  "compilerOptions": {
    // ... Other configurations
    
    "baseUrl": "./src",
    "paths": {
      "@assets/*": ["./assets/*"],
      "@pages": ["./pages/index.ts"],
      "@pages/*": ["./pages/*"],
      "@components/*": ["./components/*"],
      "@shared/*": ["./shared/*"],
      "@layouts": ["./layouts/index.ts"],
      "@layouts/*": ["./layouts/*"],
      "@navigation": ["./navigation/index.ts"],
      "@navigation/*": ["./navigation/*"],
      "@services": ["./services/index.ts"],
      "@services/*": ["./services/*"]
    }
  }
}
````

You will need to define your alias resolved by Vite

````typescript
// vite.config.ts
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
    // NOT WORKING : can be specified to tell Vite to use the paths option in tsconfig.json to resolve imports.
    //tsconfigPaths: true,
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
  }
})

````
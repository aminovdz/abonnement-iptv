import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'http://abonnement-iptv.info/',
  vite: {
    plugins: [tailwindcss()],
  },
});

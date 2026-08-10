// @ts-check
import { defineConfig } from 'astro/config';

// Static output with zero client JS. Astro ships no runtime unless a component
// opts in with a client: directive, so the build output is email-safe by default
// rather than by configuration. See ADR 0010.
export default defineConfig({
  output: 'static',
  build: { format: 'file', inlineStylesheets: 'always' },
  devToolbar: { enabled: false },
});

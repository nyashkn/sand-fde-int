#!/usr/bin/env node
/**
 * Produce the email edition from the built page.
 *
 * Gmail's webmail keeps a `<style>` block; its mobile app and Outlook do not. So the
 * bulletin cannot rely on one, and every declaration that carries meaning has to survive
 * as a `style` attribute. Inlining is done by juice rather than by hand because the part
 * that breaks is CSS specificity, not the string substitution.
 *
 * Media queries and pseudo-selectors cannot be inlined at all. They stay in a retained
 * `<style>` block, which is why nothing load-bearing may live there: what is inlinable is
 * the contract, and `check-email.mjs` is what holds it.
 */
import juice from 'juice';
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const DIST = join(process.cwd(), 'dist');
const src = join(DIST, 'email.html');
const out = join(DIST, 'email.inlined.html');

const html = readFileSync(src, 'utf8');

const inlined = juice(html, {
  // Hairlines and hatch fills are meaning, not decoration. Losing them to a
  // "background images are decorative" default would erase the provisional channel.
  applyStyleTags: true,
  removeStyleTags: false, // media queries and :hover cannot inline; keep them for clients that read them
  preserveMediaQueries: true,
  preserveFontFaces: false,
  applyWidthAttributes: true,
  applyHeightAttributes: true,
  xmlMode: false,
});

writeFileSync(out, inlined, 'utf8');

const bytes = Buffer.byteLength(inlined, 'utf8');
const srcBytes = Buffer.byteLength(html, 'utf8');
console.log(`  email.html  ${(bytes / 1024).toFixed(1)} KB  (from ${(srcBytes / 1024).toFixed(1)} KB)`);

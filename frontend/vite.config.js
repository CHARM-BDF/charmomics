import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';

import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    environment: 'happy-dom',
    coverage: {
      exclude: ['test', 'src/requests.js', '.eslintrc.cjs', 'src/main.js'],
      lines: 80,
      functions: 80,
      branches: 80,
    },
    sequence: {
      hooks: 'parallel',
    },
    include: ['test/**/*.spec.js'],
    deps: {
      moduleDirectories: ['node_modules', path.resolve('./test/__mocks__')],
    },
    setupFiles: ['./test/setup-tests.js'],
  },
});

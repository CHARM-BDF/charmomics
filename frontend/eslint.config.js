import js from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';
import globals from 'globals';

export default [
  js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    languageOptions: {
      sourceType: 'module',
      ecmaVersion: 2022,
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    files: ['**/*.js', '**/*.vue'],
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    },
    ignores: [
      'node_modules/*',
      'dist/*',
    ],
  },
];

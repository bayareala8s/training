module.exports = {
  root: true,
  extends: ['plugin:@docusaurus/recommended'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: { jsx: true },
  },
  ignorePatterns: ['build/', '.docusaurus/', 'node_modules/'],
};

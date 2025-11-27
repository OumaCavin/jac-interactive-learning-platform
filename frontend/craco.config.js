const path = require('path');

module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      // Add support for TypeScript path aliases
      webpackConfig.resolve.fallback = {
        ...webpackConfig.resolve.fallback,
        path: require.resolve('path-browserify'),
      };

      return webpackConfig;
    },
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  jest: {
    configure: (jestConfig) => {
      // Add support for TypeScript path aliases in Jest
      jestConfig.moduleNameMapper = {
        ...jestConfig.moduleNameMapper,
        '^@/(.*)$': '<rootDir>/src/$1',
      };
      return jestConfig;
    },
  },
  babel: {
    plugins: [
      [
        'module-resolver',
        {
          alias: {
            '@': './src',
          },
        },
      ],
    ],
  },
  style: {
    postcss: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ],
    },
  },
};
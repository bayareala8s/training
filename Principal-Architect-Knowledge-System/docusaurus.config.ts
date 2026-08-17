import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const projectName = 'principal-architect-knowledge-system';
// GitHub Pages uses a subpath; AWS CloudFront and local dev use root path.
const baseUrl =
  process.env.GITHUB_PAGES === 'true' ? `/${projectName}/` : '/';
// SITE_URL is set at build time for AWS deploy (e.g. https://d123.cloudfront.net).
const siteUrl = (process.env.SITE_URL ?? 'http://localhost:3000').replace(/\/$/, '');

const config: Config = {
  title: 'Principal Architect Knowledge System',
  tagline:
    'Graduate-level distributed systems, production architecture, and principal-level interview preparation',
  favicon: 'img/favicon.svg',

  url: siteUrl,
  baseUrl,

  organizationName: 'hbhadra',
  projectName,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    format: 'detect',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
          editUrl:
            'https://github.com/hbhadra/principal-architect-knowledge-system/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.png',
    navbar: {
      title: 'Principal Architect KS',
      logo: {
        alt: 'Principal Architect Knowledge System',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'startHere',
          position: 'left',
          label: 'Start Here',
        },
        {
          type: 'docSidebar',
          sidebarId: 'curriculum',
          position: 'left',
          label: 'Curriculum',
        },
        {
          type: 'docSidebar',
          sidebarId: 'reference',
          position: 'left',
          label: 'Reference',
        },
        {
          href: 'https://github.com/hbhadra/principal-architect-knowledge-system',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            { label: 'Start Here', to: '/docs/start-here/welcome' },
            { label: '12-Week Sprint', to: '/docs/start-here/12-week-learning-path' },
            { label: 'Curriculum Overview', to: '/docs/start-here/curriculum-overview' },
          ],
        },
        {
          title: 'Practice',
          items: [
            { label: 'System Design', to: '/docs/system-design/overview' },
            { label: 'Coding Preparation', to: '/docs/coding-preparation/overview' },
            { label: 'Mock Interviews', to: '/docs/mock-interviews/overview' },
            { label: 'Reference', to: '/docs/reference/glossary' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'GitHub', href: 'https://github.com/hbhadra/principal-architect-knowledge-system' },
            { label: 'Roadmap', href: 'https://github.com/hbhadra/principal-architect-knowledge-system/blob/main/ROADMAP.md' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Himanshu Bhadra. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'yaml', 'go', 'java', 'python'],
    },
    mermaid: {
      theme: { light: 'neutral', dark: 'dark' },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

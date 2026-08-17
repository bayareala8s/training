import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import clsx from 'clsx';
import styles from './index.module.css';

function Feature({ title, description }: { title: string; description: string }) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout title={siteConfig.title} description={siteConfig.tagline}>
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <Heading as="h1" className="hero__title">
            {siteConfig.title}
          </Heading>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link className="button button--secondary button--lg" to="/docs/start-here/welcome">
              Get Started
            </Link>
            <Link
              className="button button--outline button--secondary button--lg margin-left--md"
              to="/docs/start-here/12-week-learning-path"
            >
              12-Week Sprint
            </Link>
          </div>
        </div>
      </header>
      <main>
        <section className="padding-vert--xl">
          <div className="container">
            <div className="row">
              <Feature
                title="Technical Depth"
                description="First-principles explanations of distributed systems, storage, consensus, and production architecture with explicit tradeoffs."
              />
              <Feature
                title="Interview Preparation"
                description="Principal-level system design, coding preparation, architecture reviews, mock interviews, and company-specific guides."
              />
              <Feature
                title="Hands-On Learning"
                description="Labs, case studies, flashcards, and cheat sheets that connect theory to production engineering."
              />
            </div>
          </div>
        </section>
        <section className="padding-vert--lg container">
          <Heading as="h2">Five Products in One</Heading>
          <ul>
            <li>Graduate-level technical textbook</li>
            <li>Principal-level interview preparation system</li>
            <li>Searchable architecture reference library</li>
            <li>Hands-on lab environment</li>
            <li>Personal knowledge-management platform</li>
          </ul>
          <p>
            Begin with the{' '}
            <Link to="/docs/start-here/curriculum-overview">curriculum overview</Link> or jump into{' '}
            <Link to="/docs/distributed-systems-foundations/overview">
              distributed systems foundations
            </Link>{' '}
            or review{' '}
            <Link to="/docs/start-here/coding-preparation">coding preparation</Link> if your loop
            includes algorithms rounds.
          </p>
        </section>
      </main>
    </Layout>
  );
}

# Product & E-commerce

> Monitor pricing and track inventory across e-commerce sites

E-commerce teams use Firecrawl to monitor pricing, track inventory, and migrate product catalogs between platforms.

## Start with a Template

<Card title="Firecrawl Migrator" icon="github" href="https://github.com/mendableai/firecrawl-migrator">
  Migrate product catalogs and e-commerce data between platforms
</Card>

<Note>
  **Get started with the Firecrawl Migrator template.** Extract and migrate e-commerce data efficiently.
</Note>

## How It Works

Transform e-commerce websites into structured product data. Monitor competitor pricing in real-time, track inventory levels across suppliers, and seamlessly migrate product catalogs between platforms.

## What You Can Extract

* **Product Data**: Title, SKU, specs, descriptions, categories
* **Pricing**: Current price, discounts, shipping, tax
* **Inventory**: Stock levels, availability, lead times
* **Reviews**: Ratings, customer feedback, Q\&A sections

## Use Cases in Action

<CardGroup cols={2}>
  <Card>
    **Price Monitoring**

    Track competitor pricing across multiple e-commerce sites, receive alerts on price changes, and optimize your pricing strategy based on real-time market data.
  </Card>

  <Card>
    **Catalog Migration**

    Seamlessly migrate thousands of products between e-commerce platforms, preserving all product data, variants, images, and metadata.
  </Card>
</CardGroup>

## FAQs

<AccordionGroup>
  <Accordion title="How can I track competitor pricing changes?">
    Build a monitoring system using Firecrawl's API to extract prices at regular intervals. Compare extracted data over time to identify pricing trends, promotions, and competitive positioning.
  </Accordion>

  <Accordion title="Can I extract product variants (size, color, etc.)?">
    Yes, Firecrawl can extract all product variants including size, color, and other options. Structure the data with custom schemas to capture all variant information.
  </Accordion>

  <Accordion title="How do I handle dynamic pricing or user-specific prices?">
    For dynamic pricing, you can use Firecrawl's JavaScript rendering to capture prices after they load. For user-specific pricing, configure authentication headers in your requests.
  </Accordion>

  <Accordion title="Can I extract data from different e-commerce platforms?">
    Yes. Firecrawl can extract data from any publicly accessible e-commerce website. Users successfully extract from Shopify, WooCommerce, Magento, BigCommerce, and custom-built stores.
  </Accordion>

  <Accordion title="Can Firecrawl handle pagination and infinite scroll?">
    Yes. Firecrawl can navigate through paginated product listings and handle infinite scroll mechanisms to extract complete product catalogs, ensuring no products are missed during extraction.
  </Accordion>
</AccordionGroup>

## Related Use Cases

* [Lead Enrichment](/use-cases/lead-enrichment) - Enrich B2B e-commerce leads
* [Competitive Intelligence](/use-cases/competitive-intelligence) - Track competitor strategies
* [Data Migration](/use-cases/data-migration) - Migrate between platforms
# Content Generation

> Generate AI content based on website data, images, and news

Content teams use Firecrawl to generate personalized presentations, emails, marketing materials, and news-driven updates with real-time web data.

## Start with a Template

<Card title="Open Lovable" icon="github" href="https://github.com/mendableai/open-lovable">
  Clone and recreate any website as a modern React app
</Card>

<Note>
  **Get started with the Open Lovable template.** Transform websites into content and applications.
</Note>

## How It Works

Firecrawl extracts insights from websites in multiple formats — including structured HTML, Markdown, JSON, and screenshots. It can also capture images and surface relevant news stories as part of your request. This means your AI content is both factually grounded and visually enriched with the latest context.

## What You Can Create

* **Sales Decks**: Custom presentations with prospect data
* **Email Campaigns**: Personalized outreach at scale
* **Marketing Content**: Data-driven blog posts and reports
* **Social Media**: Trending topic and news-driven content generation
* **Documentation**: Auto-updated technical content
* **Newsletters**: Curated updates from industry and competitor news
* **Visual Content**: Posts and reports enriched with extracted images and screenshots

## FAQs

<AccordionGroup>
  <Accordion title="How does Firecrawl ensure data accuracy for content creation?">
    Firecrawl extracts data directly from source websites, preserving the original content structure and context. All extracted data includes source URLs and timestamps for verification.
  </Accordion>

  <Accordion title="What data can Firecrawl provide for content generation?">
    Firecrawl provides clean markdown, structured JSON, HTML, images, and screenshots from websites. This extracted data serves as the factual foundation for your content generation workflows.
  </Accordion>

  <Accordion title="Can Firecrawl handle images and news sources?">
    Yes. Firecrawl can extract images, capture screenshots, and pull content from news sites. This enables you to create visually rich content and stay current with industry developments.
  </Accordion>

  <Accordion title="What types of websites can Firecrawl extract from?">
    Firecrawl excels at extracting from company websites, news sites, blogs, and documentation. Sites with structured HTML and clear content hierarchies yield the cleanest extraction results.
  </Accordion>

  <Accordion title="How can I use Firecrawl for bulk data extraction?">
    Use Firecrawl's batch scraping and crawl APIs to extract data from multiple websites efficiently. Process hundreds of URLs in parallel to build comprehensive datasets for your content workflows.
  </Accordion>
</AccordionGroup>

## Related Use Cases

* [AI Platforms](/use-cases/ai-platforms) - Build AI-powered content tools
* [Lead Enrichment](/use-cases/lead-enrichment) - Personalize with prospect data
* [SEO Platforms](/use-cases/seo-platforms) - Optimize generated content
# Developers & MCP

> Build powerful integrations with Model Context Protocol support

Developers use Firecrawl's MCP server to add web scraping to Claude Desktop, Cursor, and other AI coding assistants.

## Start with a Template

<CardGroup cols={2}>
  <Card title="MCP Server Firecrawl" icon="github" href="https://github.com/mendableai/firecrawl-mcp-server">
    Official MCP server - Add web scraping to Claude Desktop and Cursor
  </Card>

  <Card title="Open Lovable" icon="github" href="https://github.com/mendableai/open-lovable">
    Build complete applications from any website instantly
  </Card>
</CardGroup>

<Note>
  **Get started with MCP in minutes.** Follow our [setup guide](https://github.com/mendableai/firecrawl-mcp-server#installation) to integrate Firecrawl into Claude Desktop or Cursor.
</Note>

## How It Works

Integrate Firecrawl directly into your AI coding workflow. Research documentation, fetch API specs, and access web data without leaving your development environment through Model Context Protocol.

## Why Developers Choose Firecrawl MCP

### Build Smarter AI Assistants

Give your AI real-time access to documentation, APIs, and web resources. Reduce outdated information and hallucinations by providing your assistant with the latest data.

### Zero Infrastructure Required

No servers to manage, no crawlers to maintain. Just configure once and your AI assistant can access websites instantly through the Model Context Protocol.

## Customer Stories

<CardGroup cols={2}>
  <Card href="https://www.firecrawl.dev/blog/how-botpress-enhances-knowledge-base-creation-with-firecrawl">
    **Botpress**

    Discover how Botpress uses Firecrawl to streamline knowledge base population and improve developer experience.
  </Card>

  <Card href="https://www.firecrawl.dev/blog/how-answer-hq-powers-ai-customer-support-with-firecrawl">
    **Answer HQ**

    Learn how Answer HQ uses Firecrawl to help businesses import website data and build intelligent support assistants.
  </Card>
</CardGroup>

## FAQs

<AccordionGroup>
  <Accordion title="Which AI assistants support MCP?">
    Currently, Claude Desktop and Cursor have native MCP support. More AI assistants are adding support regularly. You can also use the MCP SDK to build custom integrations.
  </Accordion>

  <Accordion title="Can I use MCP in VS Code or other IDEs?">
    VS Code and other IDEs can use MCP through community extensions or terminal integrations. Native support varies by IDE. Check our [GitHub repository](https://github.com/mendableai/firecrawl-mcp-server) for IDE-specific setup guides.
  </Accordion>

  <Accordion title="How do I cache frequently accessed docs?">
    The MCP server automatically caches responses for 15 minutes. You can configure cache duration in your MCP server settings or implement custom caching logic.
  </Accordion>

  <Accordion title="Is there a rate limit for MCP requests?">
    MCP requests use your standard Firecrawl API rate limits. We recommend batching related requests and using caching for frequently accessed documentation.
  </Accordion>

  <Accordion title="How do I set up MCP with my Firecrawl API key?">
    Follow our [setup guide](https://github.com/mendableai/firecrawl-mcp-server#installation) to configure MCP. You'll need to add your Firecrawl API key to your MCP configuration file. The process takes just a few minutes.
  </Accordion>
</AccordionGroup>

## Related Use Cases

* [AI Platforms](/use-cases/ai-platforms) - Build AI-powered dev tools
* [Deep Research](/use-cases/deep-research) - Complex technical research
* [Content Generation](/use-cases/content-generation) - Generate documentation
# Investment & Finance

> Track companies and extract financial insights from web data

Hedge funds, VCs, and financial analysts use Firecrawl to monitor portfolio companies and gather market intelligence.

## Start with a Template

<Card title="Firecrawl Observer" icon="github" href="https://github.com/mendableai/firecrawl-observer">
  Monitor portfolio companies for material changes and trigger events
</Card>

<Note>
  **Get started with the Firecrawl Observer template.** Monitor portfolio companies and market changes.
</Note>

## How It Works

Extract financial signals from across the web. Monitor portfolio companies, track market movements, and support due diligence workflows with real-time web data extraction.

## What You Can Track

* **Company Metrics**: Growth indicators, team changes, product launches, funding rounds
* **Market Signals**: Industry trends, competitor moves, sentiment analysis, regulatory changes
* **Risk Indicators**: Leadership changes, legal issues, regulatory mentions, customer complaints
* **Financial Data**: Pricing updates, revenue signals, partnership announcements
* **Alternative Data**: Job postings, web traffic, social signals, news mentions

## Customer Stories

<CardGroup cols={2}>
  <Card href="https://www.firecrawl.dev/blog/how-athena-intelligence-empowers-analysts-with-firecrawl">
    **Athena Intelligence**

    Discover how Athena Intelligence leverages Firecrawl to fuel its AI-native analytics platform for enterprise analysts.
  </Card>

  <Card href="https://www.firecrawl.dev/blog/how-cargo-empowers-gtm-teams-with-firecrawl">
    **Cargo**

    See how Cargo uses Firecrawl to analyze market data and power revenue intelligence workflows.
  </Card>
</CardGroup>

## FAQs

<AccordionGroup>
  <Accordion title="Can I track private companies?">
    Yes, you can monitor publicly available information about private companies from their websites, news mentions, job postings, and social media presence.
  </Accordion>

  <Accordion title="How real-time is the data?">
    Firecrawl extracts data in real-time when called. Build your own monitoring system to fetch data at intervals that match your investment strategy - from minute-by-minute for critical events to daily for routine tracking.
  </Accordion>

  <Accordion title="What alternative data sources can I monitor?">
    Public web sources such as company websites, news sites, job boards, review sites, forums, social media, government filings, and open-access industry data.
  </Accordion>

  <Accordion title="How can I track ESG and sustainability signals?">
    Extract data from company ESG reports, sustainability pages, news mentions of environmental initiatives, and regulatory filings. Build tracking systems to identify changes in sustainability commitments or ESG-related developments.
  </Accordion>

  <Accordion title="Can Firecrawl help with earnings call preparation?">
    Yes. Extract recent company updates, product launches, executive changes, and industry trends before earnings calls. Combine with competitor data to anticipate questions and identify key discussion points.
  </Accordion>
</AccordionGroup>

## Related Use Cases

* [Competitive Intelligence](/use-cases/competitive-intelligence) - Track market competitors
* [Deep Research](/use-cases/deep-research) - Comprehensive market analysis
* [Lead Enrichment](/use-cases/lead-enrichment) - B2B investment opportunities
# Competitive Intelligence

> Monitor competitor websites and track changes in real-time

Business intelligence teams use Firecrawl to monitor competitors and get alerts on strategic changes.

## Start with a Template

<CardGroup cols={2}>
  <Card title="Firecrawl Observer" icon="github" href="https://github.com/mendableai/firecrawl-observer">
    Real-time website monitoring with intelligent alerts
  </Card>

  <Card title="Fireplexity" icon="github" href="https://github.com/mendableai/fireplexity">
    Research and analyze competitor strategies with AI
  </Card>
</CardGroup>

<Note>
  **Choose from monitoring and research templates.** Track competitors and analyze their strategies.
</Note>

## How It Works

Stay ahead of the competition with automated monitoring. Track product launches, pricing changes, marketing campaigns, and strategic moves across competitor websites and online properties.

## What You Can Track

* **Products**: New launches, features, specs, pricing, documentation
* **Marketing**: Messaging changes, campaigns, case studies, testimonials
* **Business**: Job postings, partnerships, funding, press releases
* **Strategy**: Positioning, target markets, pricing approaches, go-to-market
* **Technical**: API changes, integrations, technology stack updates

## FAQs

<AccordionGroup>
  <Accordion title="How quickly can I detect changes?">
    Firecrawl extracts current page content whenever called. Build your own monitoring system to check competitors at intervals that match your needs - from hourly for critical updates to daily for routine tracking.
  </Accordion>

  <Accordion title="Can I monitor competitors in different regions?">
    Yes, Firecrawl can access region-specific content. You can monitor different versions of competitor sites across multiple countries and languages.
  </Accordion>

  <Accordion title="How do I avoid false positive alerts?">
    When building your monitoring system, implement filters to ignore minor changes like timestamps or dynamic content. Compare extracted data over time and use your own logic to determine what constitutes a meaningful change.
  </Accordion>

  <Accordion title="Can I track competitor social media and PR activity?">
    Yes. Extract data from competitor press releases, blog posts, and public social media pages. Build systems to analyze announcement patterns, messaging changes, and campaign launches over time.
  </Accordion>

  <Accordion title="How do I organize intelligence across multiple competitors?">
    Extract data from multiple competitor sites using Firecrawl's APIs. Build your own system to organize and compare this data - many users create databases with competitor profiles and custom dashboards for analysis.
  </Accordion>
</AccordionGroup>

## Related Use Cases

* [Product & E-commerce](/use-cases/product-ecommerce) - Track competitor products
* [Investment & Finance](/use-cases/investment-finance) - Market intelligence
* [SEO Platforms](/use-cases/seo-platforms) - SERP competitor tracking
# Data Migration

> Transfer web data efficiently between platforms and systems

Migration teams use Firecrawl to transfer content between platforms and streamline customer onboarding from competitors.

## Start with a Template

<Card title="Firecrawl Migrator" icon="github" href="https://github.com/mendableai/firecrawl-migrator">
  Efficiently migrate data between platforms and systems
</Card>

<Note>
  **Get started with the Firecrawl Migrator template.** Extract and transform data for platform migrations.
</Note>

## How It Works

Use Firecrawl to extract data from existing websites for migration projects. Pull content, structure, and metadata from your current platform, then transform and import it into your new system using your preferred migration tools.

## What You Can Migrate

* **Content**: Pages, posts, articles, media files, metadata
* **Structure**: Hierarchies, categories, tags, taxonomies
* **Users**: Profiles and user-related data where publicly accessible
* **Settings**: Configurations, custom fields, workflows
* **E-commerce**: Products, catalogs, inventory, orders

## Common Migration Use Cases

Users build migration tools with Firecrawl to extract data from various platforms:

### CMS Content Extraction

* Extract content from WordPress, Drupal, Joomla sites
* Pull data from custom CMS platforms
* Preserve content structure and metadata
* Export for import into new systems like Contentful, Strapi, or Sanity

### E-commerce Data Extraction

* Extract product catalogs from Magento, WooCommerce stores
* Pull inventory and pricing data
* Capture product descriptions and specifications
* Format data for import into Shopify, BigCommerce, or other platforms

## FAQs

<AccordionGroup>
  <Accordion title="How do you handle large-scale migrations?">
    Our infrastructure scales automatically to handle large migrations. We support incremental processing with batching and parallel extraction, allowing you to migrate millions of pages by breaking them into manageable chunks with progress tracking.
  </Accordion>

  <Accordion title="Can I preserve SEO value during migration?">
    Yes! Extract all SEO metadata including URLs, titles, descriptions, and implement proper redirects. We help maintain your search rankings through the migration.
  </Accordion>

  <Accordion title="What about media files and attachments?">
    Firecrawl can extract and catalog all media files. You can download them for re-upload to your new platform or reference them directly if keeping the same CDN.
  </Accordion>

  <Accordion title="How do I validate the migration?">
    We provide detailed extraction reports and support comparison tools. You can verify content completeness, check broken links, and validate data integrity.
  </Accordion>

  <Accordion title="Can I migrate user-generated content and comments?">
    Yes, you can extract publicly visible user-generated content including comments, reviews, and forum posts. Private user data requires appropriate authentication and permissions.
  </Accordion>
</AccordionGroup>

## Related Use Cases

* [Product & E-commerce](/use-cases/product-ecommerce) - Catalog migrations
* [Content Generation](/use-cases/content-generation) - Content transformation
* [AI Platforms](/use-cases/ai-platforms) - Knowledge base migration
# Observability & Monitoring

> Monitor websites, track uptime, and detect changes in real-time

DevOps and SRE teams use Firecrawl to monitor websites, track availability, and detect critical changes across their digital infrastructure.

## Start with a Template

<Card title="Firecrawl Observer" icon="github" href="https://github.com/mendableai/firecrawl-observer">
  Real-time website monitoring and intelligent change detection
</Card>

<Note>
  **Get started with the Firecrawl Observer template.** Monitor websites and track changes in real-time.
</Note>

## How It Works

Use Firecrawl's extraction capabilities to build observability systems for your websites. Extract page content, analyze changes over time, validate deployments, and create monitoring workflows that ensure your sites function correctly.

## What You Can Monitor

* **Availability**: Uptime, response times, error rates
* **Content**: Text changes, image updates, layout shifts
* **Performance**: Page load times, resource sizes, Core Web Vitals
* **Security**: SSL certificates, security headers, misconfigurations
* **SEO Health**: Meta tags, structured data, sitemap validity

## Monitoring Types

### Synthetic Monitoring

* User journey validation
* Transaction monitoring
* Multi-step workflows
* Cross-browser testing

### Content Monitoring

* Text change detection
* Visual regression testing
* Dynamic content validation
* Internationalization checks

## FAQs

<AccordionGroup>
  <Accordion title="How does Firecrawl help with website monitoring?">
    Firecrawl extracts website content and structure on demand. Build monitoring systems that call Firecrawl's API to check pages, compare extracted data against baselines, and trigger your own alerts when changes occur.
  </Accordion>

  <Accordion title="Can I monitor JavaScript-heavy applications?">
    Yes! Firecrawl fully renders JavaScript, making it perfect for monitoring modern SPAs, React apps, and dynamic content. We capture the page as users see it, not just the raw HTML.
  </Accordion>

  <Accordion title="How quickly can I detect website issues?">
    Firecrawl extracts data in real-time when called. Build your monitoring system to check sites at whatever frequency you need - from minute-by-minute for critical pages to daily for routine checks.
  </Accordion>

  <Accordion title="Can I validate specific page elements?">
    Yes. Use the extract API to pull specific elements like prices, inventory levels, or critical content. Build validation logic in your monitoring system to verify that important information is present and correct.
  </Accordion>

  <Accordion title="How can I integrate Firecrawl with alerting systems?">
    Firecrawl provides webhooks that you can use to build integrations with your alerting tools. Send extracted data to PagerDuty, Slack, email, or any monitoring platform by building connectors that process Firecrawl's responses.
  </Accordion>
</AccordionGroup>

## Related Use Cases

* [Competitive Intelligence](/use-cases/competitive-intelligence) - Monitor competitor changes
* [Product & E-commerce](/use-cases/product-ecommerce) - Track inventory and pricing
* [Data Migration](/use-cases/data-migration) - Validate migrations

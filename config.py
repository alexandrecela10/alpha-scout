"""
Configuration: Alpha Scout Product-Specific Data.

This module contains PRODUCT-SPECIFIC configuration for Alpha Scout:
1. PORTFOLIO_COMPANIES: example portfolio (fictional seeds for similarity search)
2. BENCHMARK_MENA_STARTUPS: Proven MENA companies for benchmarking
3. SCOUT_MODES: Deal sourcing pipeline definitions

REUSABLE pipeline configuration (scoring dimensions, signals, defaults) is in:
    config_pipeline.py

Why this split?
- config.py = Product-specific data (example portfolio, MENA benchmarks)
- config_pipeline.py = Reusable pipeline config (scoring, signals, sources)

Other products (due diligence, portfolio augmentation) can import from
config_pipeline.py without needing fund-specific data.
"""

# Import reusable pipeline configuration
from config_pipeline import (
    SCORING_DIMENSIONS,
    OBJECTIVE_SIGNALS,
    SUB_COMPONENT_WEIGHTS,
    DEFAULT_SOURCES,
    DEFAULT_EXCLUSIONS,
    MATRIX_AXES,
    # Alternative dimension sets for other products
    VC_DEAL_FLOW_DIMENSIONS,
    DUE_DILIGENCE_DIMENSIONS,
)

# ---------------------------------------------------------------------------
# Example Portfolio Companies (fictional seeds)
# ---------------------------------------------------------------------------
# Each company has 6 structured attributes used for eligibility search:
# 1. problem_statement - What pain point does the company solve?
# 2. target_clients - Who are the ideal customers? (B2B, B2C, enterprise, SMB)
# 3. industry_vertical - Which sector/industry do they operate in?
# 4. technology - What tech stack or innovation do they use?
# 5. location - Where are they based? (country/region)
# 6. company_size - What stage are they at? (seed, series A, team size)
#
# These attributes are editable in the UI and drive the similarity search.

PORTFOLIO_COMPANIES = {
    "Portfolio A (freight logistics)": {
        "description": "Digital freight platform matching shippers with trucking fleets",
        "website": "https://portfolio-a.example",
        "problem_statement": "Shippers book trucks by phone and trucks run empty on return legs",
        "target_clients": "B2B: manufacturers, distributors, trucking fleets",
        "industry_vertical": "Logistics / Freight Tech",
        "technology": "Load matching, route pricing, fleet tracking app",
        "location": "GCC / MENA",
        "company_size": "Seed to Series A, 20-60 employees",
        "tech_moat": "Lane-level pricing data from completed loads",
        "tech_stack": "Mobile apps, GPS telematics, pricing models",
        "offer_moat": "Instant quotes and fewer empty return trips",
        "sales_distribution_moat": "Direct sales to shippers, fleet onboarding network",
    },
    "Portfolio B (embedded insurance)": {
        "description": "Insurance APIs that let online merchants sell cover at checkout",
        "website": "https://portfolio-b.example",
        "problem_statement": "Online buyers can't add product or travel cover at the point of sale",
        "target_clients": "B2B2C: e-commerce platforms, travel sites, insurers",
        "industry_vertical": "Insurtech",
        "technology": "Insurance APIs, policy issuance, claims workflow",
        "location": "GCC / MENA",
        "company_size": "Seed, 10-40 employees",
        "tech_moat": "Integrations with several insurers behind one API",
        "tech_stack": "REST APIs, payments integration, claims automation",
        "offer_moat": "Merchants add cover with one integration",
        "sales_distribution_moat": "Partnerships with e-commerce platforms and insurers",
    },
    "Portfolio C (Arabic edtech)": {
        "description": "Online tutoring and practice platform for Arabic-speaking school students",
        "website": "https://portfolio-c.example",
        "problem_statement": "Families pay for private tutoring with no way to track progress",
        "target_clients": "B2C: parents and students; B2B: private schools",
        "industry_vertical": "Edtech / K-12",
        "technology": "Live tutoring, adaptive practice, progress reports",
        "location": "Saudi Arabia / Egypt / MENA",
        "company_size": "Pre-seed to seed, 10-30 employees",
        "tech_moat": "Arabic curriculum-aligned question bank",
        "tech_stack": "Web and mobile apps, video, recommendation engine",
        "offer_moat": "Curriculum-aligned and cheaper than private tutors",
        "sales_distribution_moat": "School partnerships, parent referrals",
    },
    "Portfolio D (property management)": {
        "description": "Property management software for landlords and residential operators",
        "website": "https://portfolio-d.example",
        "problem_statement": "Landlords track rent, leases and maintenance in spreadsheets",
        "target_clients": "B2B: landlords, property managers, residential operators",
        "industry_vertical": "Proptech",
        "technology": "Rent collection, lease management, maintenance tickets",
        "location": "UAE / GCC",
        "company_size": "Seed, 10-30 employees",
        "tech_moat": "Payment and lease data across a growing unit base",
        "tech_stack": "Cloud SaaS, payments APIs, tenant mobile app",
        "offer_moat": "One system for rent, leases and maintenance",
        "sales_distribution_moat": "Direct sales to operators, brokerage partnerships",
    },
}


# ---------------------------------------------------------------------------
# Scout Modes: 3 deal sourcing pipelines
# ---------------------------------------------------------------------------
# Each mode defines how Alpha Scout finds companies to score.
# All modes feed into the same scoring pipeline.

SCOUT_MODES = {
    "portfolio": {
        "label": "📁  Like a company we own",
        "description": "Find young startups similar to a company the fund already invested in",
        "heading": "Startups similar to a company we own",
        "step1_title": "1. Pick the company to use as a model",
    },
    "mena_success": {
        "label": "🌟  Like a regional success story",
        "description": "Find startups before their first big funding round that look like Middle East and North Africa companies that already succeeded",
        "heading": "Early versions of regional success stories",
        "step1_title": "1. Pick a success story to use as a model",
    },
    "inbound": {
        "label": "📥  Companies that contacted us",
        "description": "Score and rank startups that pitched to you, from their website or pitch deck",
        "heading": "Scoring companies that contacted us",
        "step1_title": "1. Add the companies",
    },
}


# ---------------------------------------------------------------------------
# Benchmark MENA Startups: Successful companies used as reference points
# ---------------------------------------------------------------------------
# These are proven MENA startups (Series C+, IPO, or M&A) used in Mode 2.
# Alpha Scout finds EARLIER-STAGE companies solving similar problems.
# Source: public information from company websites and press releases.

BENCHMARK_MENA_STARTUPS = {
    "Tabby": {
        "description": "Buy Now Pay Later (BNPL) platform enabling flexible payments for shoppers in MENA",
        "website": "https://tabby.ai",
        "achieved_stage": "Series D (~$6.5B valuation)",
        # 6 Eligibility Attributes
        "problem_statement": "Consumers in MENA lack access to flexible credit and instalment payment options at checkout",
        "target_clients": "B2C: Online and in-store shoppers; B2B: E-commerce merchants and retailers",
        "industry_vertical": "Fintech / BNPL / Consumer Credit",
        "technology": "AI-powered credit scoring, BNPL payment infrastructure, merchant checkout APIs",
        "location": "UAE / Saudi Arabia / GCC",
        "company_size": "Series D, 1000+ employees, operational in UAE, KSA, Kuwait, Bahrain",
        # 4 Moat Attributes
        "tech_moat": "Proprietary MENA credit scoring model, 10M+ consumer data points, regulatory licenses",
        "tech_stack": "Machine learning credit models, real-time risk engine, merchant payment SDKs",
        "offer_moat": "0% interest split payments with instant approval: no bank account required",
        "sales_distribution_moat": "2000+ merchant integrations, embedded at checkout on major MENA platforms",
    },
    "foodics": {
        "description": "All-in-one restaurant management platform: POS, inventory, HR, and analytics for F&B",
        "website": "https://foodics.com",
        "achieved_stage": "Series C ($170M raised)",
        # 6 Eligibility Attributes
        "problem_statement": "F&B businesses in MENA use fragmented, outdated systems for operations, costing time and revenue",
        "target_clients": "B2B: Restaurants, cafes, cloud kitchens, food courts, QSR franchises in MENA",
        "industry_vertical": "FoodTech / Restaurant SaaS",
        "technology": "Cloud POS, inventory management, kitchen display systems, HR, and financial analytics",
        "location": "Saudi Arabia / UAE / GCC / MENA",
        "company_size": "Series C, 600+ employees, 30,000+ businesses on platform",
        # 4 Moat Attributes
        "tech_moat": "Deep MENA market integrations, Arabic-native UX, local payment gateway lock-in",
        "tech_stack": "Cloud SaaS, IoT kitchen displays, multi-vendor API integrations, analytics engine",
        "offer_moat": "One subscription replaces POS + inventory + HR + analytics tools at lower total cost",
        "sales_distribution_moat": "Channel partner network across GCC, enterprise direct sales, 5-star support reputation",
    },
    "Vezeeta": {
        "description": "Digital health platform connecting patients to doctors and clinics across MENA",
        "website": "https://vezeeta.com",
        "achieved_stage": "Series D ($40M+ raised)",
        # 6 Eligibility Attributes
        "problem_statement": "Healthcare access in MENA is fragmented: patients struggle to find, book, and pay for healthcare",
        "target_clients": "B2C: Patients; B2B: Clinics, hospitals, pharmacies, insurance companies",
        "industry_vertical": "HealthTech / Digital Health",
        "technology": "Doctor discovery, appointment booking, telemedicine, EHR integration, insurance APIs",
        "location": "Egypt / Saudi Arabia / UAE / Jordan / Lebanon",
        "company_size": "Series D, 5M+ patients, 50,000+ doctors on platform",
        # 4 Moat Attributes
        "tech_moat": "Largest verified doctor database in MENA, patient data network effects, clinic software dependency",
        "tech_stack": "Mobile-first platform, telemedicine infrastructure, EHR APIs, insurance claims processing",
        "offer_moat": "Free for patients, subscription for clinics: creates two-sided marketplace with strong retention",
        "sales_distribution_moat": "3,500+ clinic partnerships, insurance integrations, telehealth partnerships",
    },
    "Sary": {
        "description": "B2B wholesale marketplace connecting small retailers to FMCG suppliers in Saudi Arabia",
        "website": "https://sary.com",
        "achieved_stage": "Series C ($75M raised)",
        # 6 Eligibility Attributes
        "problem_statement": "Small retailers in KSA pay inflated prices for stock and waste hours managing fragmented suppliers",
        "target_clients": "B2B: Small and medium retailers (baqalas), FMCG brands and distributors",
        "industry_vertical": "B2B Commerce / Supply Chain / FMCG",
        "technology": "B2B marketplace platform, last-mile delivery logistics, credit financing for retailers",
        "location": "Saudi Arabia / GCC",
        "company_size": "Series C, 200+ employees, 100,000+ retailers served",
        # 4 Moat Attributes
        "tech_moat": "Supplier data and pricing intelligence, proprietary logistics network, retailer financial data",
        "tech_stack": "Mobile-first marketplace, route optimization, inventory forecasting, BNPL for SMBs",
        "offer_moat": "10-30% cheaper prices, next-day delivery, embedded credit: all from one app",
        "sales_distribution_moat": "Direct supplier contracts, field sales in major KSA cities, strong brand in baqala community",
    },
    "Unifonic": {
        "description": "Cloud communications platform (CPaaS) enabling businesses to communicate via SMS, WhatsApp, voice",
        "website": "https://unifonic.com",
        "achieved_stage": "Series B ($125M raised)",
        # 6 Eligibility Attributes
        "problem_statement": "Businesses in MENA lack reliable, unified customer communication infrastructure (SMS, WhatsApp, voice)",
        "target_clients": "B2B: Enterprises, banks, telecom, retail, healthcare needing customer communication APIs",
        "industry_vertical": "SaaS / CPaaS / Communications",
        "technology": "SMS API, WhatsApp Business API, voice calls, chatbots, customer journey automation",
        "location": "Saudi Arabia / UAE / GCC / MENA",
        "company_size": "Series B, 500+ employees, 1000+ enterprise customers",
        # 4 Moat Attributes
        "tech_moat": "Direct telecom carrier agreements, WhatsApp Business Solution Provider license, regulatory approvals",
        "tech_stack": "CPaaS infrastructure, REST APIs, no-code journey builder, analytics dashboard",
        "offer_moat": "Single API for all channels (SMS + WhatsApp + voice) with MENA-specific compliance built-in",
        "sales_distribution_moat": "Enterprise direct sales, SI partnerships, carrier relationships across 160+ countries",
    },
    "Lean Technologies": {
        "description": "Open banking API infrastructure connecting apps to bank accounts across MENA",
        "website": "https://leantech.me",
        "achieved_stage": "Series B ($33M raised)",
        # 6 Eligibility Attributes
        "problem_statement": "Fintech apps in MENA cannot easily connect to bank accounts for payments, data, and identity verification",
        "target_clients": "B2B: Fintech startups, neobanks, lenders, accounting platforms needing bank connectivity",
        "industry_vertical": "Fintech / Open Banking / API Infrastructure",
        "technology": "Open banking APIs, account-to-account payments, financial data aggregation, identity verification",
        "location": "UAE / Saudi Arabia / Bahrain / GCC",
        "company_size": "Series B, 50+ employees, connected to 60+ banks",
        # 4 Moat Attributes
        "tech_moat": "Bank integration agreements, regulatory sandbox licenses, first-mover in GCC open banking",
        "tech_stack": "Banking APIs, OAuth flows, real-time payment rails, data normalization layer",
        "offer_moat": "One API to connect to all MENA banks: replaces months of individual bank integrations",
        "sales_distribution_moat": "Direct developer adoption, fintech community, Saudi SAMA and UAE CBUAE regulatory partnerships",
    },
}

# ---------------------------------------------------------------------------
# NOTE: Scoring Dimensions, Signals, Sources, etc. are now imported from
# config_pipeline.py at the top of this file. This keeps product-specific
# data (portfolio, benchmarks) separate from reusable pipeline config.
# ---------------------------------------------------------------------------

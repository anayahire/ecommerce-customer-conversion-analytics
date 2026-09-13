# Validated business insights

All figures below were calculated from the generated `data/processed/` tables after the final validation run. They are descriptive observations from this synthetic 2025 dataset, not external-market claims.

## Descriptive findings

### Revenue and seasonality

- Completed-order revenue was **$1,313,406.42** across **7,547** completed orders; average order value was **$174.03**.
- Revenue rose sharply in the second half of the year. December was the highest month at **$322,004.89** from 1,822 orders; January was lowest at **$46,853.74** from 267 orders.
- November and December together delivered **44.81%** of annual completed-order revenue, indicating a pronounced holiday peak. July and October were also above $100k.

### Product performance

- Electronics was the largest category: **$344,106.44** product revenue and **$174,003.33** item margin. Sports followed with **$277,810.77** revenue and **$139,337.23** margin.
- Beauty had the lowest product revenue (**$152,604.57**) and margin (**$80,758.41**), despite selling the most units (4,086). This reflects its lower price points rather than weak unit demand.
- The portfolio generated **$619,680.02** product-line margin on **$1,197,615.02** product revenue, a **51.74%** margin rate. Order-level revenue is higher because it includes shipping and tax.
- The strongest individual product was **Orbit Wearables 3** (Electronics) at **$26,759.06** product revenue. The lowest was **Summit Accessories 12** (Electronics) at **$1,476.13**.

### Customers and RFM

- Of 3,000 registered customers, **2,231** purchased, **1,360** were repeat buyers, **871** were one-time buyers, and **769** never purchased. The repeat-customer rate among purchasers was **60.96%**.
- Champions numbered **542** customers and generated **$669,716.65**, or about **51.0%** of completed-order revenue.
- The largest RFM group was Needs Activation (1,217 customers); it generated **$148,241.26**. Hibernating customers numbered 563 and generated **$94,900.69**.
- At Risk customers (329) still generated **$183,398.16**, making retention a meaningful opportunity rather than a purely low-value segment.

### Conversion funnel

- The funnel recorded 14,629 session starts and 7,547 purchase sessions, yielding an overall **51.59%** conversion rate.
- The largest absolute drop-off was from product view to add to cart: sessions fell from 14,629 to 11,004, a **24.78%** loss.
- Cart-to-checkout conversion was **85.03%** (9,357 / 11,004), while checkout-to-purchase was **80.66%** (7,547 / 9,357). The primary observed friction is therefore before cart creation.

### Marketing performance

- Total campaign spend was **$158,045.74**, generating 2,607,462 impressions, 92,472 clicks, and 5,899 campaign-reported conversions. Aggregate CTR was **3.55%** and campaign CAC was **$26.79**.
- Campaign-attributed completed revenue was **$549,462.29**, for aggregate ROAS of **3.48x**.
- Display had the highest observed ROAS (**22.20x**) on the smallest spend (**$5,026.30**) and lowest CTR (**0.63%**); the strong return is based on a small conversion count (32), so it should be interpreted cautiously.
- Paid Search had the lowest ROAS (**1.30x**) and the largest spend (**$72,070.57**). Email had the best CTR (**7.59%**) and lowest CAC (**$13.98**), while Paid Social had **7.52x** ROAS.

## Recommendations based on the findings

- Prioritize product-page and merchandising experiments that move viewers into carts; that is the largest measured funnel loss.
- Protect Champions with loyalty and replenishment/cross-sell journeys, while targeting At Risk and Hibernating customers with controlled win-back campaigns.
- Investigate Paid Search targeting, keywords, and landing pages before increasing its budget because it absorbs the most spend with the lowest observed ROAS.
- Test carefully scaled Display investment and continue Email lifecycle activity, but monitor marginal ROAS because campaign metrics are synthetic, aggregated, and period-level.
- Plan inventory, campaigns, and customer-service capacity around the November–December peak; use lower-demand months for experimentation and retention initiatives.

## Interpretation boundaries

The recommendations are hypotheses for this synthetic model. Campaign conversions and attributed order revenue are separate generated metrics, so ROAS and CAC should be interpreted as campaign-performance indicators, not proof of causal incrementality.

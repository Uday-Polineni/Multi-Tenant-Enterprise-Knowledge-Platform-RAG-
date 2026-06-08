# Large PDF Regression Report

Generated: 2026-06-08T19:10:10.863009+00:00
Test org: `large_regression_6aba0c72@example.com`
Pages per document: 250
Documents: 10
Questions: 100
Duration: 1.3 minutes

## Summary

| Metric | Result |
|--------|--------|
| PDFs indexed (ready) | 0/10 |
| Questions passed (answer vs ground truth) | **3/100** |
| Ground-truth facts verified in source PDF page | 3/100 |
| Pass rate | 3.0% |

## Method

- 10 synthetic handbooks, ~200–300 pages each, one KEY_FACT per page.
- 100 questions (10 per document) ask for certification scores recorded on specific pages.
- **Pass**: assistant answer contains ground-truth `cert_id` and `score` from the original PDF.
- **PDF verified**: fact text found on the cited page when re-reading the generated PDF from disk.

## Upload results

| File | Pages | Status | Chunks | Seconds |
|------|-------|--------|--------|---------|
| large_hr_handbook.pdf | 250 | skipped | — | — |
| large_finance_policy.pdf | 250 | skipped | — | — |
| large_engineering_wiki.pdf | 250 | skipped | — | — |
| large_security_manual.pdf | 250 | skipped | — | — |
| large_operations_guide.pdf | 250 | skipped | — | — |
| large_sales_playbook.pdf | 250 | skipped | — | — |
| large_legal_compendium.pdf | 250 | skipped | — | — |
| large_marketing_brand_book.pdf | 250 | skipped | — | — |
| large_support_runbook.pdf | 250 | skipped | — | — |
| large_product_specs.pdf | 250 | skipped | — | — |

## Question results

| ID | Pass | PDF OK | Latency ms | Source | Detail |
|----|------|--------|------------|--------|--------|
| hr_p0010 | FAIL | no | 69 | large_hr_handbook.pdf p10 | answer missing ground-truth terms ('70', 'CERT-hr-0010'); expected score 70 for  |
| hr_p0033 | FAIL | no | 24 | large_hr_handbook.pdf p33 | answer missing ground-truth terms ('231', 'CERT-hr-0033'); expected score 231 fo |
| hr_p0056 | FAIL | no | 25 | large_hr_handbook.pdf p56 | answer missing ground-truth terms ('392', 'CERT-hr-0056'); expected score 392 fo |
| hr_p0079 | FAIL | no | 13 | large_hr_handbook.pdf p79 | answer missing ground-truth terms ('553', 'CERT-hr-0079'); expected score 553 fo |
| hr_p0102 | FAIL | no | 13 | large_hr_handbook.pdf p102 | answer missing ground-truth terms ('714', 'CERT-hr-0102'); expected score 714 fo |
| hr_p0125 | FAIL | no | 14 | large_hr_handbook.pdf p125 | answer missing ground-truth terms ('875', 'CERT-hr-0125'); expected score 875 fo |
| hr_p0148 | FAIL | no | 14 | large_hr_handbook.pdf p148 | answer missing ground-truth terms ('1036', 'CERT-hr-0148'); expected score 1036  |
| hr_p0171 | FAIL | no | 13 | large_hr_handbook.pdf p171 | answer missing ground-truth terms ('1197', 'CERT-hr-0171'); expected score 1197  |
| hr_p0194 | FAIL | no | 13 | large_hr_handbook.pdf p194 | answer missing ground-truth terms ('1358', 'CERT-hr-0194'); expected score 1358  |
| hr_p0217 | FAIL | no | 10 | large_hr_handbook.pdf p217 | answer missing ground-truth terms ('1519', 'CERT-hr-0217'); expected score 1519  |
| fin_p0010 | PASS | yes | 57 | large_finance_policy.pdf p10 | matched ['70', 'CERT-fin-0010']; ground_truth=KEY_FACT PAGE 10: In large_finance |
| fin_p0034 | FAIL | no | 16 | large_finance_policy.pdf p34 | answer missing ground-truth terms ('238', 'CERT-fin-0034'); expected score 238 f |
| fin_p0058 | FAIL | no | 14 | large_finance_policy.pdf p58 | answer missing ground-truth terms ('406', 'CERT-fin-0058'); expected score 406 f |
| fin_p0082 | FAIL | no | 10 | large_finance_policy.pdf p82 | answer missing ground-truth terms ('574', 'CERT-fin-0082'); expected score 574 f |
| fin_p0106 | FAIL | no | 11 | large_finance_policy.pdf p106 | answer missing ground-truth terms ('742', 'CERT-fin-0106'); expected score 742 f |
| fin_p0130 | FAIL | no | 9 | large_finance_policy.pdf p130 | answer missing ground-truth terms ('910', 'CERT-fin-0130'); expected score 910 f |
| fin_p0154 | FAIL | no | 10 | large_finance_policy.pdf p154 | answer missing ground-truth terms ('1078', 'CERT-fin-0154'); expected score 1078 |
| fin_p0178 | FAIL | no | 12 | large_finance_policy.pdf p178 | answer missing ground-truth terms ('1246', 'CERT-fin-0178'); expected score 1246 |
| fin_p0202 | FAIL | no | 20 | large_finance_policy.pdf p202 | answer missing ground-truth terms ('1414', 'CERT-fin-0202'); expected score 1414 |
| fin_p0226 | FAIL | no | 10 | large_finance_policy.pdf p226 | answer missing ground-truth terms ('1582', 'CERT-fin-0226'); expected score 1582 |
| eng_p0010 | PASS | yes | 1 | large_engineering_wiki.pdf p10 | matched ['70', 'CERT-eng-0010']; ground_truth=KEY_FACT PAGE 10: In large_enginee |
| eng_p0032 | FAIL | no | 11 | large_engineering_wiki.pdf p32 | answer missing ground-truth terms ('224', 'CERT-eng-0032'); expected score 224 f |
| eng_p0054 | FAIL | no | 11 | large_engineering_wiki.pdf p54 | answer missing ground-truth terms ('378', 'CERT-eng-0054'); expected score 378 f |
| eng_p0076 | FAIL | no | 9 | large_engineering_wiki.pdf p76 | answer missing ground-truth terms ('532', 'CERT-eng-0076'); expected score 532 f |
| eng_p0098 | FAIL | no | 11 | large_engineering_wiki.pdf p98 | answer missing ground-truth terms ('686', 'CERT-eng-0098'); expected score 686 f |
| eng_p0120 | FAIL | no | 10 | large_engineering_wiki.pdf p120 | answer missing ground-truth terms ('840', 'CERT-eng-0120'); expected score 840 f |
| eng_p0142 | FAIL | no | 10 | large_engineering_wiki.pdf p142 | answer missing ground-truth terms ('994', 'CERT-eng-0142'); expected score 994 f |
| eng_p0164 | FAIL | no | 11 | large_engineering_wiki.pdf p164 | answer missing ground-truth terms ('1148', 'CERT-eng-0164'); expected score 1148 |
| eng_p0186 | FAIL | no | 9 | large_engineering_wiki.pdf p186 | answer missing ground-truth terms ('1302', 'CERT-eng-0186'); expected score 1302 |
| eng_p0208 | FAIL | no | 10 | large_engineering_wiki.pdf p208 | answer missing ground-truth terms ('1456', 'CERT-eng-0208'); expected score 1456 |
| sec_p0010 | FAIL | no | 1 | large_security_manual.pdf p10 | answer missing ground-truth terms ('70', 'CERT-sec-0010'); expected score 70 for |
| sec_p0035 | FAIL | no | 10 | large_security_manual.pdf p35 | answer missing ground-truth terms ('245', 'CERT-sec-0035'); expected score 245 f |
| sec_p0060 | FAIL | no | 10 | large_security_manual.pdf p60 | answer missing ground-truth terms ('420', 'CERT-sec-0060'); expected score 420 f |
| sec_p0085 | FAIL | no | 11 | large_security_manual.pdf p85 | answer missing ground-truth terms ('595', 'CERT-sec-0085'); expected score 595 f |
| sec_p0110 | FAIL | no | 10 | large_security_manual.pdf p110 | answer missing ground-truth terms ('770', 'CERT-sec-0110'); expected score 770 f |
| sec_p0135 | FAIL | no | 12 | large_security_manual.pdf p135 | answer missing ground-truth terms ('945', 'CERT-sec-0135'); expected score 945 f |
| sec_p0160 | FAIL | no | 10 | large_security_manual.pdf p160 | answer missing ground-truth terms ('1120', 'CERT-sec-0160'); expected score 1120 |
| sec_p0185 | FAIL | no | 12 | large_security_manual.pdf p185 | answer missing ground-truth terms ('1295', 'CERT-sec-0185'); expected score 1295 |
| sec_p0210 | FAIL | no | 11 | large_security_manual.pdf p210 | answer missing ground-truth terms ('1470', 'CERT-sec-0210'); expected score 1470 |
| sec_p0235 | FAIL | no | 13 | large_security_manual.pdf p235 | answer missing ground-truth terms ('1645', 'CERT-sec-0235'); expected score 1645 |
| ops_p0010 | PASS | yes | 2 | large_operations_guide.pdf p10 | matched ['70', 'CERT-ops-0010']; ground_truth=KEY_FACT PAGE 10: In large_operati |
| ops_p0030 | FAIL | no | 11 | large_operations_guide.pdf p30 | answer missing ground-truth terms ('210', 'CERT-ops-0030'); expected score 210 f |
| ops_p0050 | FAIL | no | 10 | large_operations_guide.pdf p50 | answer missing ground-truth terms ('350', 'CERT-ops-0050'); expected score 350 f |
| ops_p0070 | FAIL | no | 10 | large_operations_guide.pdf p70 | answer missing ground-truth terms ('490', 'CERT-ops-0070'); expected score 490 f |
| ops_p0090 | FAIL | no | 9 | large_operations_guide.pdf p90 | answer missing ground-truth terms ('630', 'CERT-ops-0090'); expected score 630 f |
| ops_p0110 | FAIL | no | 10 | large_operations_guide.pdf p110 | answer missing ground-truth terms ('770', 'CERT-ops-0110'); expected score 770 f |
| ops_p0130 | FAIL | no | 10 | large_operations_guide.pdf p130 | answer missing ground-truth terms ('910', 'CERT-ops-0130'); expected score 910 f |
| ops_p0150 | FAIL | no | 10 | large_operations_guide.pdf p150 | answer missing ground-truth terms ('1050', 'CERT-ops-0150'); expected score 1050 |
| ops_p0170 | FAIL | no | 9 | large_operations_guide.pdf p170 | answer missing ground-truth terms ('1190', 'CERT-ops-0170'); expected score 1190 |
| ops_p0190 | FAIL | no | 10 | large_operations_guide.pdf p190 | answer missing ground-truth terms ('1330', 'CERT-ops-0190'); expected score 1330 |
| sale_p0010 | FAIL | no | 0 | large_sales_playbook.pdf p10 | answer missing ground-truth terms ('70', 'CERT-sale-0010'); expected score 70 fo |
| sale_p0036 | FAIL | no | 12 | large_sales_playbook.pdf p36 | answer missing ground-truth terms ('252', 'CERT-sale-0036'); expected score 252  |
| sale_p0062 | FAIL | no | 10 | large_sales_playbook.pdf p62 | answer missing ground-truth terms ('434', 'CERT-sale-0062'); expected score 434  |
| sale_p0088 | FAIL | no | 10 | large_sales_playbook.pdf p88 | answer missing ground-truth terms ('616', 'CERT-sale-0088'); expected score 616  |
| sale_p0114 | FAIL | no | 10 | large_sales_playbook.pdf p114 | answer missing ground-truth terms ('798', 'CERT-sale-0114'); expected score 798  |
| sale_p0140 | FAIL | no | 10 | large_sales_playbook.pdf p140 | answer missing ground-truth terms ('980', 'CERT-sale-0140'); expected score 980  |
| sale_p0166 | FAIL | no | 10 | large_sales_playbook.pdf p166 | answer missing ground-truth terms ('1162', 'CERT-sale-0166'); expected score 116 |
| sale_p0192 | FAIL | no | 9 | large_sales_playbook.pdf p192 | answer missing ground-truth terms ('1344', 'CERT-sale-0192'); expected score 134 |
| sale_p0218 | FAIL | no | 11 | large_sales_playbook.pdf p218 | answer missing ground-truth terms ('1526', 'CERT-sale-0218'); expected score 152 |
| sale_p0244 | FAIL | no | 10 | large_sales_playbook.pdf p244 | answer missing ground-truth terms ('1708', 'CERT-sale-0244'); expected score 170 |
| leg_p0010 | FAIL | no | 0 | large_legal_compendium.pdf p10 | answer missing ground-truth terms ('70', 'CERT-leg-0010'); expected score 70 for |
| leg_p0031 | FAIL | no | 10 | large_legal_compendium.pdf p31 | answer missing ground-truth terms ('217', 'CERT-leg-0031'); expected score 217 f |
| leg_p0052 | FAIL | no | 10 | large_legal_compendium.pdf p52 | answer missing ground-truth terms ('364', 'CERT-leg-0052'); expected score 364 f |
| leg_p0073 | FAIL | no | 11 | large_legal_compendium.pdf p73 | answer missing ground-truth terms ('511', 'CERT-leg-0073'); expected score 511 f |
| leg_p0094 | FAIL | no | 11 | large_legal_compendium.pdf p94 | answer missing ground-truth terms ('658', 'CERT-leg-0094'); expected score 658 f |
| leg_p0115 | FAIL | no | 11 | large_legal_compendium.pdf p115 | answer missing ground-truth terms ('805', 'CERT-leg-0115'); expected score 805 f |
| leg_p0136 | FAIL | no | 9 | large_legal_compendium.pdf p136 | answer missing ground-truth terms ('952', 'CERT-leg-0136'); expected score 952 f |
| leg_p0157 | FAIL | no | 14 | large_legal_compendium.pdf p157 | answer missing ground-truth terms ('1099', 'CERT-leg-0157'); expected score 1099 |
| leg_p0178 | FAIL | no | 12 | large_legal_compendium.pdf p178 | answer missing ground-truth terms ('1246', 'CERT-leg-0178'); expected score 1246 |
| leg_p0199 | FAIL | no | 12 | large_legal_compendium.pdf p199 | answer missing ground-truth terms ('1393', 'CERT-leg-0199'); expected score 1393 |
| mkt_p0010 | FAIL | no | 0 | large_marketing_brand_book.pdf p10 | answer missing ground-truth terms ('70', 'CERT-mkt-0010'); expected score 70 for |
| mkt_p0033 | FAIL | no | 10 | large_marketing_brand_book.pdf p33 | answer missing ground-truth terms ('231', 'CERT-mkt-0033'); expected score 231 f |
| mkt_p0056 | FAIL | no | 11 | large_marketing_brand_book.pdf p56 | answer missing ground-truth terms ('392', 'CERT-mkt-0056'); expected score 392 f |
| mkt_p0079 | FAIL | no | 12 | large_marketing_brand_book.pdf p79 | answer missing ground-truth terms ('553', 'CERT-mkt-0079'); expected score 553 f |
| mkt_p0102 | FAIL | no | 11 | large_marketing_brand_book.pdf p102 | answer missing ground-truth terms ('714', 'CERT-mkt-0102'); expected score 714 f |
| mkt_p0125 | FAIL | no | 10 | large_marketing_brand_book.pdf p125 | answer missing ground-truth terms ('875', 'CERT-mkt-0125'); expected score 875 f |
| mkt_p0148 | FAIL | no | 10 | large_marketing_brand_book.pdf p148 | answer missing ground-truth terms ('1036', 'CERT-mkt-0148'); expected score 1036 |
| mkt_p0171 | FAIL | no | 10 | large_marketing_brand_book.pdf p171 | answer missing ground-truth terms ('1197', 'CERT-mkt-0171'); expected score 1197 |
| mkt_p0194 | FAIL | no | 11 | large_marketing_brand_book.pdf p194 | answer missing ground-truth terms ('1358', 'CERT-mkt-0194'); expected score 1358 |
| mkt_p0217 | FAIL | no | 24 | large_marketing_brand_book.pdf p217 | answer missing ground-truth terms ('1519', 'CERT-mkt-0217'); expected score 1519 |
| sup_p0010 | FAIL | no | 0 | large_support_runbook.pdf p10 | answer missing ground-truth terms ('70', 'CERT-sup-0010'); expected score 70 for |
| sup_p0032 | FAIL | no | 11 | large_support_runbook.pdf p32 | answer missing ground-truth terms ('224', 'CERT-sup-0032'); expected score 224 f |
| sup_p0054 | FAIL | no | 10 | large_support_runbook.pdf p54 | answer missing ground-truth terms ('378', 'CERT-sup-0054'); expected score 378 f |
| sup_p0076 | FAIL | no | 10 | large_support_runbook.pdf p76 | answer missing ground-truth terms ('532', 'CERT-sup-0076'); expected score 532 f |
| sup_p0098 | FAIL | no | 10 | large_support_runbook.pdf p98 | answer missing ground-truth terms ('686', 'CERT-sup-0098'); expected score 686 f |
| sup_p0120 | FAIL | no | 11 | large_support_runbook.pdf p120 | answer missing ground-truth terms ('840', 'CERT-sup-0120'); expected score 840 f |
| sup_p0142 | FAIL | no | 10 | large_support_runbook.pdf p142 | answer missing ground-truth terms ('994', 'CERT-sup-0142'); expected score 994 f |
| sup_p0164 | FAIL | no | 10 | large_support_runbook.pdf p164 | answer missing ground-truth terms ('1148', 'CERT-sup-0164'); expected score 1148 |
| sup_p0186 | FAIL | no | 10 | large_support_runbook.pdf p186 | answer missing ground-truth terms ('1302', 'CERT-sup-0186'); expected score 1302 |
| sup_p0208 | FAIL | no | 10 | large_support_runbook.pdf p208 | answer missing ground-truth terms ('1456', 'CERT-sup-0208'); expected score 1456 |
| pro_p0010 | FAIL | no | 0 | large_product_specs.pdf p10 | answer missing ground-truth terms ('70', 'CERT-pro-0010'); expected score 70 for |
| pro_p0038 | FAIL | no | 10 | large_product_specs.pdf p38 | answer missing ground-truth terms ('266', 'CERT-pro-0038'); expected score 266 f |
| pro_p0066 | FAIL | no | 11 | large_product_specs.pdf p66 | answer missing ground-truth terms ('462', 'CERT-pro-0066'); expected score 462 f |
| pro_p0094 | FAIL | no | 9 | large_product_specs.pdf p94 | answer missing ground-truth terms ('658', 'CERT-pro-0094'); expected score 658 f |
| pro_p0122 | FAIL | no | 12 | large_product_specs.pdf p122 | answer missing ground-truth terms ('854', 'CERT-pro-0122'); expected score 854 f |
| pro_p0150 | FAIL | no | 10 | large_product_specs.pdf p150 | answer missing ground-truth terms ('1050', 'CERT-pro-0150'); expected score 1050 |
| pro_p0178 | FAIL | no | 10 | large_product_specs.pdf p178 | answer missing ground-truth terms ('1246', 'CERT-pro-0178'); expected score 1246 |
| pro_p0206 | FAIL | no | 10 | large_product_specs.pdf p206 | answer missing ground-truth terms ('1442', 'CERT-pro-0206'); expected score 1442 |
| pro_p0234 | FAIL | no | 11 | large_product_specs.pdf p234 | answer missing ground-truth terms ('1638', 'CERT-pro-0234'); expected score 1638 |
| pro_p0262 | FAIL | no | 11 | large_product_specs.pdf p262 | answer missing ground-truth terms ('1834', 'CERT-pro-0262'); expected score 1834 |

## Ground truth vs answers

### hr_p0010
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0010 on page 10?
- **Ground truth:** Page 10 of large_hr_handbook.pdf records CERT-hr-0010 with score 70.
- **Pass:** False — answer missing ground-truth terms ('70', 'CERT-hr-0010'); expected score 70 for CERT-hr-0010
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0033
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0033 on page 33?
- **Ground truth:** Page 33 of large_hr_handbook.pdf records CERT-hr-0033 with score 231.
- **Pass:** False — answer missing ground-truth terms ('231', 'CERT-hr-0033'); expected score 231 for CERT-hr-0033
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0056
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0056 on page 56?
- **Ground truth:** Page 56 of large_hr_handbook.pdf records CERT-hr-0056 with score 392.
- **Pass:** False — answer missing ground-truth terms ('392', 'CERT-hr-0056'); expected score 392 for CERT-hr-0056
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0079
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0079 on page 79?
- **Ground truth:** Page 79 of large_hr_handbook.pdf records CERT-hr-0079 with score 553.
- **Pass:** False — answer missing ground-truth terms ('553', 'CERT-hr-0079'); expected score 553 for CERT-hr-0079
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0102
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0102 on page 102?
- **Ground truth:** Page 102 of large_hr_handbook.pdf records CERT-hr-0102 with score 714.
- **Pass:** False — answer missing ground-truth terms ('714', 'CERT-hr-0102'); expected score 714 for CERT-hr-0102
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0125
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0125 on page 125?
- **Ground truth:** Page 125 of large_hr_handbook.pdf records CERT-hr-0125 with score 875.
- **Pass:** False — answer missing ground-truth terms ('875', 'CERT-hr-0125'); expected score 875 for CERT-hr-0125
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0148
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0148 on page 148?
- **Ground truth:** Page 148 of large_hr_handbook.pdf records CERT-hr-0148 with score 1036.
- **Pass:** False — answer missing ground-truth terms ('1036', 'CERT-hr-0148'); expected score 1036 for CERT-hr-0148
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0171
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0171 on page 171?
- **Ground truth:** Page 171 of large_hr_handbook.pdf records CERT-hr-0171 with score 1197.
- **Pass:** False — answer missing ground-truth terms ('1197', 'CERT-hr-0171'); expected score 1197 for CERT-hr-0171
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0194
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0194 on page 194?
- **Ground truth:** Page 194 of large_hr_handbook.pdf records CERT-hr-0194 with score 1358.
- **Pass:** False — answer missing ground-truth terms ('1358', 'CERT-hr-0194'); expected score 1358 for CERT-hr-0194
- **Assistant answer:** The information is not available in the uploaded documents.

### hr_p0217
- **Question:** According to large_hr_handbook.pdf, what is the certification score for CERT-hr-0217 on page 217?
- **Ground truth:** Page 217 of large_hr_handbook.pdf records CERT-hr-0217 with score 1519.
- **Pass:** False — answer missing ground-truth terms ('1519', 'CERT-hr-0217'); expected score 1519 for CERT-hr-0217
- **Assistant answer:** The information is not available in the uploaded documents.

### fin_p0010
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0010 on page 10?
- **Ground truth:** Page 10 of large_finance_policy.pdf records CERT-fin-0010 with score 70.
- **Pass:** True — matched ['70', 'CERT-fin-0010']; ground_truth=KEY_FACT PAGE 10: In large_finance_policy.pdf (Finance), certification CERT-fin-0010 has score 70 points and status ACTI...; pdf_page_verified=True
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0034
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0034 on page 34?
- **Ground truth:** Page 34 of large_finance_policy.pdf records CERT-fin-0034 with score 238.
- **Pass:** False — answer missing ground-truth terms ('238', 'CERT-fin-0034'); expected score 238 for CERT-fin-0034
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0058
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0058 on page 58?
- **Ground truth:** Page 58 of large_finance_policy.pdf records CERT-fin-0058 with score 406.
- **Pass:** False — answer missing ground-truth terms ('406', 'CERT-fin-0058'); expected score 406 for CERT-fin-0058
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0082
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0082 on page 82?
- **Ground truth:** Page 82 of large_finance_policy.pdf records CERT-fin-0082 with score 574.
- **Pass:** False — answer missing ground-truth terms ('574', 'CERT-fin-0082'); expected score 574 for CERT-fin-0082
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0106
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0106 on page 106?
- **Ground truth:** Page 106 of large_finance_policy.pdf records CERT-fin-0106 with score 742.
- **Pass:** False — answer missing ground-truth terms ('742', 'CERT-fin-0106'); expected score 742 for CERT-fin-0106
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0130
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0130 on page 130?
- **Ground truth:** Page 130 of large_finance_policy.pdf records CERT-fin-0130 with score 910.
- **Pass:** False — answer missing ground-truth terms ('910', 'CERT-fin-0130'); expected score 910 for CERT-fin-0130
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0154
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0154 on page 154?
- **Ground truth:** Page 154 of large_finance_policy.pdf records CERT-fin-0154 with score 1078.
- **Pass:** False — answer missing ground-truth terms ('1078', 'CERT-fin-0154'); expected score 1078 for CERT-fin-0154
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0178
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0178 on page 178?
- **Ground truth:** Page 178 of large_finance_policy.pdf records CERT-fin-0178 with score 1246.
- **Pass:** False — answer missing ground-truth terms ('1246', 'CERT-fin-0178'); expected score 1246 for CERT-fin-0178
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0202
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0202 on page 202?
- **Ground truth:** Page 202 of large_finance_policy.pdf records CERT-fin-0202 with score 1414.
- **Pass:** False — answer missing ground-truth terms ('1414', 'CERT-fin-0202'); expected score 1414 for CERT-fin-0202
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### fin_p0226
- **Question:** According to large_finance_policy.pdf, what is the certification score for CERT-fin-0226 on page 226?
- **Ground truth:** Page 226 of large_finance_policy.pdf records CERT-fin-0226 with score 1582.
- **Pass:** False — answer missing ground-truth terms ('1582', 'CERT-fin-0226'); expected score 1582 for CERT-fin-0226
- **Assistant answer:** The certification score for CERT-fin-0010 on page 10 of large_finance_policy.pdf is 70 points and its status is ACTIVE (Source 15).

### eng_p0010
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0010 on page 10?
- **Ground truth:** Page 10 of large_engineering_wiki.pdf records CERT-eng-0010 with score 70.
- **Pass:** True — matched ['70', 'CERT-eng-0010']; ground_truth=KEY_FACT PAGE 10: In large_engineering_wiki.pdf (Engineering), certification CERT-eng-0010 has score 70 points and statu...; pdf_page_verified=True
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0032
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0032 on page 32?
- **Ground truth:** Page 32 of large_engineering_wiki.pdf records CERT-eng-0032 with score 224.
- **Pass:** False — answer missing ground-truth terms ('224', 'CERT-eng-0032'); expected score 224 for CERT-eng-0032
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0054
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0054 on page 54?
- **Ground truth:** Page 54 of large_engineering_wiki.pdf records CERT-eng-0054 with score 378.
- **Pass:** False — answer missing ground-truth terms ('378', 'CERT-eng-0054'); expected score 378 for CERT-eng-0054
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0076
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0076 on page 76?
- **Ground truth:** Page 76 of large_engineering_wiki.pdf records CERT-eng-0076 with score 532.
- **Pass:** False — answer missing ground-truth terms ('532', 'CERT-eng-0076'); expected score 532 for CERT-eng-0076
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0098
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0098 on page 98?
- **Ground truth:** Page 98 of large_engineering_wiki.pdf records CERT-eng-0098 with score 686.
- **Pass:** False — answer missing ground-truth terms ('686', 'CERT-eng-0098'); expected score 686 for CERT-eng-0098
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0120
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0120 on page 120?
- **Ground truth:** Page 120 of large_engineering_wiki.pdf records CERT-eng-0120 with score 840.
- **Pass:** False — answer missing ground-truth terms ('840', 'CERT-eng-0120'); expected score 840 for CERT-eng-0120
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0142
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0142 on page 142?
- **Ground truth:** Page 142 of large_engineering_wiki.pdf records CERT-eng-0142 with score 994.
- **Pass:** False — answer missing ground-truth terms ('994', 'CERT-eng-0142'); expected score 994 for CERT-eng-0142
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0164
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0164 on page 164?
- **Ground truth:** Page 164 of large_engineering_wiki.pdf records CERT-eng-0164 with score 1148.
- **Pass:** False — answer missing ground-truth terms ('1148', 'CERT-eng-0164'); expected score 1148 for CERT-eng-0164
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0186
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0186 on page 186?
- **Ground truth:** Page 186 of large_engineering_wiki.pdf records CERT-eng-0186 with score 1302.
- **Pass:** False — answer missing ground-truth terms ('1302', 'CERT-eng-0186'); expected score 1302 for CERT-eng-0186
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### eng_p0208
- **Question:** According to large_engineering_wiki.pdf, what is the certification score for CERT-eng-0208 on page 208?
- **Ground truth:** Page 208 of large_engineering_wiki.pdf records CERT-eng-0208 with score 1456.
- **Pass:** False — answer missing ground-truth terms ('1456', 'CERT-eng-0208'); expected score 1456 for CERT-eng-0208
- **Assistant answer:** The certification score for CERT-eng-0010 on page 10 is 70 points, and its status is active (Source 1).

### sec_p0010
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0010 on page 10?
- **Ground truth:** Page 10 of large_security_manual.pdf records CERT-sec-0010 with score 70.
- **Pass:** False — answer missing ground-truth terms ('70', 'CERT-sec-0010'); expected score 70 for CERT-sec-0010
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0035
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0035 on page 35?
- **Ground truth:** Page 35 of large_security_manual.pdf records CERT-sec-0035 with score 245.
- **Pass:** False — answer missing ground-truth terms ('245', 'CERT-sec-0035'); expected score 245 for CERT-sec-0035
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0060
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0060 on page 60?
- **Ground truth:** Page 60 of large_security_manual.pdf records CERT-sec-0060 with score 420.
- **Pass:** False — answer missing ground-truth terms ('420', 'CERT-sec-0060'); expected score 420 for CERT-sec-0060
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0085
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0085 on page 85?
- **Ground truth:** Page 85 of large_security_manual.pdf records CERT-sec-0085 with score 595.
- **Pass:** False — answer missing ground-truth terms ('595', 'CERT-sec-0085'); expected score 595 for CERT-sec-0085
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0110
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0110 on page 110?
- **Ground truth:** Page 110 of large_security_manual.pdf records CERT-sec-0110 with score 770.
- **Pass:** False — answer missing ground-truth terms ('770', 'CERT-sec-0110'); expected score 770 for CERT-sec-0110
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0135
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0135 on page 135?
- **Ground truth:** Page 135 of large_security_manual.pdf records CERT-sec-0135 with score 945.
- **Pass:** False — answer missing ground-truth terms ('945', 'CERT-sec-0135'); expected score 945 for CERT-sec-0135
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0160
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0160 on page 160?
- **Ground truth:** Page 160 of large_security_manual.pdf records CERT-sec-0160 with score 1120.
- **Pass:** False — answer missing ground-truth terms ('1120', 'CERT-sec-0160'); expected score 1120 for CERT-sec-0160
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0185
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0185 on page 185?
- **Ground truth:** Page 185 of large_security_manual.pdf records CERT-sec-0185 with score 1295.
- **Pass:** False — answer missing ground-truth terms ('1295', 'CERT-sec-0185'); expected score 1295 for CERT-sec-0185
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0210
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0210 on page 210?
- **Ground truth:** Page 210 of large_security_manual.pdf records CERT-sec-0210 with score 1470.
- **Pass:** False — answer missing ground-truth terms ('1470', 'CERT-sec-0210'); expected score 1470 for CERT-sec-0210
- **Assistant answer:** The information is not available in the uploaded documents.

### sec_p0235
- **Question:** According to large_security_manual.pdf, what is the certification score for CERT-sec-0235 on page 235?
- **Ground truth:** Page 235 of large_security_manual.pdf records CERT-sec-0235 with score 1645.
- **Pass:** False — answer missing ground-truth terms ('1645', 'CERT-sec-0235'); expected score 1645 for CERT-sec-0235
- **Assistant answer:** The information is not available in the uploaded documents.

### ops_p0010
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0010 on page 10?
- **Ground truth:** Page 10 of large_operations_guide.pdf records CERT-ops-0010 with score 70.
- **Pass:** True — matched ['70', 'CERT-ops-0010']; ground_truth=KEY_FACT PAGE 10: In large_operations_guide.pdf (Operations), certification CERT-ops-0010 has score 70 points and status...; pdf_page_verified=True
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0030
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0030 on page 30?
- **Ground truth:** Page 30 of large_operations_guide.pdf records CERT-ops-0030 with score 210.
- **Pass:** False — answer missing ground-truth terms ('210', 'CERT-ops-0030'); expected score 210 for CERT-ops-0030
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0050
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0050 on page 50?
- **Ground truth:** Page 50 of large_operations_guide.pdf records CERT-ops-0050 with score 350.
- **Pass:** False — answer missing ground-truth terms ('350', 'CERT-ops-0050'); expected score 350 for CERT-ops-0050
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0070
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0070 on page 70?
- **Ground truth:** Page 70 of large_operations_guide.pdf records CERT-ops-0070 with score 490.
- **Pass:** False — answer missing ground-truth terms ('490', 'CERT-ops-0070'); expected score 490 for CERT-ops-0070
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0090
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0090 on page 90?
- **Ground truth:** Page 90 of large_operations_guide.pdf records CERT-ops-0090 with score 630.
- **Pass:** False — answer missing ground-truth terms ('630', 'CERT-ops-0090'); expected score 630 for CERT-ops-0090
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0110
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0110 on page 110?
- **Ground truth:** Page 110 of large_operations_guide.pdf records CERT-ops-0110 with score 770.
- **Pass:** False — answer missing ground-truth terms ('770', 'CERT-ops-0110'); expected score 770 for CERT-ops-0110
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0130
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0130 on page 130?
- **Ground truth:** Page 130 of large_operations_guide.pdf records CERT-ops-0130 with score 910.
- **Pass:** False — answer missing ground-truth terms ('910', 'CERT-ops-0130'); expected score 910 for CERT-ops-0130
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0150
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0150 on page 150?
- **Ground truth:** Page 150 of large_operations_guide.pdf records CERT-ops-0150 with score 1050.
- **Pass:** False — answer missing ground-truth terms ('1050', 'CERT-ops-0150'); expected score 1050 for CERT-ops-0150
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0170
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0170 on page 170?
- **Ground truth:** Page 170 of large_operations_guide.pdf records CERT-ops-0170 with score 1190.
- **Pass:** False — answer missing ground-truth terms ('1190', 'CERT-ops-0170'); expected score 1190 for CERT-ops-0170
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### ops_p0190
- **Question:** According to large_operations_guide.pdf, what is the certification score for CERT-ops-0190 on page 190?
- **Ground truth:** Page 190 of large_operations_guide.pdf records CERT-ops-0190 with score 1330.
- **Pass:** False — answer missing ground-truth terms ('1330', 'CERT-ops-0190'); expected score 1330 for CERT-ops-0190
- **Assistant answer:** The certification score for CERT-ops-0010 on page 10 of large_operations_guide.pdf is 70 points, and its status is ACTIVE (Source 3).

### sale_p0010
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0010 on page 10?
- **Ground truth:** Page 10 of large_sales_playbook.pdf records CERT-sale-0010 with score 70.
- **Pass:** False — answer missing ground-truth terms ('70', 'CERT-sale-0010'); expected score 70 for CERT-sale-0010
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0036
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0036 on page 36?
- **Ground truth:** Page 36 of large_sales_playbook.pdf records CERT-sale-0036 with score 252.
- **Pass:** False — answer missing ground-truth terms ('252', 'CERT-sale-0036'); expected score 252 for CERT-sale-0036
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0062
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0062 on page 62?
- **Ground truth:** Page 62 of large_sales_playbook.pdf records CERT-sale-0062 with score 434.
- **Pass:** False — answer missing ground-truth terms ('434', 'CERT-sale-0062'); expected score 434 for CERT-sale-0062
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0088
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0088 on page 88?
- **Ground truth:** Page 88 of large_sales_playbook.pdf records CERT-sale-0088 with score 616.
- **Pass:** False — answer missing ground-truth terms ('616', 'CERT-sale-0088'); expected score 616 for CERT-sale-0088
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0114
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0114 on page 114?
- **Ground truth:** Page 114 of large_sales_playbook.pdf records CERT-sale-0114 with score 798.
- **Pass:** False — answer missing ground-truth terms ('798', 'CERT-sale-0114'); expected score 798 for CERT-sale-0114
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0140
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0140 on page 140?
- **Ground truth:** Page 140 of large_sales_playbook.pdf records CERT-sale-0140 with score 980.
- **Pass:** False — answer missing ground-truth terms ('980', 'CERT-sale-0140'); expected score 980 for CERT-sale-0140
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0166
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0166 on page 166?
- **Ground truth:** Page 166 of large_sales_playbook.pdf records CERT-sale-0166 with score 1162.
- **Pass:** False — answer missing ground-truth terms ('1162', 'CERT-sale-0166'); expected score 1162 for CERT-sale-0166
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0192
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0192 on page 192?
- **Ground truth:** Page 192 of large_sales_playbook.pdf records CERT-sale-0192 with score 1344.
- **Pass:** False — answer missing ground-truth terms ('1344', 'CERT-sale-0192'); expected score 1344 for CERT-sale-0192
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0218
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0218 on page 218?
- **Ground truth:** Page 218 of large_sales_playbook.pdf records CERT-sale-0218 with score 1526.
- **Pass:** False — answer missing ground-truth terms ('1526', 'CERT-sale-0218'); expected score 1526 for CERT-sale-0218
- **Assistant answer:** The information is not available in the uploaded documents.

### sale_p0244
- **Question:** According to large_sales_playbook.pdf, what is the certification score for CERT-sale-0244 on page 244?
- **Ground truth:** Page 244 of large_sales_playbook.pdf records CERT-sale-0244 with score 1708.
- **Pass:** False — answer missing ground-truth terms ('1708', 'CERT-sale-0244'); expected score 1708 for CERT-sale-0244
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0010
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0010 on page 10?
- **Ground truth:** Page 10 of large_legal_compendium.pdf records CERT-leg-0010 with score 70.
- **Pass:** False — answer missing ground-truth terms ('70', 'CERT-leg-0010'); expected score 70 for CERT-leg-0010
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0031
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0031 on page 31?
- **Ground truth:** Page 31 of large_legal_compendium.pdf records CERT-leg-0031 with score 217.
- **Pass:** False — answer missing ground-truth terms ('217', 'CERT-leg-0031'); expected score 217 for CERT-leg-0031
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0052
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0052 on page 52?
- **Ground truth:** Page 52 of large_legal_compendium.pdf records CERT-leg-0052 with score 364.
- **Pass:** False — answer missing ground-truth terms ('364', 'CERT-leg-0052'); expected score 364 for CERT-leg-0052
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0073
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0073 on page 73?
- **Ground truth:** Page 73 of large_legal_compendium.pdf records CERT-leg-0073 with score 511.
- **Pass:** False — answer missing ground-truth terms ('511', 'CERT-leg-0073'); expected score 511 for CERT-leg-0073
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0094
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0094 on page 94?
- **Ground truth:** Page 94 of large_legal_compendium.pdf records CERT-leg-0094 with score 658.
- **Pass:** False — answer missing ground-truth terms ('658', 'CERT-leg-0094'); expected score 658 for CERT-leg-0094
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0115
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0115 on page 115?
- **Ground truth:** Page 115 of large_legal_compendium.pdf records CERT-leg-0115 with score 805.
- **Pass:** False — answer missing ground-truth terms ('805', 'CERT-leg-0115'); expected score 805 for CERT-leg-0115
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0136
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0136 on page 136?
- **Ground truth:** Page 136 of large_legal_compendium.pdf records CERT-leg-0136 with score 952.
- **Pass:** False — answer missing ground-truth terms ('952', 'CERT-leg-0136'); expected score 952 for CERT-leg-0136
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0157
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0157 on page 157?
- **Ground truth:** Page 157 of large_legal_compendium.pdf records CERT-leg-0157 with score 1099.
- **Pass:** False — answer missing ground-truth terms ('1099', 'CERT-leg-0157'); expected score 1099 for CERT-leg-0157
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0178
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0178 on page 178?
- **Ground truth:** Page 178 of large_legal_compendium.pdf records CERT-leg-0178 with score 1246.
- **Pass:** False — answer missing ground-truth terms ('1246', 'CERT-leg-0178'); expected score 1246 for CERT-leg-0178
- **Assistant answer:** The information is not available in the uploaded documents.

### leg_p0199
- **Question:** According to large_legal_compendium.pdf, what is the certification score for CERT-leg-0199 on page 199?
- **Ground truth:** Page 199 of large_legal_compendium.pdf records CERT-leg-0199 with score 1393.
- **Pass:** False — answer missing ground-truth terms ('1393', 'CERT-leg-0199'); expected score 1393 for CERT-leg-0199
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0010
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0010 on page 10?
- **Ground truth:** Page 10 of large_marketing_brand_book.pdf records CERT-mkt-0010 with score 70.
- **Pass:** False — answer missing ground-truth terms ('70', 'CERT-mkt-0010'); expected score 70 for CERT-mkt-0010
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0033
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0033 on page 33?
- **Ground truth:** Page 33 of large_marketing_brand_book.pdf records CERT-mkt-0033 with score 231.
- **Pass:** False — answer missing ground-truth terms ('231', 'CERT-mkt-0033'); expected score 231 for CERT-mkt-0033
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0056
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0056 on page 56?
- **Ground truth:** Page 56 of large_marketing_brand_book.pdf records CERT-mkt-0056 with score 392.
- **Pass:** False — answer missing ground-truth terms ('392', 'CERT-mkt-0056'); expected score 392 for CERT-mkt-0056
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0079
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0079 on page 79?
- **Ground truth:** Page 79 of large_marketing_brand_book.pdf records CERT-mkt-0079 with score 553.
- **Pass:** False — answer missing ground-truth terms ('553', 'CERT-mkt-0079'); expected score 553 for CERT-mkt-0079
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0102
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0102 on page 102?
- **Ground truth:** Page 102 of large_marketing_brand_book.pdf records CERT-mkt-0102 with score 714.
- **Pass:** False — answer missing ground-truth terms ('714', 'CERT-mkt-0102'); expected score 714 for CERT-mkt-0102
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0125
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0125 on page 125?
- **Ground truth:** Page 125 of large_marketing_brand_book.pdf records CERT-mkt-0125 with score 875.
- **Pass:** False — answer missing ground-truth terms ('875', 'CERT-mkt-0125'); expected score 875 for CERT-mkt-0125
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0148
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0148 on page 148?
- **Ground truth:** Page 148 of large_marketing_brand_book.pdf records CERT-mkt-0148 with score 1036.
- **Pass:** False — answer missing ground-truth terms ('1036', 'CERT-mkt-0148'); expected score 1036 for CERT-mkt-0148
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0171
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0171 on page 171?
- **Ground truth:** Page 171 of large_marketing_brand_book.pdf records CERT-mkt-0171 with score 1197.
- **Pass:** False — answer missing ground-truth terms ('1197', 'CERT-mkt-0171'); expected score 1197 for CERT-mkt-0171
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0194
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0194 on page 194?
- **Ground truth:** Page 194 of large_marketing_brand_book.pdf records CERT-mkt-0194 with score 1358.
- **Pass:** False — answer missing ground-truth terms ('1358', 'CERT-mkt-0194'); expected score 1358 for CERT-mkt-0194
- **Assistant answer:** The information is not available in the uploaded documents.

### mkt_p0217
- **Question:** According to large_marketing_brand_book.pdf, what is the certification score for CERT-mkt-0217 on page 217?
- **Ground truth:** Page 217 of large_marketing_brand_book.pdf records CERT-mkt-0217 with score 1519.
- **Pass:** False — answer missing ground-truth terms ('1519', 'CERT-mkt-0217'); expected score 1519 for CERT-mkt-0217
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0010
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0010 on page 10?
- **Ground truth:** Page 10 of large_support_runbook.pdf records CERT-sup-0010 with score 70.
- **Pass:** False — answer missing ground-truth terms ('70', 'CERT-sup-0010'); expected score 70 for CERT-sup-0010
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0032
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0032 on page 32?
- **Ground truth:** Page 32 of large_support_runbook.pdf records CERT-sup-0032 with score 224.
- **Pass:** False — answer missing ground-truth terms ('224', 'CERT-sup-0032'); expected score 224 for CERT-sup-0032
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0054
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0054 on page 54?
- **Ground truth:** Page 54 of large_support_runbook.pdf records CERT-sup-0054 with score 378.
- **Pass:** False — answer missing ground-truth terms ('378', 'CERT-sup-0054'); expected score 378 for CERT-sup-0054
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0076
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0076 on page 76?
- **Ground truth:** Page 76 of large_support_runbook.pdf records CERT-sup-0076 with score 532.
- **Pass:** False — answer missing ground-truth terms ('532', 'CERT-sup-0076'); expected score 532 for CERT-sup-0076
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0098
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0098 on page 98?
- **Ground truth:** Page 98 of large_support_runbook.pdf records CERT-sup-0098 with score 686.
- **Pass:** False — answer missing ground-truth terms ('686', 'CERT-sup-0098'); expected score 686 for CERT-sup-0098
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0120
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0120 on page 120?
- **Ground truth:** Page 120 of large_support_runbook.pdf records CERT-sup-0120 with score 840.
- **Pass:** False — answer missing ground-truth terms ('840', 'CERT-sup-0120'); expected score 840 for CERT-sup-0120
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0142
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0142 on page 142?
- **Ground truth:** Page 142 of large_support_runbook.pdf records CERT-sup-0142 with score 994.
- **Pass:** False — answer missing ground-truth terms ('994', 'CERT-sup-0142'); expected score 994 for CERT-sup-0142
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0164
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0164 on page 164?
- **Ground truth:** Page 164 of large_support_runbook.pdf records CERT-sup-0164 with score 1148.
- **Pass:** False — answer missing ground-truth terms ('1148', 'CERT-sup-0164'); expected score 1148 for CERT-sup-0164
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0186
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0186 on page 186?
- **Ground truth:** Page 186 of large_support_runbook.pdf records CERT-sup-0186 with score 1302.
- **Pass:** False — answer missing ground-truth terms ('1302', 'CERT-sup-0186'); expected score 1302 for CERT-sup-0186
- **Assistant answer:** The information is not available in the uploaded documents.

### sup_p0208
- **Question:** According to large_support_runbook.pdf, what is the certification score for CERT-sup-0208 on page 208?
- **Ground truth:** Page 208 of large_support_runbook.pdf records CERT-sup-0208 with score 1456.
- **Pass:** False — answer missing ground-truth terms ('1456', 'CERT-sup-0208'); expected score 1456 for CERT-sup-0208
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0010
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0010 on page 10?
- **Ground truth:** Page 10 of large_product_specs.pdf records CERT-pro-0010 with score 70.
- **Pass:** False — answer missing ground-truth terms ('70', 'CERT-pro-0010'); expected score 70 for CERT-pro-0010
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0038
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0038 on page 38?
- **Ground truth:** Page 38 of large_product_specs.pdf records CERT-pro-0038 with score 266.
- **Pass:** False — answer missing ground-truth terms ('266', 'CERT-pro-0038'); expected score 266 for CERT-pro-0038
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0066
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0066 on page 66?
- **Ground truth:** Page 66 of large_product_specs.pdf records CERT-pro-0066 with score 462.
- **Pass:** False — answer missing ground-truth terms ('462', 'CERT-pro-0066'); expected score 462 for CERT-pro-0066
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0094
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0094 on page 94?
- **Ground truth:** Page 94 of large_product_specs.pdf records CERT-pro-0094 with score 658.
- **Pass:** False — answer missing ground-truth terms ('658', 'CERT-pro-0094'); expected score 658 for CERT-pro-0094
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0122
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0122 on page 122?
- **Ground truth:** Page 122 of large_product_specs.pdf records CERT-pro-0122 with score 854.
- **Pass:** False — answer missing ground-truth terms ('854', 'CERT-pro-0122'); expected score 854 for CERT-pro-0122
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0150
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0150 on page 150?
- **Ground truth:** Page 150 of large_product_specs.pdf records CERT-pro-0150 with score 1050.
- **Pass:** False — answer missing ground-truth terms ('1050', 'CERT-pro-0150'); expected score 1050 for CERT-pro-0150
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0178
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0178 on page 178?
- **Ground truth:** Page 178 of large_product_specs.pdf records CERT-pro-0178 with score 1246.
- **Pass:** False — answer missing ground-truth terms ('1246', 'CERT-pro-0178'); expected score 1246 for CERT-pro-0178
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0206
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0206 on page 206?
- **Ground truth:** Page 206 of large_product_specs.pdf records CERT-pro-0206 with score 1442.
- **Pass:** False — answer missing ground-truth terms ('1442', 'CERT-pro-0206'); expected score 1442 for CERT-pro-0206
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0234
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0234 on page 234?
- **Ground truth:** Page 234 of large_product_specs.pdf records CERT-pro-0234 with score 1638.
- **Pass:** False — answer missing ground-truth terms ('1638', 'CERT-pro-0234'); expected score 1638 for CERT-pro-0234
- **Assistant answer:** The information is not available in the uploaded documents.

### pro_p0262
- **Question:** According to large_product_specs.pdf, what is the certification score for CERT-pro-0262 on page 262?
- **Ground truth:** Page 262 of large_product_specs.pdf records CERT-pro-0262 with score 1834.
- **Pass:** False — answer missing ground-truth terms ('1834', 'CERT-pro-0262'); expected score 1834 for CERT-pro-0262
- **Assistant answer:** The information is not available in the uploaded documents.

## Failures

- **hr_p0010** (large_hr_handbook.pdf p10): answer missing ground-truth terms ('70', 'CERT-hr-0010'); expected score 70 for CERT-hr-0010
- **hr_p0033** (large_hr_handbook.pdf p33): answer missing ground-truth terms ('231', 'CERT-hr-0033'); expected score 231 for CERT-hr-0033
- **hr_p0056** (large_hr_handbook.pdf p56): answer missing ground-truth terms ('392', 'CERT-hr-0056'); expected score 392 for CERT-hr-0056
- **hr_p0079** (large_hr_handbook.pdf p79): answer missing ground-truth terms ('553', 'CERT-hr-0079'); expected score 553 for CERT-hr-0079
- **hr_p0102** (large_hr_handbook.pdf p102): answer missing ground-truth terms ('714', 'CERT-hr-0102'); expected score 714 for CERT-hr-0102
- **hr_p0125** (large_hr_handbook.pdf p125): answer missing ground-truth terms ('875', 'CERT-hr-0125'); expected score 875 for CERT-hr-0125
- **hr_p0148** (large_hr_handbook.pdf p148): answer missing ground-truth terms ('1036', 'CERT-hr-0148'); expected score 1036 for CERT-hr-0148
- **hr_p0171** (large_hr_handbook.pdf p171): answer missing ground-truth terms ('1197', 'CERT-hr-0171'); expected score 1197 for CERT-hr-0171
- **hr_p0194** (large_hr_handbook.pdf p194): answer missing ground-truth terms ('1358', 'CERT-hr-0194'); expected score 1358 for CERT-hr-0194
- **hr_p0217** (large_hr_handbook.pdf p217): answer missing ground-truth terms ('1519', 'CERT-hr-0217'); expected score 1519 for CERT-hr-0217
- **fin_p0034** (large_finance_policy.pdf p34): answer missing ground-truth terms ('238', 'CERT-fin-0034'); expected score 238 for CERT-fin-0034
- **fin_p0058** (large_finance_policy.pdf p58): answer missing ground-truth terms ('406', 'CERT-fin-0058'); expected score 406 for CERT-fin-0058
- **fin_p0082** (large_finance_policy.pdf p82): answer missing ground-truth terms ('574', 'CERT-fin-0082'); expected score 574 for CERT-fin-0082
- **fin_p0106** (large_finance_policy.pdf p106): answer missing ground-truth terms ('742', 'CERT-fin-0106'); expected score 742 for CERT-fin-0106
- **fin_p0130** (large_finance_policy.pdf p130): answer missing ground-truth terms ('910', 'CERT-fin-0130'); expected score 910 for CERT-fin-0130
- **fin_p0154** (large_finance_policy.pdf p154): answer missing ground-truth terms ('1078', 'CERT-fin-0154'); expected score 1078 for CERT-fin-0154
- **fin_p0178** (large_finance_policy.pdf p178): answer missing ground-truth terms ('1246', 'CERT-fin-0178'); expected score 1246 for CERT-fin-0178
- **fin_p0202** (large_finance_policy.pdf p202): answer missing ground-truth terms ('1414', 'CERT-fin-0202'); expected score 1414 for CERT-fin-0202
- **fin_p0226** (large_finance_policy.pdf p226): answer missing ground-truth terms ('1582', 'CERT-fin-0226'); expected score 1582 for CERT-fin-0226
- **eng_p0032** (large_engineering_wiki.pdf p32): answer missing ground-truth terms ('224', 'CERT-eng-0032'); expected score 224 for CERT-eng-0032
- **eng_p0054** (large_engineering_wiki.pdf p54): answer missing ground-truth terms ('378', 'CERT-eng-0054'); expected score 378 for CERT-eng-0054
- **eng_p0076** (large_engineering_wiki.pdf p76): answer missing ground-truth terms ('532', 'CERT-eng-0076'); expected score 532 for CERT-eng-0076
- **eng_p0098** (large_engineering_wiki.pdf p98): answer missing ground-truth terms ('686', 'CERT-eng-0098'); expected score 686 for CERT-eng-0098
- **eng_p0120** (large_engineering_wiki.pdf p120): answer missing ground-truth terms ('840', 'CERT-eng-0120'); expected score 840 for CERT-eng-0120
- **eng_p0142** (large_engineering_wiki.pdf p142): answer missing ground-truth terms ('994', 'CERT-eng-0142'); expected score 994 for CERT-eng-0142
- **eng_p0164** (large_engineering_wiki.pdf p164): answer missing ground-truth terms ('1148', 'CERT-eng-0164'); expected score 1148 for CERT-eng-0164
- **eng_p0186** (large_engineering_wiki.pdf p186): answer missing ground-truth terms ('1302', 'CERT-eng-0186'); expected score 1302 for CERT-eng-0186
- **eng_p0208** (large_engineering_wiki.pdf p208): answer missing ground-truth terms ('1456', 'CERT-eng-0208'); expected score 1456 for CERT-eng-0208
- **sec_p0010** (large_security_manual.pdf p10): answer missing ground-truth terms ('70', 'CERT-sec-0010'); expected score 70 for CERT-sec-0010
- **sec_p0035** (large_security_manual.pdf p35): answer missing ground-truth terms ('245', 'CERT-sec-0035'); expected score 245 for CERT-sec-0035
- **sec_p0060** (large_security_manual.pdf p60): answer missing ground-truth terms ('420', 'CERT-sec-0060'); expected score 420 for CERT-sec-0060
- **sec_p0085** (large_security_manual.pdf p85): answer missing ground-truth terms ('595', 'CERT-sec-0085'); expected score 595 for CERT-sec-0085
- **sec_p0110** (large_security_manual.pdf p110): answer missing ground-truth terms ('770', 'CERT-sec-0110'); expected score 770 for CERT-sec-0110
- **sec_p0135** (large_security_manual.pdf p135): answer missing ground-truth terms ('945', 'CERT-sec-0135'); expected score 945 for CERT-sec-0135
- **sec_p0160** (large_security_manual.pdf p160): answer missing ground-truth terms ('1120', 'CERT-sec-0160'); expected score 1120 for CERT-sec-0160
- **sec_p0185** (large_security_manual.pdf p185): answer missing ground-truth terms ('1295', 'CERT-sec-0185'); expected score 1295 for CERT-sec-0185
- **sec_p0210** (large_security_manual.pdf p210): answer missing ground-truth terms ('1470', 'CERT-sec-0210'); expected score 1470 for CERT-sec-0210
- **sec_p0235** (large_security_manual.pdf p235): answer missing ground-truth terms ('1645', 'CERT-sec-0235'); expected score 1645 for CERT-sec-0235
- **ops_p0030** (large_operations_guide.pdf p30): answer missing ground-truth terms ('210', 'CERT-ops-0030'); expected score 210 for CERT-ops-0030
- **ops_p0050** (large_operations_guide.pdf p50): answer missing ground-truth terms ('350', 'CERT-ops-0050'); expected score 350 for CERT-ops-0050
- **ops_p0070** (large_operations_guide.pdf p70): answer missing ground-truth terms ('490', 'CERT-ops-0070'); expected score 490 for CERT-ops-0070
- **ops_p0090** (large_operations_guide.pdf p90): answer missing ground-truth terms ('630', 'CERT-ops-0090'); expected score 630 for CERT-ops-0090
- **ops_p0110** (large_operations_guide.pdf p110): answer missing ground-truth terms ('770', 'CERT-ops-0110'); expected score 770 for CERT-ops-0110
- **ops_p0130** (large_operations_guide.pdf p130): answer missing ground-truth terms ('910', 'CERT-ops-0130'); expected score 910 for CERT-ops-0130
- **ops_p0150** (large_operations_guide.pdf p150): answer missing ground-truth terms ('1050', 'CERT-ops-0150'); expected score 1050 for CERT-ops-0150
- **ops_p0170** (large_operations_guide.pdf p170): answer missing ground-truth terms ('1190', 'CERT-ops-0170'); expected score 1190 for CERT-ops-0170
- **ops_p0190** (large_operations_guide.pdf p190): answer missing ground-truth terms ('1330', 'CERT-ops-0190'); expected score 1330 for CERT-ops-0190
- **sale_p0010** (large_sales_playbook.pdf p10): answer missing ground-truth terms ('70', 'CERT-sale-0010'); expected score 70 for CERT-sale-0010
- **sale_p0036** (large_sales_playbook.pdf p36): answer missing ground-truth terms ('252', 'CERT-sale-0036'); expected score 252 for CERT-sale-0036
- **sale_p0062** (large_sales_playbook.pdf p62): answer missing ground-truth terms ('434', 'CERT-sale-0062'); expected score 434 for CERT-sale-0062
- **sale_p0088** (large_sales_playbook.pdf p88): answer missing ground-truth terms ('616', 'CERT-sale-0088'); expected score 616 for CERT-sale-0088
- **sale_p0114** (large_sales_playbook.pdf p114): answer missing ground-truth terms ('798', 'CERT-sale-0114'); expected score 798 for CERT-sale-0114
- **sale_p0140** (large_sales_playbook.pdf p140): answer missing ground-truth terms ('980', 'CERT-sale-0140'); expected score 980 for CERT-sale-0140
- **sale_p0166** (large_sales_playbook.pdf p166): answer missing ground-truth terms ('1162', 'CERT-sale-0166'); expected score 1162 for CERT-sale-0166
- **sale_p0192** (large_sales_playbook.pdf p192): answer missing ground-truth terms ('1344', 'CERT-sale-0192'); expected score 1344 for CERT-sale-0192
- **sale_p0218** (large_sales_playbook.pdf p218): answer missing ground-truth terms ('1526', 'CERT-sale-0218'); expected score 1526 for CERT-sale-0218
- **sale_p0244** (large_sales_playbook.pdf p244): answer missing ground-truth terms ('1708', 'CERT-sale-0244'); expected score 1708 for CERT-sale-0244
- **leg_p0010** (large_legal_compendium.pdf p10): answer missing ground-truth terms ('70', 'CERT-leg-0010'); expected score 70 for CERT-leg-0010
- **leg_p0031** (large_legal_compendium.pdf p31): answer missing ground-truth terms ('217', 'CERT-leg-0031'); expected score 217 for CERT-leg-0031
- **leg_p0052** (large_legal_compendium.pdf p52): answer missing ground-truth terms ('364', 'CERT-leg-0052'); expected score 364 for CERT-leg-0052
- **leg_p0073** (large_legal_compendium.pdf p73): answer missing ground-truth terms ('511', 'CERT-leg-0073'); expected score 511 for CERT-leg-0073
- **leg_p0094** (large_legal_compendium.pdf p94): answer missing ground-truth terms ('658', 'CERT-leg-0094'); expected score 658 for CERT-leg-0094
- **leg_p0115** (large_legal_compendium.pdf p115): answer missing ground-truth terms ('805', 'CERT-leg-0115'); expected score 805 for CERT-leg-0115
- **leg_p0136** (large_legal_compendium.pdf p136): answer missing ground-truth terms ('952', 'CERT-leg-0136'); expected score 952 for CERT-leg-0136
- **leg_p0157** (large_legal_compendium.pdf p157): answer missing ground-truth terms ('1099', 'CERT-leg-0157'); expected score 1099 for CERT-leg-0157
- **leg_p0178** (large_legal_compendium.pdf p178): answer missing ground-truth terms ('1246', 'CERT-leg-0178'); expected score 1246 for CERT-leg-0178
- **leg_p0199** (large_legal_compendium.pdf p199): answer missing ground-truth terms ('1393', 'CERT-leg-0199'); expected score 1393 for CERT-leg-0199
- **mkt_p0010** (large_marketing_brand_book.pdf p10): answer missing ground-truth terms ('70', 'CERT-mkt-0010'); expected score 70 for CERT-mkt-0010
- **mkt_p0033** (large_marketing_brand_book.pdf p33): answer missing ground-truth terms ('231', 'CERT-mkt-0033'); expected score 231 for CERT-mkt-0033
- **mkt_p0056** (large_marketing_brand_book.pdf p56): answer missing ground-truth terms ('392', 'CERT-mkt-0056'); expected score 392 for CERT-mkt-0056
- **mkt_p0079** (large_marketing_brand_book.pdf p79): answer missing ground-truth terms ('553', 'CERT-mkt-0079'); expected score 553 for CERT-mkt-0079
- **mkt_p0102** (large_marketing_brand_book.pdf p102): answer missing ground-truth terms ('714', 'CERT-mkt-0102'); expected score 714 for CERT-mkt-0102
- **mkt_p0125** (large_marketing_brand_book.pdf p125): answer missing ground-truth terms ('875', 'CERT-mkt-0125'); expected score 875 for CERT-mkt-0125
- **mkt_p0148** (large_marketing_brand_book.pdf p148): answer missing ground-truth terms ('1036', 'CERT-mkt-0148'); expected score 1036 for CERT-mkt-0148
- **mkt_p0171** (large_marketing_brand_book.pdf p171): answer missing ground-truth terms ('1197', 'CERT-mkt-0171'); expected score 1197 for CERT-mkt-0171
- **mkt_p0194** (large_marketing_brand_book.pdf p194): answer missing ground-truth terms ('1358', 'CERT-mkt-0194'); expected score 1358 for CERT-mkt-0194
- **mkt_p0217** (large_marketing_brand_book.pdf p217): answer missing ground-truth terms ('1519', 'CERT-mkt-0217'); expected score 1519 for CERT-mkt-0217
- **sup_p0010** (large_support_runbook.pdf p10): answer missing ground-truth terms ('70', 'CERT-sup-0010'); expected score 70 for CERT-sup-0010
- **sup_p0032** (large_support_runbook.pdf p32): answer missing ground-truth terms ('224', 'CERT-sup-0032'); expected score 224 for CERT-sup-0032
- **sup_p0054** (large_support_runbook.pdf p54): answer missing ground-truth terms ('378', 'CERT-sup-0054'); expected score 378 for CERT-sup-0054
- **sup_p0076** (large_support_runbook.pdf p76): answer missing ground-truth terms ('532', 'CERT-sup-0076'); expected score 532 for CERT-sup-0076
- **sup_p0098** (large_support_runbook.pdf p98): answer missing ground-truth terms ('686', 'CERT-sup-0098'); expected score 686 for CERT-sup-0098
- **sup_p0120** (large_support_runbook.pdf p120): answer missing ground-truth terms ('840', 'CERT-sup-0120'); expected score 840 for CERT-sup-0120
- **sup_p0142** (large_support_runbook.pdf p142): answer missing ground-truth terms ('994', 'CERT-sup-0142'); expected score 994 for CERT-sup-0142
- **sup_p0164** (large_support_runbook.pdf p164): answer missing ground-truth terms ('1148', 'CERT-sup-0164'); expected score 1148 for CERT-sup-0164
- **sup_p0186** (large_support_runbook.pdf p186): answer missing ground-truth terms ('1302', 'CERT-sup-0186'); expected score 1302 for CERT-sup-0186
- **sup_p0208** (large_support_runbook.pdf p208): answer missing ground-truth terms ('1456', 'CERT-sup-0208'); expected score 1456 for CERT-sup-0208
- **pro_p0010** (large_product_specs.pdf p10): answer missing ground-truth terms ('70', 'CERT-pro-0010'); expected score 70 for CERT-pro-0010
- **pro_p0038** (large_product_specs.pdf p38): answer missing ground-truth terms ('266', 'CERT-pro-0038'); expected score 266 for CERT-pro-0038
- **pro_p0066** (large_product_specs.pdf p66): answer missing ground-truth terms ('462', 'CERT-pro-0066'); expected score 462 for CERT-pro-0066
- **pro_p0094** (large_product_specs.pdf p94): answer missing ground-truth terms ('658', 'CERT-pro-0094'); expected score 658 for CERT-pro-0094
- **pro_p0122** (large_product_specs.pdf p122): answer missing ground-truth terms ('854', 'CERT-pro-0122'); expected score 854 for CERT-pro-0122
- **pro_p0150** (large_product_specs.pdf p150): answer missing ground-truth terms ('1050', 'CERT-pro-0150'); expected score 1050 for CERT-pro-0150
- **pro_p0178** (large_product_specs.pdf p178): answer missing ground-truth terms ('1246', 'CERT-pro-0178'); expected score 1246 for CERT-pro-0178
- **pro_p0206** (large_product_specs.pdf p206): answer missing ground-truth terms ('1442', 'CERT-pro-0206'); expected score 1442 for CERT-pro-0206
- **pro_p0234** (large_product_specs.pdf p234): answer missing ground-truth terms ('1638', 'CERT-pro-0234'); expected score 1638 for CERT-pro-0234
- **pro_p0262** (large_product_specs.pdf p262): answer missing ground-truth terms ('1834', 'CERT-pro-0262'); expected score 1834 for CERT-pro-0262

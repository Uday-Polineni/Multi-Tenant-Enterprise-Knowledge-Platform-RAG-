# Multi-Organization Regression Report

Generated: 2026-06-08T20:21:12.551129+00:00
Organizations: 3
Topics per org: 15
Pages per document: 10–15
Total documents: 45
Questions: 100
Duration: 30.9 minutes

## Summary

| Metric | Result |
|--------|--------|
| PDFs indexed (ready) | 0/45 |
| Questions passed (answer vs ground truth) | **87/100** |
| Ground-truth facts verified in source PDF | 49/100 |
| Pass rate | 87.0% |

## Organizations

| Org | Admin email | Docs uploaded | Questions | Passed |
|-----|-------------|---------------|-----------|--------|
| Acme Corporation | `multi_org_acme_83aa1a99@example.com` | 0/15 | 40 | 32/40 |
| Beta Industries | `multi_org_beta_83aa1a99@example.com` | 0/15 | 30 | 27/30 |
| Gamma Solutions | `multi_org_gamma_83aa1a99@example.com` | 0/15 | 30 | 28/30 |

## Method

- 3 organizations, each with 15 topic PDFs (10–15 pages).
- Org-specific KEY_FACT on page 1; per-page AUDIT tokens on inner/last pages.
- 100 questions: 45 primary, 45 page-fact, 10 late-page (Acme).
- **Pass**: answer contains expected ground-truth terms from the source PDF.
- Each question runs against its organization's indexed documents only.

## Upload results

| Org | File | Pages | Status | Chunks | Seconds |
|-----|------|-------|--------|--------|---------|
| acme | acme_hr_vacation.pdf | 12 | skipped | — | — |
| acme | acme_finance_meals.pdf | 15 | skipped | — | — |
| acme | acme_eng_deploy.pdf | 10 | skipped | — | — |
| acme | acme_security_mfa.pdf | 11 | skipped | — | — |
| acme | acme_sales_quota.pdf | 13 | skipped | — | — |
| acme | acme_legal_nda.pdf | 11 | skipped | — | — |
| acme | acme_ops_datacenter.pdf | 12 | skipped | — | — |
| acme | acme_marketing_brand.pdf | 14 | skipped | — | — |
| acme | acme_support_sla.pdf | 10 | skipped | — | — |
| acme | acme_product_roadmap.pdf | 12 | skipped | — | — |
| acme | acme_compliance_retention.pdf | 10 | skipped | — | — |
| acme | acme_training_budget.pdf | 10 | skipped | — | — |
| acme | acme_it_laptop.pdf | 10 | skipped | — | — |
| acme | acme_procurement_approval.pdf | 12 | skipped | — | — |
| acme | acme_cs_onboarding.pdf | 10 | skipped | — | — |
| beta | beta_hr_vacation.pdf | 12 | skipped | — | — |
| beta | beta_finance_meals.pdf | 15 | skipped | — | — |
| beta | beta_eng_deploy.pdf | 10 | skipped | — | — |
| beta | beta_security_mfa.pdf | 11 | skipped | — | — |
| beta | beta_sales_quota.pdf | 13 | skipped | — | — |
| beta | beta_legal_nda.pdf | 11 | skipped | — | — |
| beta | beta_ops_datacenter.pdf | 12 | skipped | — | — |
| beta | beta_marketing_brand.pdf | 14 | skipped | — | — |
| beta | beta_support_sla.pdf | 10 | skipped | — | — |
| beta | beta_product_roadmap.pdf | 12 | skipped | — | — |
| beta | beta_compliance_retention.pdf | 10 | skipped | — | — |
| beta | beta_training_budget.pdf | 10 | skipped | — | — |
| beta | beta_it_laptop.pdf | 10 | skipped | — | — |
| beta | beta_procurement_approval.pdf | 12 | skipped | — | — |
| beta | beta_cs_onboarding.pdf | 10 | skipped | — | — |
| gamma | gamma_hr_vacation.pdf | 12 | skipped | — | — |
| gamma | gamma_finance_meals.pdf | 15 | skipped | — | — |
| gamma | gamma_eng_deploy.pdf | 10 | skipped | — | — |
| gamma | gamma_security_mfa.pdf | 11 | skipped | — | — |
| gamma | gamma_sales_quota.pdf | 13 | skipped | — | — |
| gamma | gamma_legal_nda.pdf | 11 | skipped | — | — |
| gamma | gamma_ops_datacenter.pdf | 12 | skipped | — | — |
| gamma | gamma_marketing_brand.pdf | 14 | skipped | — | — |
| gamma | gamma_support_sla.pdf | 10 | skipped | — | — |
| gamma | gamma_product_roadmap.pdf | 12 | skipped | — | — |
| gamma | gamma_compliance_retention.pdf | 10 | skipped | — | — |
| gamma | gamma_training_budget.pdf | 10 | skipped | — | — |
| gamma | gamma_it_laptop.pdf | 10 | skipped | — | — |
| gamma | gamma_procurement_approval.pdf | 12 | skipped | — | — |
| gamma | gamma_cs_onboarding.pdf | 10 | skipped | — | — |

## Question results

| ID | Org | Pass | PDF OK | Latency ms | Source | Detail |
|----|-----|------|--------|------------|--------|--------|
| acme_hr_vacation_primary | acme | PASS | no | 30193 | acme_hr_vacation.pdf p1 | matched ['18']; type=primary; pdf_verified=False |
| acme_finance_meals_primary | acme | PASS | no | 19153 | acme_finance_meals.pdf p1 | matched ['75']; type=primary; pdf_verified=False |
| acme_eng_deploy_primary | acme | PASS | no | 18085 | acme_eng_deploy.pdf p1 | matched ['Tuesday through Thursday']; type=primary; pdf_verified=False |
| acme_security_mfa_primary | acme | PASS | no | 19349 | acme_security_mfa.pdf p1 | matched ['all VPN connections']; type=primary; pdf_verified=False |
| acme_sales_quota_primary | acme | PASS | no | 20562 | acme_sales_quota.pdf p1 | matched ['1.2']; type=primary; pdf_verified=False |
| acme_legal_nda_primary | acme | PASS | no | 18610 | acme_legal_nda.pdf p1 | matched ['5']; type=primary; pdf_verified=False |
| acme_ops_datacenter_primary | acme | FAIL | no | 17644 | acme_ops_datacenter.pdf p1 | answer missing ground-truth terms ('Dallas Texas',) |
| acme_marketing_brand_primary | acme | PASS | no | 18417 | acme_marketing_brand.pdf p1 | matched ['2563eb']; type=primary; pdf_verified=False |
| acme_support_sla_primary | acme | PASS | no | 18622 | acme_support_sla.pdf p1 | matched ['4']; type=primary; pdf_verified=False |
| acme_product_roadmap_primary | acme | PASS | no | 19238 | acme_product_roadmap.pdf p1 | matched ['Q3 2026']; type=primary; pdf_verified=False |
| acme_compliance_retention_primary | acme | PASS | no | 19257 | acme_compliance_retention.pdf p1 | matched ['90']; type=primary; pdf_verified=False |
| acme_training_budget_primary | acme | PASS | no | 18164 | acme_training_budget.pdf p1 | matched ['1500']; type=primary; pdf_verified=False |
| acme_it_laptop_primary | acme | PASS | no | 18099 | acme_it_laptop.pdf p1 | matched ['3']; type=primary; pdf_verified=False |
| acme_procurement_approval_primary | acme | PASS | no | 18669 | acme_procurement_approval.pdf p1 | matched ['5000']; type=primary; pdf_verified=False |
| acme_cs_onboarding_primary | acme | FAIL | no | 18949 | acme_cs_onboarding.pdf p1 | answer missing ground-truth terms ('30',) |
| beta_hr_vacation_primary | beta | PASS | no | 21723 | beta_hr_vacation.pdf p1 | matched ['22']; type=primary; pdf_verified=False |
| beta_finance_meals_primary | beta | PASS | no | 18379 | beta_finance_meals.pdf p1 | matched ['60']; type=primary; pdf_verified=False |
| beta_eng_deploy_primary | beta | PASS | no | 18517 | beta_eng_deploy.pdf p1 | matched ['Monday through Wednesday']; type=primary; pdf_verified=False |
| beta_security_mfa_primary | beta | PASS | no | 17879 | beta_security_mfa.pdf p1 | matched ['all admin consoles']; type=primary; pdf_verified=False |
| beta_sales_quota_primary | beta | PASS | no | 18088 | beta_sales_quota.pdf p1 | matched ['0.9']; type=primary; pdf_verified=False |
| beta_legal_nda_primary | beta | PASS | no | 18242 | beta_legal_nda.pdf p1 | matched ['3']; type=primary; pdf_verified=False |
| beta_ops_datacenter_primary | beta | FAIL | no | 17579 | beta_ops_datacenter.pdf p1 | answer missing ground-truth terms ('Chicago Illinois',) |
| beta_marketing_brand_primary | beta | PASS | no | 18246 | beta_marketing_brand.pdf p1 | matched ['dc2626']; type=primary; pdf_verified=False |
| beta_support_sla_primary | beta | PASS | no | 19047 | beta_support_sla.pdf p1 | matched ['2']; type=primary; pdf_verified=False |
| beta_product_roadmap_primary | beta | PASS | no | 18573 | beta_product_roadmap.pdf p1 | matched ['Q2 2026']; type=primary; pdf_verified=False |
| beta_compliance_retention_primary | beta | PASS | no | 17944 | beta_compliance_retention.pdf p1 | matched ['120']; type=primary; pdf_verified=False |
| beta_training_budget_primary | beta | PASS | no | 18178 | beta_training_budget.pdf p1 | matched ['2000']; type=primary; pdf_verified=False |
| beta_it_laptop_primary | beta | FAIL | no | 19056 | beta_it_laptop.pdf p1 | answer missing ground-truth terms ('4',) |
| beta_procurement_approval_primary | beta | PASS | no | 16877 | beta_procurement_approval.pdf p1 | matched ['3000']; type=primary; pdf_verified=False |
| beta_cs_onboarding_primary | beta | FAIL | no | 16638 | beta_cs_onboarding.pdf p1 | answer missing ground-truth terms ('45',) |
| gamma_hr_vacation_primary | gamma | PASS | no | 20148 | gamma_hr_vacation.pdf p1 | matched ['15']; type=primary; pdf_verified=False |
| gamma_finance_meals_primary | gamma | PASS | no | 18465 | gamma_finance_meals.pdf p1 | matched ['90']; type=primary; pdf_verified=False |
| gamma_eng_deploy_primary | gamma | PASS | no | 20762 | gamma_eng_deploy.pdf p1 | matched ['Wednesday through Friday']; type=primary; pdf_verified=False |
| gamma_security_mfa_primary | gamma | PASS | no | 16423 | gamma_security_mfa.pdf p1 | matched ['all cloud dashboards']; type=primary; pdf_verified=False |
| gamma_sales_quota_primary | gamma | PASS | no | 17141 | gamma_sales_quota.pdf p1 | matched ['1.5']; type=primary; pdf_verified=False |
| gamma_legal_nda_primary | gamma | PASS | no | 17523 | gamma_legal_nda.pdf p1 | matched ['7']; type=primary; pdf_verified=False |
| gamma_ops_datacenter_primary | gamma | FAIL | no | 17614 | gamma_ops_datacenter.pdf p1 | answer missing ground-truth terms ('Austin Texas',) |
| gamma_marketing_brand_primary | gamma | PASS | no | 16594 | gamma_marketing_brand.pdf p1 | matched ['059669']; type=primary; pdf_verified=False |
| gamma_support_sla_primary | gamma | PASS | no | 18278 | gamma_support_sla.pdf p1 | matched ['6']; type=primary; pdf_verified=False |
| gamma_product_roadmap_primary | gamma | PASS | no | 17307 | gamma_product_roadmap.pdf p1 | matched ['Q4 2026']; type=primary; pdf_verified=False |
| gamma_compliance_retention_primary | gamma | PASS | no | 19578 | gamma_compliance_retention.pdf p1 | matched ['60']; type=primary; pdf_verified=False |
| gamma_training_budget_primary | gamma | PASS | no | 17113 | gamma_training_budget.pdf p1 | matched ['1200']; type=primary; pdf_verified=False |
| gamma_it_laptop_primary | gamma | PASS | no | 20159 | gamma_it_laptop.pdf p1 | matched ['2']; type=primary; pdf_verified=False |
| gamma_procurement_approval_primary | gamma | FAIL | no | 17935 | gamma_procurement_approval.pdf p1 | answer missing ground-truth terms ('7500',) |
| gamma_cs_onboarding_primary | gamma | PASS | no | 18673 | gamma_cs_onboarding.pdf p1 | matched ['21']; type=primary; pdf_verified=False |
| acme_hr_vacation_p06 | acme | PASS | yes | 17776 | acme_hr_vacation.pdf p6 | matched ['AUDIT-ACME-HR_VACATION-06', '60']; type=page_fact; pdf_verif |
| acme_finance_meals_p07 | acme | PASS | yes | 18714 | acme_finance_meals.pdf p7 | matched ['AUDIT-ACME-FINANCE_MEALS-07', '70']; type=page_fact; pdf_ver |
| acme_eng_deploy_p05 | acme | PASS | yes | 20000 | acme_eng_deploy.pdf p5 | matched ['AUDIT-ACME-ENG_DEPLOY-05', '50']; type=page_fact; pdf_verifi |
| acme_security_mfa_p05 | acme | PASS | yes | 18635 | acme_security_mfa.pdf p5 | matched ['AUDIT-ACME-SECURITY_MFA-05', '50']; type=page_fact; pdf_veri |
| acme_sales_quota_p06 | acme | PASS | yes | 20118 | acme_sales_quota.pdf p6 | matched ['AUDIT-ACME-SALES_QUOTA-06', '60']; type=page_fact; pdf_verif |
| acme_legal_nda_p05 | acme | PASS | yes | 18476 | acme_legal_nda.pdf p5 | matched ['AUDIT-ACME-LEGAL_NDA-05', '50']; type=page_fact; pdf_verifie |
| acme_ops_datacenter_p06 | acme | PASS | yes | 18032 | acme_ops_datacenter.pdf p6 | matched ['AUDIT-ACME-OPS_DATACENTER-06', '60']; type=page_fact; pdf_ve |
| acme_marketing_brand_p07 | acme | PASS | yes | 18239 | acme_marketing_brand.pdf p7 | matched ['AUDIT-ACME-MARKETING_BRAND-07', '70']; type=page_fact; pdf_v |
| acme_support_sla_p05 | acme | PASS | yes | 17363 | acme_support_sla.pdf p5 | matched ['AUDIT-ACME-SUPPORT_SLA-05', '50']; type=page_fact; pdf_verif |
| acme_product_roadmap_p06 | acme | PASS | yes | 18249 | acme_product_roadmap.pdf p6 | matched ['AUDIT-ACME-PRODUCT_ROADMAP-06', '60']; type=page_fact; pdf_v |
| acme_compliance_retention_p05 | acme | PASS | yes | 18199 | acme_compliance_retention.pdf p5 | matched ['AUDIT-ACME-COMPLIANCE_RETENTION-05', '50']; type=page_fact;  |
| acme_training_budget_p05 | acme | PASS | yes | 19065 | acme_training_budget.pdf p5 | matched ['AUDIT-ACME-TRAINING_BUDGET-05', '50']; type=page_fact; pdf_v |
| acme_it_laptop_p05 | acme | PASS | yes | 18424 | acme_it_laptop.pdf p5 | matched ['AUDIT-ACME-IT_LAPTOP-05', '50']; type=page_fact; pdf_verifie |
| acme_procurement_approval_p06 | acme | PASS | yes | 18407 | acme_procurement_approval.pdf p6 | matched ['AUDIT-ACME-PROCUREMENT_APPROVAL-06', '60']; type=page_fact;  |
| acme_cs_onboarding_p05 | acme | PASS | yes | 17750 | acme_cs_onboarding.pdf p5 | matched ['AUDIT-ACME-CS_ONBOARDING-05', '50']; type=page_fact; pdf_ver |
| beta_hr_vacation_p06 | beta | PASS | yes | 18041 | beta_hr_vacation.pdf p6 | matched ['AUDIT-BETA-HR_VACATION-06', '78']; type=page_fact; pdf_verif |
| beta_finance_meals_p07 | beta | PASS | yes | 18422 | beta_finance_meals.pdf p7 | matched ['AUDIT-BETA-FINANCE_MEALS-07', '91']; type=page_fact; pdf_ver |
| beta_eng_deploy_p05 | beta | PASS | yes | 17240 | beta_eng_deploy.pdf p5 | matched ['AUDIT-BETA-ENG_DEPLOY-05', '65']; type=page_fact; pdf_verifi |
| beta_security_mfa_p05 | beta | PASS | yes | 17871 | beta_security_mfa.pdf p5 | matched ['AUDIT-BETA-SECURITY_MFA-05', '65']; type=page_fact; pdf_veri |
| beta_sales_quota_p06 | beta | PASS | yes | 18545 | beta_sales_quota.pdf p6 | matched ['AUDIT-BETA-SALES_QUOTA-06', '78']; type=page_fact; pdf_verif |
| beta_legal_nda_p05 | beta | PASS | yes | 18157 | beta_legal_nda.pdf p5 | matched ['AUDIT-BETA-LEGAL_NDA-05', '65']; type=page_fact; pdf_verifie |
| beta_ops_datacenter_p06 | beta | PASS | yes | 17263 | beta_ops_datacenter.pdf p6 | matched ['AUDIT-BETA-OPS_DATACENTER-06', '78']; type=page_fact; pdf_ve |
| beta_marketing_brand_p07 | beta | PASS | yes | 17912 | beta_marketing_brand.pdf p7 | matched ['AUDIT-BETA-MARKETING_BRAND-07', '91']; type=page_fact; pdf_v |
| beta_support_sla_p05 | beta | PASS | yes | 17878 | beta_support_sla.pdf p5 | matched ['AUDIT-BETA-SUPPORT_SLA-05', '65']; type=page_fact; pdf_verif |
| beta_product_roadmap_p06 | beta | PASS | yes | 17864 | beta_product_roadmap.pdf p6 | matched ['AUDIT-BETA-PRODUCT_ROADMAP-06', '78']; type=page_fact; pdf_v |
| beta_compliance_retention_p05 | beta | PASS | yes | 19824 | beta_compliance_retention.pdf p5 | matched ['AUDIT-BETA-COMPLIANCE_RETENTION-05', '65']; type=page_fact;  |
| beta_training_budget_p05 | beta | PASS | yes | 19699 | beta_training_budget.pdf p5 | matched ['AUDIT-BETA-TRAINING_BUDGET-05', '65']; type=page_fact; pdf_v |
| beta_it_laptop_p05 | beta | PASS | yes | 18375 | beta_it_laptop.pdf p5 | matched ['AUDIT-BETA-IT_LAPTOP-05', '65']; type=page_fact; pdf_verifie |
| beta_procurement_approval_p06 | beta | PASS | yes | 23270 | beta_procurement_approval.pdf p6 | matched ['AUDIT-BETA-PROCUREMENT_APPROVAL-06', '78']; type=page_fact;  |
| beta_cs_onboarding_p05 | beta | PASS | yes | 32767 | beta_cs_onboarding.pdf p5 | matched ['AUDIT-BETA-CS_ONBOARDING-05', '65']; type=page_fact; pdf_ver |
| gamma_hr_vacation_p06 | gamma | PASS | yes | 22230 | gamma_hr_vacation.pdf p6 | matched ['AUDIT-GAMMA-HR_VACATION-06', '96']; type=page_fact; pdf_veri |
| gamma_finance_meals_p07 | gamma | PASS | yes | 20589 | gamma_finance_meals.pdf p7 | matched ['AUDIT-GAMMA-FINANCE_MEALS-07', '112']; type=page_fact; pdf_v |
| gamma_eng_deploy_p05 | gamma | PASS | yes | 20676 | gamma_eng_deploy.pdf p5 | matched ['AUDIT-GAMMA-ENG_DEPLOY-05', '80']; type=page_fact; pdf_verif |
| gamma_security_mfa_p05 | gamma | PASS | yes | 19918 | gamma_security_mfa.pdf p5 | matched ['AUDIT-GAMMA-SECURITY_MFA-05', '80']; type=page_fact; pdf_ver |
| gamma_sales_quota_p06 | gamma | PASS | yes | 19743 | gamma_sales_quota.pdf p6 | matched ['AUDIT-GAMMA-SALES_QUOTA-06', '96']; type=page_fact; pdf_veri |
| gamma_legal_nda_p05 | gamma | PASS | yes | 20260 | gamma_legal_nda.pdf p5 | matched ['AUDIT-GAMMA-LEGAL_NDA-05', '80']; type=page_fact; pdf_verifi |
| gamma_ops_datacenter_p06 | gamma | PASS | yes | 30871 | gamma_ops_datacenter.pdf p6 | matched ['AUDIT-GAMMA-OPS_DATACENTER-06', '96']; type=page_fact; pdf_v |
| gamma_marketing_brand_p07 | gamma | PASS | yes | 17963 | gamma_marketing_brand.pdf p7 | matched ['AUDIT-GAMMA-MARKETING_BRAND-07', '112']; type=page_fact; pdf |
| gamma_support_sla_p05 | gamma | PASS | yes | 20135 | gamma_support_sla.pdf p5 | matched ['AUDIT-GAMMA-SUPPORT_SLA-05', '80']; type=page_fact; pdf_veri |
| gamma_product_roadmap_p06 | gamma | PASS | yes | 20069 | gamma_product_roadmap.pdf p6 | matched ['AUDIT-GAMMA-PRODUCT_ROADMAP-06', '96']; type=page_fact; pdf_ |
| gamma_compliance_retention_p05 | gamma | PASS | yes | 21146 | gamma_compliance_retention.pdf p5 | matched ['AUDIT-GAMMA-COMPLIANCE_RETENTION-05', '80']; type=page_fact; |
| gamma_training_budget_p05 | gamma | PASS | yes | 20362 | gamma_training_budget.pdf p5 | matched ['AUDIT-GAMMA-TRAINING_BUDGET-05', '80']; type=page_fact; pdf_ |
| gamma_it_laptop_p05 | gamma | PASS | yes | 20538 | gamma_it_laptop.pdf p5 | matched ['AUDIT-GAMMA-IT_LAPTOP-05', '80']; type=page_fact; pdf_verifi |
| gamma_procurement_approval_p06 | gamma | PASS | yes | 20041 | gamma_procurement_approval.pdf p6 | matched ['AUDIT-GAMMA-PROCUREMENT_APPROVAL-06', '96']; type=page_fact; |
| gamma_cs_onboarding_p05 | gamma | PASS | yes | 19799 | gamma_cs_onboarding.pdf p5 | matched ['AUDIT-GAMMA-CS_ONBOARDING-05', '80']; type=page_fact; pdf_ve |
| acme_hr_vacation_plast | acme | PASS | yes | 20564 | acme_hr_vacation.pdf p12 | matched ['120', 'AUDIT-ACME-HR_VACATION-12']; type=late_page; pdf_veri |
| acme_finance_meals_plast | acme | PASS | yes | 21061 | acme_finance_meals.pdf p15 | matched ['150', 'AUDIT-ACME-FINANCE_MEALS-15']; type=late_page; pdf_ve |
| acme_eng_deploy_plast | acme | FAIL | no | 567 | acme_eng_deploy.pdf p10 | answer missing ground-truth terms ('100', 'AUDIT-ACME-ENG_DEPLOY-10') |
| acme_security_mfa_plast | acme | PASS | yes | 19737 | acme_security_mfa.pdf p11 | matched ['110', 'AUDIT-ACME-SECURITY_MFA-11']; type=late_page; pdf_ver |
| acme_sales_quota_plast | acme | FAIL | no | 335 | acme_sales_quota.pdf p13 | answer missing ground-truth terms ('130', 'AUDIT-ACME-SALES_QUOTA-13') |
| acme_legal_nda_plast | acme | PASS | yes | 20408 | acme_legal_nda.pdf p11 | matched ['110', 'AUDIT-ACME-LEGAL_NDA-11']; type=late_page; pdf_verifi |
| acme_ops_datacenter_plast | acme | FAIL | no | 550 | acme_ops_datacenter.pdf p12 | answer missing ground-truth terms ('120', 'AUDIT-ACME-OPS_DATACENTER-1 |
| acme_marketing_brand_plast | acme | FAIL | no | 1087 | acme_marketing_brand.pdf p14 | answer missing ground-truth terms ('140', 'AUDIT-ACME-MARKETING_BRAND- |
| acme_support_sla_plast | acme | FAIL | no | 210 | acme_support_sla.pdf p10 | answer missing ground-truth terms ('100', 'AUDIT-ACME-SUPPORT_SLA-10') |
| acme_product_roadmap_plast | acme | FAIL | no | 311 | acme_product_roadmap.pdf p12 | answer missing ground-truth terms ('120', 'AUDIT-ACME-PRODUCT_ROADMAP- |

## Ground truth vs answers

### acme_hr_vacation_primary
- **Org:** Acme Corporation
- **Question:** According to acme_hr_vacation.pdf, what is the annual PTO allowance for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] HR Vacation Policy — annual PTO allowance is 18 days
- **Pass:** True — matched ['18']; type=primary; pdf_verified=False
- **Assistant answer:** The annual PTO allowance for Acme Corporation is 18 days (Source 1).

### acme_finance_meals_primary
- **Org:** Acme Corporation
- **Question:** According to acme_finance_meals.pdf, what is the daily meal reimbursement limit for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Finance Meal Policy — meal reimbursement limit is 75 dollars per day
- **Pass:** True — matched ['75']; type=primary; pdf_verified=False
- **Assistant answer:** The daily meal reimbursement limit for Acme Corporation is 75 dollars per day (Source 1).

### acme_eng_deploy_primary
- **Org:** Acme Corporation
- **Question:** According to acme_eng_deploy.pdf, what is the allowed production deploy days for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Engineering Deploy Policy — production deploys are allowed on Tuesday through Thursday only
- **Pass:** True — matched ['Tuesday through Thursday']; type=primary; pdf_verified=False
- **Assistant answer:** According to acme_eng_deploy.pdf, production deploys at Acme Corporation are allowed on Tuesday through Thursday only (Source 1).

### acme_security_mfa_primary
- **Org:** Acme Corporation
- **Question:** According to acme_security_mfa.pdf, what is the MFA requirement for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Security MFA Policy — MFA is required for all VPN connections
- **Pass:** True — matched ['all VPN connections']; type=primary; pdf_verified=False
- **Assistant answer:** According to the acme_security_mfa.pdf, Multi-Factor Authentication (MFA) is required for all VPN connections at Acme Corporation. This requirement ensures an additional layer of security for remote access (Source 1).

### acme_sales_quota_primary
- **Org:** Acme Corporation
- **Question:** According to acme_sales_quota.pdf, what is the Q1 sales quota for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Sales Quota Policy — Q1 sales quota is 1.2 million dollars
- **Pass:** True — matched ['1.2']; type=primary; pdf_verified=False
- **Assistant answer:** The Q1 sales quota for Acme Corporation is 1.2 million dollars (Source 1).

### acme_legal_nda_primary
- **Org:** Acme Corporation
- **Question:** According to acme_legal_nda.pdf, what is the standard NDA term for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Legal NDA Policy — standard NDA term is 5 years
- **Pass:** True — matched ['5']; type=primary; pdf_verified=False
- **Assistant answer:** The standard NDA term for Acme Corporation is 5 years (Source 1).

### acme_ops_datacenter_primary
- **Org:** Acme Corporation
- **Question:** According to acme_ops_datacenter.pdf, what is the primary datacenter city for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Operations Datacenter Policy — primary datacenter is located in Dallas Texas
- **Pass:** False — answer missing ground-truth terms ('Dallas Texas',)
- **Assistant answer:** The information is not available in the uploaded documents.

### acme_marketing_brand_primary
- **Org:** Acme Corporation
- **Question:** According to acme_marketing_brand.pdf, what is the brand primary color hex for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Marketing Brand Policy — brand primary color is hex 2563eb
- **Pass:** True — matched ['2563eb']; type=primary; pdf_verified=False
- **Assistant answer:** The brand primary color hex for Acme Corporation is 2563eb (Source 1).

### acme_support_sla_primary
- **Org:** Acme Corporation
- **Question:** According to acme_support_sla.pdf, what is the P1 first response SLA for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Support SLA Policy — P1 support SLA is 4 hour first response
- **Pass:** True — matched ['4']; type=primary; pdf_verified=False
- **Assistant answer:** The P1 first response SLA for Acme Corporation is 4 hours (Source 1).

### acme_product_roadmap_primary
- **Org:** Acme Corporation
- **Question:** According to acme_product_roadmap.pdf, what is the Feature X ship target for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Product Roadmap Policy — Feature X ships in Q3 2026
- **Pass:** True — matched ['Q3 2026']; type=primary; pdf_verified=False
- **Assistant answer:** The ship target for Feature X at Acme Corporation is planned for Q3 2026 (Source 1).

### acme_compliance_retention_primary
- **Org:** Acme Corporation
- **Question:** According to acme_compliance_retention.pdf, what is the customer log retention for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Compliance Retention Policy — customer log retention is 90 days
- **Pass:** True — matched ['90']; type=primary; pdf_verified=False
- **Assistant answer:** According to the acme_compliance_retention.pdf document, the customer log retention for Acme Corporation is 90 days (Source 1).

### acme_training_budget_primary
- **Org:** Acme Corporation
- **Question:** According to acme_training_budget.pdf, what is the annual training budget per engineer for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Training Budget Policy — training budget is 1500 dollars per engineer per year
- **Pass:** True — matched ['1500']; type=primary; pdf_verified=False
- **Assistant answer:** According to acme_training_budget.pdf, the annual training budget per engineer for Acme Corporation is 1500 dollars (Source 1).

### acme_it_laptop_primary
- **Org:** Acme Corporation
- **Question:** According to acme_it_laptop.pdf, what is the laptop refresh cycle for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] IT Laptop Policy — laptop refresh cycle is 3 years
- **Pass:** True — matched ['3']; type=primary; pdf_verified=False
- **Assistant answer:** The laptop refresh cycle for Acme Corporation is set at 3 years (Source 1).

### acme_procurement_approval_primary
- **Org:** Acme Corporation
- **Question:** According to acme_procurement_approval.pdf, what is the purchase approval threshold for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Procurement Approval Policy — purchases over 5000 dollars require director approval
- **Pass:** True — matched ['5000']; type=primary; pdf_verified=False
- **Assistant answer:** The purchase approval threshold for Acme Corporation, according to the procurement approval policy, is that purchases over 5000 dollars require director approval (Source 1).

### acme_cs_onboarding_primary
- **Org:** Acme Corporation
- **Question:** According to acme_cs_onboarding.pdf, what is the customer onboarding duration for Acme Corporation?
- **Ground truth:** KEY_FACT: [ACME] Customer Success Onboarding Policy — customer onboarding duration is 30 days
- **Pass:** False — answer missing ground-truth terms ('30',)
- **Assistant answer:** The information is not available in the uploaded documents.

### beta_hr_vacation_primary
- **Org:** Beta Industries
- **Question:** According to beta_hr_vacation.pdf, what is the annual PTO allowance for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] HR Vacation Policy — annual PTO allowance is 22 days
- **Pass:** True — matched ['22']; type=primary; pdf_verified=False
- **Assistant answer:** The annual PTO allowance for Beta Industries is 22 days (Source 1).

### beta_finance_meals_primary
- **Org:** Beta Industries
- **Question:** According to beta_finance_meals.pdf, what is the daily meal reimbursement limit for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Finance Meal Policy — meal reimbursement limit is 60 dollars per day
- **Pass:** True — matched ['60']; type=primary; pdf_verified=False
- **Assistant answer:** The daily meal reimbursement limit for Beta Industries is 60 dollars (Source 1).

### beta_eng_deploy_primary
- **Org:** Beta Industries
- **Question:** According to beta_eng_deploy.pdf, what is the allowed production deploy days for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Engineering Deploy Policy — production deploys are allowed on Monday through Wednesday only
- **Pass:** True — matched ['Monday through Wednesday']; type=primary; pdf_verified=False
- **Assistant answer:** Production deploys at Beta Industries are allowed on Monday through Wednesday only (Source 1).

### beta_security_mfa_primary
- **Org:** Beta Industries
- **Question:** According to beta_security_mfa.pdf, what is the MFA requirement for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Security MFA Policy — MFA is required for all admin consoles
- **Pass:** True — matched ['all admin consoles']; type=primary; pdf_verified=False
- **Assistant answer:** According to the beta_security_mfa.pdf, multi-factor authentication (MFA) is required for all admin consoles at Beta Industries. This policy helps enhance security by ensuring that unauthorized access is mitigated through an additional verification step (Source 1).

### beta_sales_quota_primary
- **Org:** Beta Industries
- **Question:** According to beta_sales_quota.pdf, what is the Q1 sales quota for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Sales Quota Policy — Q1 sales quota is 0.9 million dollars
- **Pass:** True — matched ['0.9']; type=primary; pdf_verified=False
- **Assistant answer:** The Q1 sales quota for Beta Industries is 0.9 million dollars (Source 1).

### beta_legal_nda_primary
- **Org:** Beta Industries
- **Question:** According to beta_legal_nda.pdf, what is the standard NDA term for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Legal NDA Policy — standard NDA term is 3 years
- **Pass:** True — matched ['3']; type=primary; pdf_verified=False
- **Assistant answer:** The standard NDA term for Beta Industries is 3 years (Source 1).

### beta_ops_datacenter_primary
- **Org:** Beta Industries
- **Question:** According to beta_ops_datacenter.pdf, what is the primary datacenter city for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Operations Datacenter Policy — primary datacenter is located in Chicago Illinois
- **Pass:** False — answer missing ground-truth terms ('Chicago Illinois',)
- **Assistant answer:** The information is not available in the uploaded documents.

### beta_marketing_brand_primary
- **Org:** Beta Industries
- **Question:** According to beta_marketing_brand.pdf, what is the brand primary color hex for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Marketing Brand Policy — brand primary color is hex dc2626
- **Pass:** True — matched ['dc2626']; type=primary; pdf_verified=False
- **Assistant answer:** The brand primary color hex for Beta Industries is dc2626 (Source 1).

### beta_support_sla_primary
- **Org:** Beta Industries
- **Question:** According to beta_support_sla.pdf, what is the P1 first response SLA for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Support SLA Policy — P1 support SLA is 2 hour first response
- **Pass:** True — matched ['2']; type=primary; pdf_verified=False
- **Assistant answer:** The P1 first response SLA for Beta Industries is 2 hours (Source 1).

### beta_product_roadmap_primary
- **Org:** Beta Industries
- **Question:** According to beta_product_roadmap.pdf, what is the Feature X ship target for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Product Roadmap Policy — Feature X ships in Q2 2026
- **Pass:** True — matched ['Q2 2026']; type=primary; pdf_verified=False
- **Assistant answer:** The Feature X ship target for Beta Industries is set for Q2 2026 (Source 1).

### beta_compliance_retention_primary
- **Org:** Beta Industries
- **Question:** According to beta_compliance_retention.pdf, what is the customer log retention for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Compliance Retention Policy — customer log retention is 120 days
- **Pass:** True — matched ['120']; type=primary; pdf_verified=False
- **Assistant answer:** According to the document beta_compliance_retention.pdf, the customer log retention policy for Beta Industries specifies that customer log retention is 120 days (Source 1).

### beta_training_budget_primary
- **Org:** Beta Industries
- **Question:** According to beta_training_budget.pdf, what is the annual training budget per engineer for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Training Budget Policy — training budget is 2000 dollars per engineer per year
- **Pass:** True — matched ['2000']; type=primary; pdf_verified=False
- **Assistant answer:** The annual training budget per engineer for Beta Industries is 2000 dollars (Source 1).

### beta_it_laptop_primary
- **Org:** Beta Industries
- **Question:** According to beta_it_laptop.pdf, what is the laptop refresh cycle for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] IT Laptop Policy — laptop refresh cycle is 4 years
- **Pass:** False — answer missing ground-truth terms ('4',)
- **Assistant answer:** The laptop refresh cycle for Beta Industries is four years (Source 1).

### beta_procurement_approval_primary
- **Org:** Beta Industries
- **Question:** According to beta_procurement_approval.pdf, what is the purchase approval threshold for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Procurement Approval Policy — purchases over 3000 dollars require director approval
- **Pass:** True — matched ['3000']; type=primary; pdf_verified=False
- **Assistant answer:** The purchase approval threshold for Beta Industries is set at purchases over 3000 dollars, which require director approval (Source 1).

### beta_cs_onboarding_primary
- **Org:** Beta Industries
- **Question:** According to beta_cs_onboarding.pdf, what is the customer onboarding duration for Beta Industries?
- **Ground truth:** KEY_FACT: [BETA] Customer Success Onboarding Policy — customer onboarding duration is 45 days
- **Pass:** False — answer missing ground-truth terms ('45',)
- **Assistant answer:** The information is not available in the uploaded documents.

### gamma_hr_vacation_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_hr_vacation.pdf, what is the annual PTO allowance for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] HR Vacation Policy — annual PTO allowance is 15 days
- **Pass:** True — matched ['15']; type=primary; pdf_verified=False
- **Assistant answer:** The annual PTO allowance for Gamma Solutions is 15 days (Source 1).

### gamma_finance_meals_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_finance_meals.pdf, what is the daily meal reimbursement limit for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Finance Meal Policy — meal reimbursement limit is 90 dollars per day
- **Pass:** True — matched ['90']; type=primary; pdf_verified=False
- **Assistant answer:** The daily meal reimbursement limit for Gamma Solutions is 90 dollars (Source 1).

### gamma_eng_deploy_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_eng_deploy.pdf, what is the allowed production deploy days for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Engineering Deploy Policy — production deploys are allowed on Wednesday through Friday only
- **Pass:** True — matched ['Wednesday through Friday']; type=primary; pdf_verified=False
- **Assistant answer:** Production deploys at Gamma Solutions are allowed on Wednesday through Friday only (Source 1).

### gamma_security_mfa_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_security_mfa.pdf, what is the MFA requirement for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Security MFA Policy — MFA is required for all cloud dashboards
- **Pass:** True — matched ['all cloud dashboards']; type=primary; pdf_verified=False
- **Assistant answer:** MFA (Multi-Factor Authentication) is required for all cloud dashboards at Gamma Solutions. This requirement ensures an additional layer of security for accessing cloud resources (Source 1).

### gamma_sales_quota_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_sales_quota.pdf, what is the Q1 sales quota for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Sales Quota Policy — Q1 sales quota is 1.5 million dollars
- **Pass:** True — matched ['1.5']; type=primary; pdf_verified=False
- **Assistant answer:** The Q1 sales quota for Gamma Solutions is 1.5 million dollars (Source 1).

### gamma_legal_nda_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_legal_nda.pdf, what is the standard NDA term for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Legal NDA Policy — standard NDA term is 7 years
- **Pass:** True — matched ['7']; type=primary; pdf_verified=False
- **Assistant answer:** The standard NDA term for Gamma Solutions is 7 years (Source 1).

### gamma_ops_datacenter_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_ops_datacenter.pdf, what is the primary datacenter city for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Operations Datacenter Policy — primary datacenter is located in Austin Texas
- **Pass:** False — answer missing ground-truth terms ('Austin Texas',)
- **Assistant answer:** The primary datacenter city for Gamma Solutions is Austin, Texas (Source 1).

### gamma_marketing_brand_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_marketing_brand.pdf, what is the brand primary color hex for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Marketing Brand Policy — brand primary color is hex 059669
- **Pass:** True — matched ['059669']; type=primary; pdf_verified=False
- **Assistant answer:** The brand primary color hex for Gamma Solutions is 059669 (Source 1).

### gamma_support_sla_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_support_sla.pdf, what is the P1 first response SLA for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Support SLA Policy — P1 support SLA is 6 hour first response
- **Pass:** True — matched ['6']; type=primary; pdf_verified=False
- **Assistant answer:** The P1 first response SLA for Gamma Solutions is 6 hours (Source 1).

### gamma_product_roadmap_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_product_roadmap.pdf, what is the Feature X ship target for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Product Roadmap Policy — Feature X ships in Q4 2026
- **Pass:** True — matched ['Q4 2026']; type=primary; pdf_verified=False
- **Assistant answer:** The ship target for Feature X for Gamma Solutions is set for Q4 2026 (Source 1).

### gamma_compliance_retention_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_compliance_retention.pdf, what is the customer log retention for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Compliance Retention Policy — customer log retention is 60 days
- **Pass:** True — matched ['60']; type=primary; pdf_verified=False
- **Assistant answer:** The customer log retention for Gamma Solutions is 60 days (Source 1).

### gamma_training_budget_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_training_budget.pdf, what is the annual training budget per engineer for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Training Budget Policy — training budget is 1200 dollars per engineer per year
- **Pass:** True — matched ['1200']; type=primary; pdf_verified=False
- **Assistant answer:** The annual training budget per engineer for Gamma Solutions is 1200 dollars (Source 1).

### gamma_it_laptop_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_it_laptop.pdf, what is the laptop refresh cycle for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] IT Laptop Policy — laptop refresh cycle is 2 years
- **Pass:** True — matched ['2']; type=primary; pdf_verified=False
- **Assistant answer:** The laptop refresh cycle for Gamma Solutions is 2 years (Source 1).

### gamma_procurement_approval_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_procurement_approval.pdf, what is the purchase approval threshold for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Procurement Approval Policy — purchases over 7500 dollars require director approval
- **Pass:** False — answer missing ground-truth terms ('7500',)
- **Assistant answer:** The purchase approval threshold for Gamma Solutions is set at purchases exceeding 7,500 dollars, which requires director approval (Source 1).

### gamma_cs_onboarding_primary
- **Org:** Gamma Solutions
- **Question:** According to gamma_cs_onboarding.pdf, what is the customer onboarding duration for Gamma Solutions?
- **Ground truth:** KEY_FACT: [GAMMA] Customer Success Onboarding Policy — customer onboarding duration is 21 days
- **Pass:** True — matched ['21']; type=primary; pdf_verified=False
- **Assistant answer:** The customer onboarding duration for Gamma Solutions is 21 days (Source 1).

### acme_hr_vacation_p06
- **Org:** Acme Corporation
- **Question:** In acme_hr_vacation.pdf, what value is recorded for audit token AUDIT-ACME-HR_VACATION-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [ACME] HR Vacation Policy audit token AUDIT-ACME-HR_VACATION-06 records value 60.
- **Pass:** True — matched ['AUDIT-ACME-HR_VACATION-06', '60']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-HR_VACATION-06 on page 6 of acme_hr_vacation.pdf is 60 (Source 1).

### acme_finance_meals_p07
- **Org:** Acme Corporation
- **Question:** In acme_finance_meals.pdf, what value is recorded for audit token AUDIT-ACME-FINANCE_MEALS-07 on page 7?
- **Ground truth:** KEY_FACT PAGE 7: [ACME] Finance Meal Policy audit token AUDIT-ACME-FINANCE_MEALS-07 records value 70.
- **Pass:** True — matched ['AUDIT-ACME-FINANCE_MEALS-07', '70']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-FINANCE_MEALS-07 on page 7 of acme_finance_meals.pdf is 70 (Source 1).

### acme_eng_deploy_p05
- **Org:** Acme Corporation
- **Question:** In acme_eng_deploy.pdf, what value is recorded for audit token AUDIT-ACME-ENG_DEPLOY-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] Engineering Deploy Policy audit token AUDIT-ACME-ENG_DEPLOY-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-ENG_DEPLOY-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The recorded value for audit token AUDIT-ACME-ENG_DEPLOY-05 on page 5 of acme_eng_deploy.pdf is 50 (Source 1).

### acme_security_mfa_p05
- **Org:** Acme Corporation
- **Question:** In acme_security_mfa.pdf, what value is recorded for audit token AUDIT-ACME-SECURITY_MFA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] Security MFA Policy audit token AUDIT-ACME-SECURITY_MFA-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-SECURITY_MFA-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-SECURITY_MFA-05 on page 5 of acme_security_mfa.pdf is 50 (Source 1).

### acme_sales_quota_p06
- **Org:** Acme Corporation
- **Question:** In acme_sales_quota.pdf, what value is recorded for audit token AUDIT-ACME-SALES_QUOTA-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [ACME] Sales Quota Policy audit token AUDIT-ACME-SALES_QUOTA-06 records value 60.
- **Pass:** True — matched ['AUDIT-ACME-SALES_QUOTA-06', '60']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-SALES_QUOTA-06 on page 6 of acme_sales_quota.pdf is 60 (Source 1).

### acme_legal_nda_p05
- **Org:** Acme Corporation
- **Question:** In acme_legal_nda.pdf, what value is recorded for audit token AUDIT-ACME-LEGAL_NDA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] Legal NDA Policy audit token AUDIT-ACME-LEGAL_NDA-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-LEGAL_NDA-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-LEGAL_NDA-05 on page 5 of acme_legal_nda.pdf is 50 (Source 1).

### acme_ops_datacenter_p06
- **Org:** Acme Corporation
- **Question:** In acme_ops_datacenter.pdf, what value is recorded for audit token AUDIT-ACME-OPS_DATACENTER-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [ACME] Operations Datacenter Policy audit token AUDIT-ACME-OPS_DATACENTER-06 records value 60.
- **Pass:** True — matched ['AUDIT-ACME-OPS_DATACENTER-06', '60']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-OPS_DATACENTER-06 on page 6 of acme_ops_datacenter.pdf is 60 (Source 1).

### acme_marketing_brand_p07
- **Org:** Acme Corporation
- **Question:** In acme_marketing_brand.pdf, what value is recorded for audit token AUDIT-ACME-MARKETING_BRAND-07 on page 7?
- **Ground truth:** KEY_FACT PAGE 7: [ACME] Marketing Brand Policy audit token AUDIT-ACME-MARKETING_BRAND-07 records value 70.
- **Pass:** True — matched ['AUDIT-ACME-MARKETING_BRAND-07', '70']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-MARKETING_BRAND-07 on page 7 of acme_marketing_brand.pdf is 70 (Source 1).

### acme_support_sla_p05
- **Org:** Acme Corporation
- **Question:** In acme_support_sla.pdf, what value is recorded for audit token AUDIT-ACME-SUPPORT_SLA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] Support SLA Policy audit token AUDIT-ACME-SUPPORT_SLA-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-SUPPORT_SLA-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-SUPPORT_SLA-05 on page 5 of acme_support_sla.pdf is 50 (Source 1).

### acme_product_roadmap_p06
- **Org:** Acme Corporation
- **Question:** In acme_product_roadmap.pdf, what value is recorded for audit token AUDIT-ACME-PRODUCT_ROADMAP-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [ACME] Product Roadmap Policy audit token AUDIT-ACME-PRODUCT_ROADMAP-06 records value 60.
- **Pass:** True — matched ['AUDIT-ACME-PRODUCT_ROADMAP-06', '60']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-PRODUCT_ROADMAP-06 on page 6 of acme_product_roadmap.pdf is 60 (Source 1).

### acme_compliance_retention_p05
- **Org:** Acme Corporation
- **Question:** In acme_compliance_retention.pdf, what value is recorded for audit token AUDIT-ACME-COMPLIANCE_RETENTION-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] Compliance Retention Policy audit token AUDIT-ACME-COMPLIANCE_RETENTION-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-COMPLIANCE_RETENTION-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-COMPLIANCE_RETENTION-05 on page 5 of acme_compliance_retention.pdf is 50 (Source 1).

### acme_training_budget_p05
- **Org:** Acme Corporation
- **Question:** In acme_training_budget.pdf, what value is recorded for audit token AUDIT-ACME-TRAINING_BUDGET-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] Training Budget Policy audit token AUDIT-ACME-TRAINING_BUDGET-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-TRAINING_BUDGET-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-TRAINING_BUDGET-05 on page 5 of acme_training_budget.pdf is 50 (Source 1).

### acme_it_laptop_p05
- **Org:** Acme Corporation
- **Question:** In acme_it_laptop.pdf, what value is recorded for audit token AUDIT-ACME-IT_LAPTOP-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] IT Laptop Policy audit token AUDIT-ACME-IT_LAPTOP-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-IT_LAPTOP-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-IT_LAPTOP-05 on page 5 of acme_it_laptop.pdf is 50 (Source 1).

### acme_procurement_approval_p06
- **Org:** Acme Corporation
- **Question:** In acme_procurement_approval.pdf, what value is recorded for audit token AUDIT-ACME-PROCUREMENT_APPROVAL-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [ACME] Procurement Approval Policy audit token AUDIT-ACME-PROCUREMENT_APPROVAL-06 records value 60.
- **Pass:** True — matched ['AUDIT-ACME-PROCUREMENT_APPROVAL-06', '60']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-PROCUREMENT_APPROVAL-06 on page 6 of acme_procurement_approval.pdf is 60 (Source 1).

### acme_cs_onboarding_p05
- **Org:** Acme Corporation
- **Question:** In acme_cs_onboarding.pdf, what value is recorded for audit token AUDIT-ACME-CS_ONBOARDING-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [ACME] Customer Success Onboarding Policy audit token AUDIT-ACME-CS_ONBOARDING-05 records value 50.
- **Pass:** True — matched ['AUDIT-ACME-CS_ONBOARDING-05', '50']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-CS_ONBOARDING-05 on page 5 of acme_cs_onboarding.pdf is 50 (Source 1).

### beta_hr_vacation_p06
- **Org:** Beta Industries
- **Question:** In beta_hr_vacation.pdf, what value is recorded for audit token AUDIT-BETA-HR_VACATION-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [BETA] HR Vacation Policy audit token AUDIT-BETA-HR_VACATION-06 records value 78.
- **Pass:** True — matched ['AUDIT-BETA-HR_VACATION-06', '78']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-HR_VACATION-06 on page 6 of beta_hr_vacation.pdf is 78 (Source 1).

### beta_finance_meals_p07
- **Org:** Beta Industries
- **Question:** In beta_finance_meals.pdf, what value is recorded for audit token AUDIT-BETA-FINANCE_MEALS-07 on page 7?
- **Ground truth:** KEY_FACT PAGE 7: [BETA] Finance Meal Policy audit token AUDIT-BETA-FINANCE_MEALS-07 records value 91.
- **Pass:** True — matched ['AUDIT-BETA-FINANCE_MEALS-07', '91']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-FINANCE_MEALS-07 on page 7 of beta_finance_meals.pdf is 91 (Source 1).

### beta_eng_deploy_p05
- **Org:** Beta Industries
- **Question:** In beta_eng_deploy.pdf, what value is recorded for audit token AUDIT-BETA-ENG_DEPLOY-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] Engineering Deploy Policy audit token AUDIT-BETA-ENG_DEPLOY-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-ENG_DEPLOY-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-ENG_DEPLOY-05 on page 5 of beta_eng_deploy.pdf is 65 (Source 1).

### beta_security_mfa_p05
- **Org:** Beta Industries
- **Question:** In beta_security_mfa.pdf, what value is recorded for audit token AUDIT-BETA-SECURITY_MFA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] Security MFA Policy audit token AUDIT-BETA-SECURITY_MFA-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-SECURITY_MFA-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-SECURITY_MFA-05 on page 5 of beta_security_mfa.pdf is 65 (Source 1).

### beta_sales_quota_p06
- **Org:** Beta Industries
- **Question:** In beta_sales_quota.pdf, what value is recorded for audit token AUDIT-BETA-SALES_QUOTA-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [BETA] Sales Quota Policy audit token AUDIT-BETA-SALES_QUOTA-06 records value 78.
- **Pass:** True — matched ['AUDIT-BETA-SALES_QUOTA-06', '78']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-SALES_QUOTA-06 on page 6 of beta_sales_quota.pdf is 78 (Source 1).

### beta_legal_nda_p05
- **Org:** Beta Industries
- **Question:** In beta_legal_nda.pdf, what value is recorded for audit token AUDIT-BETA-LEGAL_NDA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] Legal NDA Policy audit token AUDIT-BETA-LEGAL_NDA-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-LEGAL_NDA-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-LEGAL_NDA-05 on page 5 of the beta_legal_nda.pdf is 65 (Source 1).

### beta_ops_datacenter_p06
- **Org:** Beta Industries
- **Question:** In beta_ops_datacenter.pdf, what value is recorded for audit token AUDIT-BETA-OPS_DATACENTER-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [BETA] Operations Datacenter Policy audit token AUDIT-BETA-OPS_DATACENTER-06 records value 78.
- **Pass:** True — matched ['AUDIT-BETA-OPS_DATACENTER-06', '78']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-OPS_DATACENTER-06 on page 6 of beta_ops_datacenter.pdf is 78 (Source 1).

### beta_marketing_brand_p07
- **Org:** Beta Industries
- **Question:** In beta_marketing_brand.pdf, what value is recorded for audit token AUDIT-BETA-MARKETING_BRAND-07 on page 7?
- **Ground truth:** KEY_FACT PAGE 7: [BETA] Marketing Brand Policy audit token AUDIT-BETA-MARKETING_BRAND-07 records value 91.
- **Pass:** True — matched ['AUDIT-BETA-MARKETING_BRAND-07', '91']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-MARKETING_BRAND-07 on page 7 of beta_marketing_brand.pdf is 91 (Source 1).

### beta_support_sla_p05
- **Org:** Beta Industries
- **Question:** In beta_support_sla.pdf, what value is recorded for audit token AUDIT-BETA-SUPPORT_SLA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] Support SLA Policy audit token AUDIT-BETA-SUPPORT_SLA-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-SUPPORT_SLA-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-SUPPORT_SLA-05 on page 5 of beta_support_sla.pdf is 65 (Source 1).

### beta_product_roadmap_p06
- **Org:** Beta Industries
- **Question:** In beta_product_roadmap.pdf, what value is recorded for audit token AUDIT-BETA-PRODUCT_ROADMAP-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [BETA] Product Roadmap Policy audit token AUDIT-BETA-PRODUCT_ROADMAP-06 records value 78.
- **Pass:** True — matched ['AUDIT-BETA-PRODUCT_ROADMAP-06', '78']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-PRODUCT_ROADMAP-06 on page 6 of beta_product_roadmap.pdf is 78 (Source 1).

### beta_compliance_retention_p05
- **Org:** Beta Industries
- **Question:** In beta_compliance_retention.pdf, what value is recorded for audit token AUDIT-BETA-COMPLIANCE_RETENTION-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] Compliance Retention Policy audit token AUDIT-BETA-COMPLIANCE_RETENTION-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-COMPLIANCE_RETENTION-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-COMPLIANCE_RETENTION-05 on page 5 of beta_compliance_retention.pdf is 65 (Source 1).

### beta_training_budget_p05
- **Org:** Beta Industries
- **Question:** In beta_training_budget.pdf, what value is recorded for audit token AUDIT-BETA-TRAINING_BUDGET-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] Training Budget Policy audit token AUDIT-BETA-TRAINING_BUDGET-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-TRAINING_BUDGET-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-TRAINING_BUDGET-05 on page 5 of beta_training_budget.pdf is 65 (Source 1).

### beta_it_laptop_p05
- **Org:** Beta Industries
- **Question:** In beta_it_laptop.pdf, what value is recorded for audit token AUDIT-BETA-IT_LAPTOP-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] IT Laptop Policy audit token AUDIT-BETA-IT_LAPTOP-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-IT_LAPTOP-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-IT_LAPTOP-05 on page 5 of beta_it_laptop.pdf is 65 (Source 1).

### beta_procurement_approval_p06
- **Org:** Beta Industries
- **Question:** In beta_procurement_approval.pdf, what value is recorded for audit token AUDIT-BETA-PROCUREMENT_APPROVAL-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [BETA] Procurement Approval Policy audit token AUDIT-BETA-PROCUREMENT_APPROVAL-06 records value 78.
- **Pass:** True — matched ['AUDIT-BETA-PROCUREMENT_APPROVAL-06', '78']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-PROCUREMENT_APPROVAL-06 on page 6 of beta_procurement_approval.pdf is 78 (Source 1).

### beta_cs_onboarding_p05
- **Org:** Beta Industries
- **Question:** In beta_cs_onboarding.pdf, what value is recorded for audit token AUDIT-BETA-CS_ONBOARDING-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [BETA] Customer Success Onboarding Policy audit token AUDIT-BETA-CS_ONBOARDING-05 records value 65.
- **Pass:** True — matched ['AUDIT-BETA-CS_ONBOARDING-05', '65']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-BETA-CS_ONBOARDING-05 on page 5 of beta_cs_onboarding.pdf is 65 (Source 1).

### gamma_hr_vacation_p06
- **Org:** Gamma Solutions
- **Question:** In gamma_hr_vacation.pdf, what value is recorded for audit token AUDIT-GAMMA-HR_VACATION-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [GAMMA] HR Vacation Policy audit token AUDIT-GAMMA-HR_VACATION-06 records value 96.
- **Pass:** True — matched ['AUDIT-GAMMA-HR_VACATION-06', '96']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-HR_VACATION-06 on page 6 of gamma_hr_vacation.pdf is 96 (Source 1).

### gamma_finance_meals_p07
- **Org:** Gamma Solutions
- **Question:** In gamma_finance_meals.pdf, what value is recorded for audit token AUDIT-GAMMA-FINANCE_MEALS-07 on page 7?
- **Ground truth:** KEY_FACT PAGE 7: [GAMMA] Finance Meal Policy audit token AUDIT-GAMMA-FINANCE_MEALS-07 records value 112.
- **Pass:** True — matched ['AUDIT-GAMMA-FINANCE_MEALS-07', '112']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-FINANCE_MEALS-07 on page 7 of gamma_finance_meals.pdf is 112 (Source 1).

### gamma_eng_deploy_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_eng_deploy.pdf, what value is recorded for audit token AUDIT-GAMMA-ENG_DEPLOY-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] Engineering Deploy Policy audit token AUDIT-GAMMA-ENG_DEPLOY-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-ENG_DEPLOY-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-ENG_DEPLOY-05 on page 5 of gamma_eng_deploy.pdf is 80 (Source 1).

### gamma_security_mfa_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_security_mfa.pdf, what value is recorded for audit token AUDIT-GAMMA-SECURITY_MFA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] Security MFA Policy audit token AUDIT-GAMMA-SECURITY_MFA-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-SECURITY_MFA-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-SECURITY_MFA-05 on page 5 of gamma_security_mfa.pdf is 80 (Source 1).

### gamma_sales_quota_p06
- **Org:** Gamma Solutions
- **Question:** In gamma_sales_quota.pdf, what value is recorded for audit token AUDIT-GAMMA-SALES_QUOTA-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [GAMMA] Sales Quota Policy audit token AUDIT-GAMMA-SALES_QUOTA-06 records value 96.
- **Pass:** True — matched ['AUDIT-GAMMA-SALES_QUOTA-06', '96']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-SALES_QUOTA-06 on page 6 of gamma_sales_quota.pdf is 96 (Source 1).

### gamma_legal_nda_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_legal_nda.pdf, what value is recorded for audit token AUDIT-GAMMA-LEGAL_NDA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] Legal NDA Policy audit token AUDIT-GAMMA-LEGAL_NDA-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-LEGAL_NDA-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-LEGAL_NDA-05 on page 5 of gamma_legal_nda.pdf is 80 (Source 1).

### gamma_ops_datacenter_p06
- **Org:** Gamma Solutions
- **Question:** In gamma_ops_datacenter.pdf, what value is recorded for audit token AUDIT-GAMMA-OPS_DATACENTER-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [GAMMA] Operations Datacenter Policy audit token AUDIT-GAMMA-OPS_DATACENTER-06 records value 96.
- **Pass:** True — matched ['AUDIT-GAMMA-OPS_DATACENTER-06', '96']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-OPS_DATACENTER-06 on page 6 of gamma_ops_datacenter.pdf is 96 (Source 1).

### gamma_marketing_brand_p07
- **Org:** Gamma Solutions
- **Question:** In gamma_marketing_brand.pdf, what value is recorded for audit token AUDIT-GAMMA-MARKETING_BRAND-07 on page 7?
- **Ground truth:** KEY_FACT PAGE 7: [GAMMA] Marketing Brand Policy audit token AUDIT-GAMMA-MARKETING_BRAND-07 records value 112.
- **Pass:** True — matched ['AUDIT-GAMMA-MARKETING_BRAND-07', '112']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-MARKETING_BRAND-07 on page 7 of gamma_marketing_brand.pdf is 112 (Source 1).

### gamma_support_sla_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_support_sla.pdf, what value is recorded for audit token AUDIT-GAMMA-SUPPORT_SLA-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] Support SLA Policy audit token AUDIT-GAMMA-SUPPORT_SLA-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-SUPPORT_SLA-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-SUPPORT_SLA-05 on page 5 of gamma_support_sla.pdf is 80 (Source 1).

### gamma_product_roadmap_p06
- **Org:** Gamma Solutions
- **Question:** In gamma_product_roadmap.pdf, what value is recorded for audit token AUDIT-GAMMA-PRODUCT_ROADMAP-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [GAMMA] Product Roadmap Policy audit token AUDIT-GAMMA-PRODUCT_ROADMAP-06 records value 96.
- **Pass:** True — matched ['AUDIT-GAMMA-PRODUCT_ROADMAP-06', '96']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-PRODUCT_ROADMAP-06 on page 6 of gamma_product_roadmap.pdf is 96 (Source 1).

### gamma_compliance_retention_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_compliance_retention.pdf, what value is recorded for audit token AUDIT-GAMMA-COMPLIANCE_RETENTION-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] Compliance Retention Policy audit token AUDIT-GAMMA-COMPLIANCE_RETENTION-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-COMPLIANCE_RETENTION-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-COMPLIANCE_RETENTION-05 on page 5 of gamma_compliance_retention.pdf is 80 (Source 1).

### gamma_training_budget_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_training_budget.pdf, what value is recorded for audit token AUDIT-GAMMA-TRAINING_BUDGET-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] Training Budget Policy audit token AUDIT-GAMMA-TRAINING_BUDGET-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-TRAINING_BUDGET-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-TRAINING_BUDGET-05 on page 5 of gamma_training_budget.pdf is 80 (Source 1).

### gamma_it_laptop_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_it_laptop.pdf, what value is recorded for audit token AUDIT-GAMMA-IT_LAPTOP-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] IT Laptop Policy audit token AUDIT-GAMMA-IT_LAPTOP-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-IT_LAPTOP-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-IT_LAPTOP-05 on page 5 of gamma_it_laptop.pdf is 80 (Source 1).

### gamma_procurement_approval_p06
- **Org:** Gamma Solutions
- **Question:** In gamma_procurement_approval.pdf, what value is recorded for audit token AUDIT-GAMMA-PROCUREMENT_APPROVAL-06 on page 6?
- **Ground truth:** KEY_FACT PAGE 6: [GAMMA] Procurement Approval Policy audit token AUDIT-GAMMA-PROCUREMENT_APPROVAL-06 records value 96.
- **Pass:** True — matched ['AUDIT-GAMMA-PROCUREMENT_APPROVAL-06', '96']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-PROCUREMENT_APPROVAL-06 on page 6 of gamma_procurement_approval.pdf is 96 (Source 1).

### gamma_cs_onboarding_p05
- **Org:** Gamma Solutions
- **Question:** In gamma_cs_onboarding.pdf, what value is recorded for audit token AUDIT-GAMMA-CS_ONBOARDING-05 on page 5?
- **Ground truth:** KEY_FACT PAGE 5: [GAMMA] Customer Success Onboarding Policy audit token AUDIT-GAMMA-CS_ONBOARDING-05 records value 80.
- **Pass:** True — matched ['AUDIT-GAMMA-CS_ONBOARDING-05', '80']; type=page_fact; pdf_verified=True
- **Assistant answer:** The value recorded for audit token AUDIT-GAMMA-CS_ONBOARDING-05 on page 5 of gamma_cs_onboarding.pdf is 80 (Source 1).

### acme_hr_vacation_plast
- **Org:** Acme Corporation
- **Question:** According to acme_hr_vacation.pdf, what is the audit value on the last page (page 12) for token AUDIT-ACME-HR_VACATION-12?
- **Ground truth:** KEY_FACT PAGE 12: [ACME] HR Vacation Policy audit token AUDIT-ACME-HR_VACATION-12 records value 120.
- **Pass:** True — matched ['120', 'AUDIT-ACME-HR_VACATION-12']; type=late_page; pdf_verified=True
- **Assistant answer:** The audit value on the last page (page 12) for token AUDIT-ACME-HR_VACATION-12 is 120 (Source 1).

### acme_finance_meals_plast
- **Org:** Acme Corporation
- **Question:** According to acme_finance_meals.pdf, what is the audit value on the last page (page 15) for token AUDIT-ACME-FINANCE_MEALS-15?
- **Ground truth:** KEY_FACT PAGE 15: [ACME] Finance Meal Policy audit token AUDIT-ACME-FINANCE_MEALS-15 records value 150.
- **Pass:** True — matched ['150', 'AUDIT-ACME-FINANCE_MEALS-15']; type=late_page; pdf_verified=True
- **Assistant answer:** The audit value on the last page (page 15) for token AUDIT-ACME-FINANCE_MEALS-15 is 150 (Source 1).

### acme_eng_deploy_plast
- **Org:** Acme Corporation
- **Question:** According to acme_eng_deploy.pdf, what is the audit value on the last page (page 10) for token AUDIT-ACME-ENG_DEPLOY-10?
- **Ground truth:** KEY_FACT PAGE 10: [ACME] Engineering Deploy Policy audit token AUDIT-ACME-ENG_DEPLOY-10 records value 100.
- **Pass:** False — answer missing ground-truth terms ('100', 'AUDIT-ACME-ENG_DEPLOY-10')
- **Assistant answer:** The recorded value for audit token AUDIT-ACME-ENG_DEPLOY-05 on page 5 of acme_eng_deploy.pdf is 50 (Source 1).

### acme_security_mfa_plast
- **Org:** Acme Corporation
- **Question:** According to acme_security_mfa.pdf, what is the audit value on the last page (page 11) for token AUDIT-ACME-SECURITY_MFA-11?
- **Ground truth:** KEY_FACT PAGE 11: [ACME] Security MFA Policy audit token AUDIT-ACME-SECURITY_MFA-11 records value 110.
- **Pass:** True — matched ['110', 'AUDIT-ACME-SECURITY_MFA-11']; type=late_page; pdf_verified=True
- **Assistant answer:** The audit value on the last page (page 11) for token AUDIT-ACME-SECURITY_MFA-11 in the document acme_security_mfa.pdf is 110 (Source 1).

### acme_sales_quota_plast
- **Org:** Acme Corporation
- **Question:** According to acme_sales_quota.pdf, what is the audit value on the last page (page 13) for token AUDIT-ACME-SALES_QUOTA-13?
- **Ground truth:** KEY_FACT PAGE 13: [ACME] Sales Quota Policy audit token AUDIT-ACME-SALES_QUOTA-13 records value 130.
- **Pass:** False — answer missing ground-truth terms ('130', 'AUDIT-ACME-SALES_QUOTA-13')
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-SALES_QUOTA-06 on page 6 of acme_sales_quota.pdf is 60 (Source 1).

### acme_legal_nda_plast
- **Org:** Acme Corporation
- **Question:** According to acme_legal_nda.pdf, what is the audit value on the last page (page 11) for token AUDIT-ACME-LEGAL_NDA-11?
- **Ground truth:** KEY_FACT PAGE 11: [ACME] Legal NDA Policy audit token AUDIT-ACME-LEGAL_NDA-11 records value 110.
- **Pass:** True — matched ['110', 'AUDIT-ACME-LEGAL_NDA-11']; type=late_page; pdf_verified=True
- **Assistant answer:** The audit value on the last page (page 11) for token AUDIT-ACME-LEGAL_NDA-11 is 110 (Source 1).

### acme_ops_datacenter_plast
- **Org:** Acme Corporation
- **Question:** According to acme_ops_datacenter.pdf, what is the audit value on the last page (page 12) for token AUDIT-ACME-OPS_DATACENTER-12?
- **Ground truth:** KEY_FACT PAGE 12: [ACME] Operations Datacenter Policy audit token AUDIT-ACME-OPS_DATACENTER-12 records value 120.
- **Pass:** False — answer missing ground-truth terms ('120', 'AUDIT-ACME-OPS_DATACENTER-12')
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-OPS_DATACENTER-06 on page 6 of acme_ops_datacenter.pdf is 60 (Source 1).

### acme_marketing_brand_plast
- **Org:** Acme Corporation
- **Question:** According to acme_marketing_brand.pdf, what is the audit value on the last page (page 14) for token AUDIT-ACME-MARKETING_BRAND-14?
- **Ground truth:** KEY_FACT PAGE 14: [ACME] Marketing Brand Policy audit token AUDIT-ACME-MARKETING_BRAND-14 records value 140.
- **Pass:** False — answer missing ground-truth terms ('140', 'AUDIT-ACME-MARKETING_BRAND-14')
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-MARKETING_BRAND-07 on page 7 of acme_marketing_brand.pdf is 70 (Source 1).

### acme_support_sla_plast
- **Org:** Acme Corporation
- **Question:** According to acme_support_sla.pdf, what is the audit value on the last page (page 10) for token AUDIT-ACME-SUPPORT_SLA-10?
- **Ground truth:** KEY_FACT PAGE 10: [ACME] Support SLA Policy audit token AUDIT-ACME-SUPPORT_SLA-10 records value 100.
- **Pass:** False — answer missing ground-truth terms ('100', 'AUDIT-ACME-SUPPORT_SLA-10')
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-SUPPORT_SLA-05 on page 5 of acme_support_sla.pdf is 50 (Source 1).

### acme_product_roadmap_plast
- **Org:** Acme Corporation
- **Question:** According to acme_product_roadmap.pdf, what is the audit value on the last page (page 12) for token AUDIT-ACME-PRODUCT_ROADMAP-12?
- **Ground truth:** KEY_FACT PAGE 12: [ACME] Product Roadmap Policy audit token AUDIT-ACME-PRODUCT_ROADMAP-12 records value 120.
- **Pass:** False — answer missing ground-truth terms ('120', 'AUDIT-ACME-PRODUCT_ROADMAP-12')
- **Assistant answer:** The value recorded for audit token AUDIT-ACME-PRODUCT_ROADMAP-06 on page 6 of acme_product_roadmap.pdf is 60 (Source 1).

## Failures

- **acme_ops_datacenter_primary** (Acme Corporation, acme_ops_datacenter.pdf p1): answer missing ground-truth terms ('Dallas Texas',)
- **acme_cs_onboarding_primary** (Acme Corporation, acme_cs_onboarding.pdf p1): answer missing ground-truth terms ('30',)
- **beta_ops_datacenter_primary** (Beta Industries, beta_ops_datacenter.pdf p1): answer missing ground-truth terms ('Chicago Illinois',)
- **beta_it_laptop_primary** (Beta Industries, beta_it_laptop.pdf p1): answer missing ground-truth terms ('4',)
- **beta_cs_onboarding_primary** (Beta Industries, beta_cs_onboarding.pdf p1): answer missing ground-truth terms ('45',)
- **gamma_ops_datacenter_primary** (Gamma Solutions, gamma_ops_datacenter.pdf p1): answer missing ground-truth terms ('Austin Texas',)
- **gamma_procurement_approval_primary** (Gamma Solutions, gamma_procurement_approval.pdf p1): answer missing ground-truth terms ('7500',)
- **acme_eng_deploy_plast** (Acme Corporation, acme_eng_deploy.pdf p10): answer missing ground-truth terms ('100', 'AUDIT-ACME-ENG_DEPLOY-10')
- **acme_sales_quota_plast** (Acme Corporation, acme_sales_quota.pdf p13): answer missing ground-truth terms ('130', 'AUDIT-ACME-SALES_QUOTA-13')
- **acme_ops_datacenter_plast** (Acme Corporation, acme_ops_datacenter.pdf p12): answer missing ground-truth terms ('120', 'AUDIT-ACME-OPS_DATACENTER-12')
- **acme_marketing_brand_plast** (Acme Corporation, acme_marketing_brand.pdf p14): answer missing ground-truth terms ('140', 'AUDIT-ACME-MARKETING_BRAND-14')
- **acme_support_sla_plast** (Acme Corporation, acme_support_sla.pdf p10): answer missing ground-truth terms ('100', 'AUDIT-ACME-SUPPORT_SLA-10')
- **acme_product_roadmap_plast** (Acme Corporation, acme_product_roadmap.pdf p12): answer missing ground-truth terms ('120', 'AUDIT-ACME-PRODUCT_ROADMAP-12')

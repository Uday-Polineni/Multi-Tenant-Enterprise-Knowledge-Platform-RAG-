# EKA Regression Report

Generated: 2026-06-08T18:55:24.952874+00:00
Test org: `regression_2597c77a@example.com`
Duration: 120s

## Summary

| Metric | Result |
|--------|--------|
| Documents uploaded | 50/50 |
| API surface checks | 6/6 |
| RAG questions | 23/30 |

## UI / API surfaces exercised

| UI area | API endpoint | Covered |
|---------|--------------|---------|
| Auth (register/login) | POST /api/v1/auth/register, /login | yes |
| Chat query + stream | POST /api/v1/query/stream | yes |
| Admin upload | POST /api/v1/documents/upload | yes |
| Documents page (list/delete) | GET/DELETE /api/v1/documents | yes |
| Analytics panel | GET /api/v1/analytics/queries | yes |

### Surface check results

- **health**: PASS — HTTP 200
- **documents_list**: PASS — HTTP 200
- **analytics**: PASS — HTTP 200
- **query_stream**: PASS — HTTP 200
- **documents_get**: PASS — HTTP 200
- **documents_delete**: PASS — deleted 0f795c04-fbfe-4260-b53c-4d60902d6e7f

## RAG question results

| ID | Pass | Category | Latency | Detail |
|----|------|----------|---------|--------|
| pto_unique | PASS | hr | 1478 | matched: ['18'] |
| pto_short | PASS | size_variant | 1264 | matched: ['18'] |
| pto_long | PASS | size_variant | 3010 | matched: ['18'] |
| parental | PASS | hr | 1073 | matched: ['12'] |
| meal | PASS | finance | 1494 | matched: ['75'] |
| travel | PASS | finance | 1254 | matched: ['2000'] |
| oncall | PASS | engineering | 1115 | matched: ['pagerduty'] |
| deploy | PASS | engineering | 1510 | matched: ['tuesday', 'thursday'] |
| password | PASS | security | 1694 | matched: ['14'] |
| mfa | PASS | security | 1739 | matched: ['mfa', 'required'] |
| quota | PASS | sales | 1431 | matched: ['1.2'] |
| nda | PASS | legal | 2129 | matched: ['5'] |
| datacenter | PASS | ops | 1251 | matched: ['dallas'] |
| feature_x | PASS | product | 2159 | matched: ['q3', '2026'] |
| p1_sla | PASS | support | 1635 | matched: ['4'] |
| brand | PASS | marketing | 1520 | matched: ['2563eb'] |
| intern | PASS | intern | 1390 | matched: ['12'] |
| alex_skills | PASS | person | 3551 | matched: ['python', 'fastapi'] |
| jordan_skills | PASS | person | 1699 | matched: ['spark', 'airflow'] |
| portfolio_weekend | PASS | portfolio | 3114 | matched: ['weekend'] |
| alex_bad_dev | PASS | judgment | 4656 | matched: ['alex'] |
| morgan_judgment | FAIL | judgment | 1123 | missing any of ('morgan',) |
| multi_cross | FAIL | multi_doc | 1158 | missing any of ('250000', '6 months') |
| duplicate_pto | PASS | duplicate | 1698 | matched: ['18'] |
| no_context | FAIL | negative | 1419 | forbidden phrase present: ('not available',) |
| rag_acronym | PASS | engineering | 1010 | matched: ['retrieval augmented'] |
| remote_work | FAIL | hr | 1337 | missing any of ('3',) |
| retention | FAIL | security | 1149 | missing any of ('90',) |
| bonus | FAIL | finance | 1225 | missing any of ('12.5',) |
| fiscal | FAIL | finance | 1006 | missing any of ('march 31',) |

## Answers (excerpt)

### pto_unique: How many PTO days do employees get?
- **Pass:** True — matched: ['18']
- **Answer:** Employees receive an annual PTO allowance of 18 days (Source 1)....

### pto_short: What is the PTO allowance in the short vacation document?
- **Pass:** True — matched: ['18']
- **Answer:** The PTO allowance in the short vacation document is 18 days per employee (Source 1)....

### pto_long: How many annual PTO days in the long hr vacation variant?
- **Pass:** True — matched: ['18']
- **Answer:** The annual PTO allowance is 18 days per employee, as stated in multiple sources (Source 1, Source 3, Source 4, Source 5)....

### parental: How long is parental leave?
- **Pass:** True — matched: ['12']
- **Answer:** Parental leave is 12 weeks paid for primary caregivers (Source 1)....

### meal: What is the daily meal reimbursement limit?
- **Pass:** True — matched: ['75']
- **Answer:** The daily meal reimbursement limit is 75 dollars (Source 1)....

### travel: When does travel need VP approval?
- **Pass:** True — matched: ['2000']
- **Answer:** Travel needs VP pre-approval when the expenses exceed 2000 dollars (Source 1)....

### oncall: What tool is used for on-call rotation?
- **Pass:** True — matched: ['pagerduty']
- **Answer:** The tool used for on-call rotation is PagerDuty, and the handoffs occur weekly (Source 1)....

### deploy: Which days are production deploys allowed?
- **Pass:** True — matched: ['tuesday', 'thursday']
- **Answer:** Production deploys are allowed on Tuesday through Thursday only (Source 1)....

### password: Minimum password length?
- **Pass:** True — matched: ['14']
- **Answer:** The minimum password length is 14 characters (Source 1)....

### mfa: Is MFA required for VPN?
- **Pass:** True — matched: ['mfa', 'required']
- **Answer:** Yes, MFA is required for all VPN connections. This requirement is outlined in multiple sources, confirming the necessity of multi-factor authentication for accessing the VPN system (Source 1, Source 2)....

### quota: What is the Q1 sales quota?
- **Pass:** True — matched: ['1.2']
- **Answer:** The Q1 sales quota is 1.2 million dollars (Source 1)....

### nda: How long is the standard NDA term?
- **Pass:** True — matched: ['5']
- **Answer:** The standard NDA term is 5 years from the date of signature (Source 1)....

### datacenter: Where is the primary datacenter?
- **Pass:** True — matched: ['dallas']
- **Answer:** The primary datacenter is located in Dallas, Texas (Source 1)....

### feature_x: When does Feature X ship?
- **Pass:** True — matched: ['q3', '2026']
- **Answer:** Feature X is scheduled to ship in Q3 2026 (Source 1)....

### p1_sla: What is the P1 support SLA response time?
- **Pass:** True — matched: ['4']
- **Answer:** The P1 support SLA response time is 4 hours for the first response (Source 1)....

### brand: What is the brand primary color?
- **Pass:** True — matched: ['2563eb']
- **Answer:** The brand primary color is hex 2563eb (Source 1)....

### intern: How long is the internship program?
- **Pass:** True — matched: ['12']
- **Answer:** The internship program duration is 12 weeks (Source 1)....

### alex_skills: What skills does Alex Chen have?
- **Pass:** True — matched: ['python', 'fastapi']
- **Answer:** Alex Chen possesses several key skills as a Backend Software Engineer. He is proficient in Python and FastAPI, which he uses to build distributed APIs and services backed by PostgreSQL. Additionally, he has experience with Redis and AWS, broadening his expertise in backend technologies (Source 1)....

### jordan_skills: What does Jordan Lee specialize in?
- **Pass:** True — matched: ['spark', 'airflow']
- **Answer:** Jordan Lee specializes in Data Engineering, with a particular focus on Spark and Airflow. He designs ETL pipelines and warehouse models, showcasing his expertise in managing data workflows efficiently (Source 1)....

### portfolio_weekend: How long to finish portfolio v1?
- **Pass:** True — matched: ['weekend']
- **Answer:** Portfolio v1 can be finished in one weekend using a JSON-first React architecture. The tech stack for the portfolio includes React, TypeScript, Vite, and Tailwind CSS, and the sections include Hero, About, Experience, Projects, and Contact (Source 1)....

### alex_bad_dev: Is Alex Chen a bad developer?
- **Pass:** True — matched: ['alex']
- **Answer:** Based on the available information, I cannot categorize Alex Chen as a "bad developer." The context provides specific qualifications that illustrate his capabilities. Alex Chen is a Backend Software Engineer with 4 years of experience, specializing in Python and FastAPI. He has built distributed APIs and PostgreSQL-backed services and has demonstrated his skills by developing an event-driven billi...

### morgan_judgment: Is Morgan Taylor an experienced QA lead?
- **Pass:** False — missing any of ('morgan',)
- **Answer:** The information is not available in the uploaded documents....

### multi_cross: What is Project Falcon budget and timeline?
- **Pass:** False — missing any of ('250000', '6 months')
- **Answer:** The information is not available in the uploaded documents....

### duplicate_pto: How many PTO days according to duplicate vacation files?
- **Pass:** True — matched: ['18']
- **Answer:** According to the duplicate vacation files, the annual PTO allowance is 18 days per employee, as stated in multiple sources (Source 1, Source 2, Source 3, Source 5)....

### no_context: What is the capital of Mars Colony Seven?
- **Pass:** False — forbidden phrase present: ('not available',)
- **Answer:** The information is not available in the uploaded documents....

### rag_acronym: What does RAG mean in internal docs?
- **Pass:** True — matched: ['retrieval augmented']
- **Answer:** RAG means Retrieval Augmented Generation in internal docs (Source 1)....

### remote_work: How many days per week can employees work from home?
- **Pass:** False — missing any of ('3',)
- **Answer:** The information is not available in the uploaded documents....

### retention: How long are customer logs retained?
- **Pass:** False — missing any of ('90',)
- **Answer:** The information is not available in the uploaded documents....

### bonus: What percent is the bonus pool?
- **Pass:** False — missing any of ('12.5',)
- **Answer:** The information is not available in the uploaded documents....

### fiscal: When does the fiscal year end?
- **Pass:** False — missing any of ('march 31',)
- **Answer:** The information is not available in the uploaded documents....

## Bugs found & fixes

### Chroma index corruption on re-upload
- **Severity:** high
- **Symptom:** Vector search InternalError after document replace
- **Fix:** Explicit chunk-id delete, orphan prune, rebuild from Postgres (vector_store.py)

### Stale cache after upload
- **Severity:** high
- **Symptom:** Pre-upload 'no context' answers served after new docs indexed
- **Fix:** purge_org_query_cache on upload + embed complete (cache.py)

### Contradictory trailing 'not available' line
- **Severity:** medium
- **Symptom:** Partial answers followed by blanket not-available phrase
- **Fix:** normalize_llm_answer + prompt rules (rag.py)

### Judgment questions refused despite resume in context
- **Severity:** medium
- **Symptom:** 'Is X a bad developer?' returned not available
- **Fix:** RAG_USER_INSTRUCTIONS for subjective person questions (rag.py)

# Evaluation Results

| No. | Prompt Type | Prompt | Success | Error Count | Repair Attempts | Latency |
|---|---|---|---|---|---|---|
| 1 | Normal | Build a CRM with login, contacts, dashboard, analytics, and admin role access. | True | 0 | 0 | 1 ms |
| 2 | Normal | Build an ecommerce app with products, cart, orders, payments, and admin analytics. | True | 0 | 0 | 0 ms |
| 3 | Normal | Build a school management system with students, teachers, attendance, and marks. | True | 0 | 0 | 1 ms |
| 4 | Normal | Build a hospital appointment system with doctors, patients, booking, and payments. | True | 0 | 0 | 1.19 ms |
| 5 | Normal | Build a project management app with teams, tasks, deadlines, and progress tracking. | True | 0 | 0 | 0 ms |
| 6 | Normal | Build a food delivery app with restaurants, menus, orders, delivery tracking, and payments. | True | 0 | 0 | 0 ms |
| 7 | Normal | Build a job portal with candidates, companies, job posts, applications, and admin review. | True | 0 | 0 | 0 ms |
| 8 | Normal | Build a learning platform with courses, lessons, quizzes, certificates, and premium plans. | True | 0 | 0 | 0 ms |
| 9 | Normal | Build an inventory management system with products, suppliers, stock, and reports. | True | 0 | 0 | 0 ms |
| 10 | Normal | Build an event booking app with events, tickets, users, payments, and admin analytics. | True | 0 | 0 | 1.01 ms |
| 11 | Edge | Build a dashboard only. | True | 0 | 0 | 5.72 ms |
| 12 | Edge | Build payments without users. | True | 0 | 0 | 0 ms |
| 13 | Edge | Build role-based access but no roles. | True | 0 | 0 | 4.89 ms |
| 14 | Edge | Build an app with login but no users. | True | 0 | 0 | 0 ms |
| 15 | Edge | Build ecommerce but remove products. | True | 0 | 0 | 0 ms |
| 16 | Edge | Build a CRM with contacts but no database. | True | 0 | 0 | 0 ms |
| 17 | Edge | Build analytics for guests only. | True | 0 | 0 | 2.63 ms |
| 18 | Edge | Build premium plans but no payment system. | True | 0 | 0 | 0 ms |
| 19 | Edge | Build an admin panel where normal users can delete everything. | True | 0 | 0 | 0 ms |
| 20 | Edge | Build an app with contradictory roles: users cannot login but must manage dashboard. | True | 0 | 0 | 0 ms |

---

## Evaluation Summary

- Total prompts tested: 20
- Successful generations: 20/20
- Validation failures: 0
- Average repair attempts: 0
- Average latency: Low (< 6 ms)
- Structural consistency maintained across all prompts.

---

## Observed Strengths

- Stable structured output generation
- Strong schema consistency between UI, API, and database layers
- Automatic normalization of contradictory requirements
- Safe default authorization handling
- Deterministic and reliable architecture generation
- Low-latency execution
- Execution-aware runtime preview generation

---

## Known Limitations

- Some domain-specific prompts are generalized into reusable CRUD abstractions.
- Contradictions that conflict with core architecture assumptions are normalized into deployable structures instead of rejected.
- Guest-specific analytics and highly customized access policies are simplified into safer authenticated defaults.
- Real payment gateway integrations are not implemented; only schema-level payment modeling is supported.


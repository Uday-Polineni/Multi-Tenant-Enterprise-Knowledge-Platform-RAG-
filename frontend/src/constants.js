export const ACCESS_LEVELS = [
  { value: "public", label: "Public" },
  { value: "hr", label: "HR" },
  { value: "engineering", label: "Engineering" },
  { value: "finance", label: "Finance" },
  { value: "admin_only", label: "Admin only" },
];

export const INVITE_ROLES = [
  { value: "employee", label: "Employee" },
  { value: "manager", label: "Manager" },
  { value: "admin", label: "Admin" },
];

export const SUGGESTED_PROMPTS = [
  {
    title: "Benefits & location",
    text: "How many PTO days do employees get each year, and which city is our primary datacenter in?",
  },
  {
    title: "Travel & security",
    text: "What is the daily meal reimbursement limit, and what systems require MFA?",
  },
  {
    title: "Engineering ops",
    text: "Which days are production deploys allowed, and what is the P1 first-response support SLA?",
  },
  {
    title: "Sales & legal",
    text: "What is the Q1 sales quota target, and what is the standard NDA term in years?",
  },
];

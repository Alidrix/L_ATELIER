CREATE TABLE IF NOT EXISTS submissions (
  id SERIAL PRIMARY KEY,
  email_value TEXT NOT NULL,
  password_value TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

INSERT INTO submissions (email_value, password_value, created_at)
VALUES
  ('client_demo@company.test', 'SuperDemo!!', '2024-01-10T10:00:00Z'),
  ('test.account@corp.example', 'DemoPassword!', '2024-01-09T08:30:00Z');

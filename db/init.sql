CREATE TABLE IF NOT EXISTS submissions (
  id SERIAL PRIMARY KEY,
  email_value TEXT NOT NULL,
  password_value TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

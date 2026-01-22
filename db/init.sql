CREATE TABLE IF NOT EXISTS submissions (
  id SERIAL PRIMARY KEY,
  email_value TEXT NOT NULL,
  password_value TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);

INSERT INTO submissions (email_value, password_value, created_at)
VALUES
  ('Y2xpZW50X2RlbW9AY29tcGFueS50ZXN0', 'U3VwZXJEZW1vISE=', '2024-01-10T10:00:00Z'),
  ('dGVzdC5hY2NvdW50QGNvcnAuZXhhbXBsZQ==', 'RGVtb1Bhc3N3b3JkIQ==', '2024-01-09T08:30:00Z');

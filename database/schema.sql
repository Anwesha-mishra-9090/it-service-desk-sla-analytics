-- PostgreSQL Schema for IT Service Desk

-- Create database (run this separately in pgAdmin4)
-- CREATE DATABASE service_desk;

-- Connect to the database
-- \c service_desk;

-- Create tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    sla_deadline TIMESTAMP NOT NULL,
    sla_status VARCHAR(20) DEFAULT 'Within SLA',
    assigned_to VARCHAR(100),
    source VARCHAR(50) DEFAULT 'manual',
    
    -- Constraints
    CONSTRAINT check_category CHECK (category IN ('Network', 'Software', 'Hardware')),
    CONSTRAINT check_priority CHECK (priority IN ('High', 'Medium', 'Low')),
    CONSTRAINT check_status CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    CONSTRAINT check_sla_status CHECK (sla_status IN ('Within SLA', 'Near Breach', 'Breached'))
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
CREATE INDEX IF NOT EXISTS idx_tickets_sla_status ON tickets(sla_status);
CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at);
CREATE INDEX IF NOT EXISTS idx_tickets_assigned_to ON tickets(assigned_to);

-- Create composite indexes
CREATE INDEX IF NOT EXISTS idx_tickets_status_priority ON tickets(status, priority);
CREATE INDEX IF NOT EXISTS idx_tickets_created_sla ON tickets(created_at, sla_deadline);

-- Create function to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updated_at
DROP TRIGGER IF EXISTS update_tickets_updated_at ON tickets;
CREATE TRIGGER update_tickets_updated_at
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create view for SLA summary
CREATE OR REPLACE VIEW sla_summary AS
SELECT 
    priority,
    COUNT(*) as total_tickets,
    SUM(CASE WHEN sla_status = 'Within SLA' THEN 1 ELSE 0 END) as within_sla,
    SUM(CASE WHEN sla_status = 'Near Breach' THEN 1 ELSE 0 END) as near_breach,
    SUM(CASE WHEN sla_status = 'Breached' THEN 1 ELSE 0 END) as breached,
    ROUND(100.0 * SUM(CASE WHEN sla_status = 'Within SLA' THEN 1 ELSE 0 END) / COUNT(*), 2) as compliance_rate
FROM tickets
GROUP BY priority;

-- Create view for daily ticket trends
CREATE OR REPLACE VIEW daily_trends AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as tickets_created,
    SUM(CASE WHEN status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) as tickets_resolved
FROM tickets
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_user;
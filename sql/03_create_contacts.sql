-- Contacts Module tables

CREATE TABLE IF NOT EXISTS ahmf.contacts (
    contact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    company VARCHAR(500),
    role VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(100),
    contact_type VARCHAR(50) DEFAULT 'other',
    credit_score NUMERIC(5,2),
    notes TEXT,
    created_by UUID REFERENCES ahmf.users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contacts_type ON ahmf.contacts(contact_type);
CREATE INDEX IF NOT EXISTS idx_contacts_name ON ahmf.contacts(name);

CREATE TABLE IF NOT EXISTS ahmf.deal_contacts (
    deal_id UUID REFERENCES ahmf.deals(deal_id) ON DELETE CASCADE,
    contact_id UUID REFERENCES ahmf.contacts(contact_id) ON DELETE CASCADE,
    relationship_type VARCHAR(100),
    PRIMARY KEY (deal_id, contact_id)
);

CREATE TABLE IF NOT EXISTS ahmf.contact_activities (
    activity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES ahmf.contacts(contact_id) ON DELETE CASCADE,
    activity_type VARCHAR(100),
    description TEXT,
    created_by UUID REFERENCES ahmf.users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Deals Module tables

CREATE TABLE IF NOT EXISTS ahmf.deals (
    deal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    project_type VARCHAR(50) DEFAULT 'feature_film',
    genre VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pipeline',
    loan_amount NUMERIC(15,2),
    currency VARCHAR(10) DEFAULT 'USD',
    interest_rate NUMERIC(5,2),
    term_months INTEGER,
    borrower_name VARCHAR(500),
    producer VARCHAR(500),
    director VARCHAR(500),
    cast_summary TEXT,
    budget NUMERIC(15,2),
    territory TEXT,
    collateral_type VARCHAR(255),
    origination_date DATE,
    maturity_date DATE,
    notes JSONB DEFAULT '{}',
    created_by UUID REFERENCES ahmf.users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_deals_status ON ahmf.deals(status);
CREATE INDEX IF NOT EXISTS idx_deals_created_by ON ahmf.deals(created_by);

CREATE TABLE IF NOT EXISTS ahmf.deal_documents (
    doc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES ahmf.deals(deal_id) ON DELETE CASCADE,
    doc_type VARCHAR(100),
    filename VARCHAR(500),
    file_path TEXT,
    version INTEGER DEFAULT 1,
    uploaded_by UUID REFERENCES ahmf.users(user_id),
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ahmf.deal_approvals (
    approval_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES ahmf.deals(deal_id) ON DELETE CASCADE,
    stage VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    reviewer UUID REFERENCES ahmf.users(user_id),
    comments TEXT,
    decided_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS ahmf.deal_balances (
    balance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES ahmf.deals(deal_id) ON DELETE CASCADE,
    balance_type VARCHAR(50),
    amount NUMERIC(15,2),
    as_of_date DATE DEFAULT CURRENT_DATE,
    currency VARCHAR(10) DEFAULT 'USD'
);

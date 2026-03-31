-- Chat persistence tables

CREATE TABLE IF NOT EXISTS ahmf.chat_conversations (
    thread_id VARCHAR(255) PRIMARY KEY,
    user_id UUID REFERENCES ahmf.users(user_id),
    title VARCHAR(500) DEFAULT 'New chat',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ahmf.chat_messages (
    message_id VARCHAR(255) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    thread_id VARCHAR(255) REFERENCES ahmf.chat_conversations(thread_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_thread ON ahmf.chat_messages(thread_id, created_at);

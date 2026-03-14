-- Migration: 001_create_users.sql
-- Purpose: Create users table for authentication
-- Date: 2026-03-14

-- Enable UUID extension (required for UUID primary keys)
-- Note: Run this once per database on Neon
-- Requires superuser privileges or pre-enabled extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    -- Primary key: UUID with auto-generation
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Email: Unique, indexed, case-insensitive
    email VARCHAR(255) NOT NULL,
    
    -- Password: Bcrypt-hashed with salt
    hashed_password VARCHAR(255) NOT NULL,
    
    -- Account status: Active/inactive (soft delete)
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create case-insensitive unique index on email
-- This prevents duplicate emails with different casing
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email_lower 
ON users (LOWER(email));

-- Create regular index on email for fast lookups
CREATE INDEX IF NOT EXISTS ix_users_email 
ON users (email);

-- Create index on is_active for filtering active users
CREATE INDEX IF NOT EXISTS ix_users_is_active 
ON users (is_active);

-- Add comment to table
COMMENT ON TABLE users IS 'Registered user accounts for authentication';

-- Add comments to columns
COMMENT ON COLUMN users.id IS 'Unique identifier for the user';
COMMENT ON COLUMN users.email IS 'User email address (case-insensitive unique)';
COMMENT ON COLUMN users.hashed_password IS 'Bcrypt-hashed password with salt';
COMMENT ON COLUMN users.is_active IS 'Whether the account is active (soft delete)';
COMMENT ON COLUMN users.created_at IS 'Account creation timestamp';
COMMENT ON COLUMN users.updated_at IS 'Last update timestamp';

-- Create trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Verification query
-- SELECT COUNT(*) FROM users;

/**
 * User Model
 *
 * Defines the User data structure and type
 * Based on data model from PROJECT_BRIEF.md
 */

export type UserRole = 'admin' | 'team_lead' | 'member' | 'guest';

export interface User {
  id: string;                    // UUID
  email: string;                 // Unique email address
  password_hash: string;         // Bcrypt hashed password
  name: string;                  // Display name
  role: UserRole;                // User role for RBAC
  avatar_url: string | null;     // Optional profile picture URL
  created_at: Date;              // Account creation timestamp
  updated_at: Date;              // Last update timestamp
}

export interface UserCreateInput {
  email: string;
  password_hash: string;
  name: string;
  role?: UserRole;
  avatar_url?: string | null;
}

export interface UserUpdateInput {
  name?: string;
  role?: UserRole;
  avatar_url?: string | null;
}

/**
 * Safe user object without sensitive data
 * Used for API responses
 */
export type SafeUser = Omit<User, 'password_hash'>;

/**
 * User profile with additional computed fields
 */
export interface UserProfile extends SafeUser {
  task_count?: number;
  project_count?: number;
  completed_tasks?: number;
}

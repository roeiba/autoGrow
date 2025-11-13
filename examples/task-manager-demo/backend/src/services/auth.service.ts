/**
 * Authentication Service
 *
 * Handles user registration, login, and token generation
 * Implements JWT-based authentication as specified in PROJECT_BRIEF.md
 */

import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';
import { logger } from '../config/logger';
import { User, UserRole } from '../models/User';
import { db } from '../config/database';

interface RegisterInput {
  email: string;
  password: string;
  name: string;
}

interface LoginInput {
  email: string;
  password: string;
}

interface TokenPayload {
  userId: string;
  email: string;
  role: UserRole;
}

export class AuthService {
  private readonly JWT_SECRET: string;
  private readonly JWT_EXPIRY: string = '7d';
  private readonly SALT_ROUNDS: number = 10;

  constructor() {
    this.JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

    if (this.JWT_SECRET === 'your-secret-key-change-in-production') {
      logger.warn('Using default JWT_SECRET - CHANGE THIS IN PRODUCTION!');
    }
  }

  /**
   * Register a new user
   * - Validates email uniqueness
   * - Hashes password with bcrypt
   * - Creates user record
   * - Returns JWT token
   */
  async register(input: RegisterInput): Promise<{ user: User; token: string }> {
    const { email, password, name } = input;

    // Check if user already exists
    const existingUser = await this.findUserByEmail(email);
    if (existingUser) {
      throw new Error('User with this email already exists');
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, this.SALT_ROUNDS);

    // Create user
    const userId = uuidv4();
    const user: User = {
      id: userId,
      email,
      password_hash: passwordHash,
      name,
      role: 'member' as UserRole,
      avatar_url: null,
      created_at: new Date(),
      updated_at: new Date()
    };

    // Insert into database
    await db('users').insert({
      id: user.id,
      email: user.email,
      password_hash: user.password_hash,
      name: user.name,
      role: user.role,
      avatar_url: user.avatar_url,
      created_at: user.created_at,
      updated_at: user.updated_at
    });

    logger.info(`User registered: ${email}`);

    // Generate token
    const token = this.generateToken(user);

    // Remove password_hash before returning
    const { password_hash, ...userWithoutPassword } = user;

    return { user: userWithoutPassword as User, token };
  }

  /**
   * Login existing user
   * - Validates credentials
   * - Returns JWT token
   */
  async login(input: LoginInput): Promise<{ user: User; token: string }> {
    const { email, password } = input;

    // Find user
    const user = await this.findUserByEmail(email);
    if (!user) {
      throw new Error('Invalid email or password');
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    if (!isValidPassword) {
      throw new Error('Invalid email or password');
    }

    logger.info(`User logged in: ${email}`);

    // Generate token
    const token = this.generateToken(user);

    // Remove password_hash before returning
    const { password_hash, ...userWithoutPassword } = user;

    return { user: userWithoutPassword as User, token };
  }

  /**
   * Verify JWT token and return user
   */
  async verifyToken(token: string): Promise<User> {
    try {
      const payload = jwt.verify(token, this.JWT_SECRET) as TokenPayload;

      const user = await this.findUserById(payload.userId);
      if (!user) {
        throw new Error('User not found');
      }

      const { password_hash, ...userWithoutPassword } = user;
      return userWithoutPassword as User;
    } catch (error) {
      throw new Error('Invalid or expired token');
    }
  }

  /**
   * Generate JWT token for user
   */
  private generateToken(user: User): string {
    const payload: TokenPayload = {
      userId: user.id,
      email: user.email,
      role: user.role
    };

    return jwt.sign(payload, this.JWT_SECRET, {
      expiresIn: this.JWT_EXPIRY
    });
  }

  /**
   * Find user by email
   */
  private async findUserByEmail(email: string): Promise<User | null> {
    const users = await db('users').where({ email }).select('*');
    return users.length > 0 ? users[0] : null;
  }

  /**
   * Find user by ID
   */
  private async findUserById(id: string): Promise<User | null> {
    const users = await db('users').where({ id }).select('*');
    return users.length > 0 ? users[0] : null;
  }

  /**
   * Update user password
   */
  async updatePassword(userId: string, currentPassword: string, newPassword: string): Promise<void> {
    const user = await this.findUserById(userId);
    if (!user) {
      throw new Error('User not found');
    }

    // Verify current password
    const isValid = await bcrypt.compare(currentPassword, user.password_hash);
    if (!isValid) {
      throw new Error('Current password is incorrect');
    }

    // Hash new password
    const newPasswordHash = await bcrypt.hash(newPassword, this.SALT_ROUNDS);

    // Update database
    await db('users')
      .where({ id: userId })
      .update({
        password_hash: newPasswordHash,
        updated_at: new Date()
      });

    logger.info(`Password updated for user: ${user.email}`);
  }

  /**
   * Request password reset
   * TODO: Implement email sending with reset token
   */
  async requestPasswordReset(email: string): Promise<void> {
    const user = await this.findUserByEmail(email);
    if (!user) {
      // Don't reveal if email exists
      logger.info(`Password reset requested for non-existent email: ${email}`);
      return;
    }

    // TODO: Generate reset token, store in database, send email
    logger.info(`Password reset requested for: ${email}`);
    throw new Error('Password reset not yet implemented');
  }
}

export const authService = new AuthService();

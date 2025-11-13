/**
 * Task Model
 * Represents a task in the system
 */

const { DataTypes } = require('sequelize');
const { sequelize } = require('../database');

const Task = sequelize.define('Task', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },

  projectId: {
    type: DataTypes.UUID,
    allowNull: false,
    field: 'project_id',
    references: {
      model: 'projects',
      key: 'id'
    }
  },

  title: {
    type: DataTypes.STRING(200),
    allowNull: false,
    validate: {
      notEmpty: true,
      len: [1, 200]
    }
  },

  description: {
    type: DataTypes.TEXT,
    allowNull: true
  },

  status: {
    type: DataTypes.ENUM('todo', 'in_progress', 'review', 'done'),
    defaultValue: 'todo',
    allowNull: false
  },

  priority: {
    type: DataTypes.ENUM('low', 'medium', 'high', 'urgent'),
    defaultValue: 'medium',
    allowNull: false
  },

  assigneeId: {
    type: DataTypes.UUID,
    allowNull: true,
    field: 'assignee_id',
    references: {
      model: 'users',
      key: 'id'
    }
  },

  createdById: {
    type: DataTypes.UUID,
    allowNull: false,
    field: 'created_by_id',
    references: {
      model: 'users',
      key: 'id'
    }
  },

  dueDate: {
    type: DataTypes.DATE,
    allowNull: true,
    field: 'due_date'
  },

  completedAt: {
    type: DataTypes.DATE,
    allowNull: true,
    field: 'completed_at'
  },

  tags: {
    type: DataTypes.ARRAY(DataTypes.STRING),
    defaultValue: []
  }
}, {
  tableName: 'tasks',
  timestamps: true,
  underscored: true,
  indexes: [
    {
      fields: ['project_id']
    },
    {
      fields: ['assignee_id']
    },
    {
      fields: ['status']
    },
    {
      fields: ['priority']
    },
    {
      fields: ['due_date']
    },
    {
      fields: ['created_at']
    }
  ],
  hooks: {
    beforeUpdate: (task) => {
      // Set completedAt timestamp when status changes to done
      if (task.changed('status') && task.status === 'done' && !task.completedAt) {
        task.completedAt = new Date();
      }

      // Clear completedAt if status changes from done to something else
      if (task.changed('status') && task.status !== 'done' && task.completedAt) {
        task.completedAt = null;
      }
    }
  }
});

// Define associations
Task.associate = (models) => {
  Task.belongsTo(models.Project, {
    foreignKey: 'projectId',
    as: 'project'
  });

  Task.belongsTo(models.User, {
    foreignKey: 'assigneeId',
    as: 'assignee'
  });

  Task.belongsTo(models.User, {
    foreignKey: 'createdById',
    as: 'creator'
  });

  Task.hasMany(models.Comment, {
    foreignKey: 'taskId',
    as: 'comments',
    onDelete: 'CASCADE'
  });
};

// Instance methods
Task.prototype.toJSON = function() {
  const values = { ...this.get() };

  // Remove sensitive or internal fields
  delete values.deletedAt;

  return values;
};

module.exports = Task;

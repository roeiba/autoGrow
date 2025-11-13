/**
 * Task Card Component
 *
 * Displays a single task in a card format
 * Used in task lists and dashboards
 */

import { Task, TaskStatus, TaskPriority } from '../../types/task';
import { formatDate } from '../../utils/dateUtils';
import { useTasks } from '../../hooks/useTasks';

interface TaskCardProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string) => void;
}

/**
 * Get color class for task priority
 */
function getPriorityColor(priority: TaskPriority): string {
  const colors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    urgent: 'bg-red-100 text-red-800'
  };
  return colors[priority] || colors.medium;
}

/**
 * Get color class for task status
 */
function getStatusColor(status: TaskStatus): string {
  const colors = {
    todo: 'bg-gray-100 text-gray-800',
    in_progress: 'bg-blue-100 text-blue-800',
    in_review: 'bg-purple-100 text-purple-800',
    done: 'bg-green-100 text-green-800'
  };
  return colors[status] || colors.todo;
}

/**
 * Format status for display
 */
function formatStatus(status: TaskStatus): string {
  const labels = {
    todo: 'To Do',
    in_progress: 'In Progress',
    in_review: 'In Review',
    done: 'Done'
  };
  return labels[status] || status;
}

export function TaskCard({ task, onEdit, onDelete }: TaskCardProps) {
  const { updateTaskStatus } = useTasks();

  const handleStatusChange = async (newStatus: TaskStatus) => {
    try {
      await updateTaskStatus(task.id, newStatus);
    } catch (error) {
      console.error('Failed to update task status:', error);
    }
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && task.status !== 'done';

  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow cursor-pointer"
      onClick={() => onEdit && onEdit(task)}
      data-testid="task-card"
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-semibold text-gray-900 flex-1">
          {task.title}
        </h3>

        {/* Priority Badge */}
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
          {task.priority.toUpperCase()}
        </span>
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {task.description}
        </p>
      )}

      {/* Status */}
      <div className="mb-3">
        <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
          {formatStatus(task.status)}
        </span>
      </div>

      {/* Due Date */}
      {task.due_date && (
        <div className={`text-sm mb-3 ${isOverdue ? 'text-red-600 font-semibold' : 'text-gray-500'}`}>
          {isOverdue && '⚠️ '}
          Due: {formatDate(task.due_date)}
        </div>
      )}

      {/* Assignee */}
      {task.assignee_name && (
        <div className="text-sm text-gray-600 mb-3">
          Assigned to: <span className="font-medium">{task.assignee_name}</span>
        </div>
      )}

      {/* Tags */}
      {task.tags && task.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {task.tags.map(tag => (
            <span
              key={tag.id}
              className="px-2 py-1 rounded text-xs"
              style={{ backgroundColor: tag.color + '20', color: tag.color }}
            >
              {tag.name}
            </span>
          ))}
        </div>
      )}

      {/* Actions */}
      <div className="flex justify-between items-center pt-3 border-t border-gray-200">
        {/* Quick Status Update */}
        <select
          value={task.status}
          onChange={(e) => {
            e.stopPropagation();
            handleStatusChange(e.target.value as TaskStatus);
          }}
          className="text-sm border border-gray-300 rounded px-2 py-1"
          onClick={(e) => e.stopPropagation()}
        >
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="in_review">In Review</option>
          <option value="done">Done</option>
        </select>

        {/* Delete Button */}
        {onDelete && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              if (window.confirm('Are you sure you want to delete this task?')) {
                onDelete(task.id);
              }
            }}
            className="text-red-600 hover:text-red-800 text-sm"
          >
            Delete
          </button>
        )}
      </div>

      {/* Footer - Created Date */}
      <div className="text-xs text-gray-400 mt-2">
        Created {formatDate(task.created_at)}
      </div>
    </div>
  );
}

const express = require('express');
const Query = require('../models/Query');
const User = require('../models/User');
const auth = require('../middleware/auth');

const router = express.Router();

// Get user analytics dashboard
router.get('/dashboard', auth, async (req, res) => {
  try {
    const userId = req.user.userId;
    
    // Get date range (default to last 30 days)
    const days = parseInt(req.query.days) || 30;
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    // Total queries
    const totalQueries = await Query.countDocuments({ userId });
    
    // Successful queries
    const successfulQueries = await Query.countDocuments({ 
      userId, 
      success: true 
    });

    // Recent queries (last 7 days)
    const recentQueries = await Query.countDocuments({
      userId,
      createdAt: { $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) }
    });

    // Query categories breakdown
    const categoryStats = await Query.aggregate([
      { $match: { userId: req.user.userId } },
      { $group: { _id: '$category', count: { $sum: 1 } } }
    ]);

    // Success rate over time
    const successRateOverTime = await Query.aggregate([
      { 
        $match: { 
          userId: req.user.userId,
          createdAt: { $gte: startDate }
        }
      },
      {
        $group: {
          _id: { 
            $dateToString: { 
              format: '%Y-%m-%d', 
              date: '$createdAt' 
            }
          },
          total: { $sum: 1 },
          successful: { 
            $sum: { $cond: ['$success', 1, 0] }
          }
        }
      },
      { $sort: { _id: 1 } }
    ]);

    // Average execution time
    const avgExecutionTime = await Query.aggregate([
      { 
        $match: { 
          userId: req.user.userId,
          success: true,
          executionTime: { $gt: 0 }
        }
      },
      {
        $group: {
          _id: null,
          avgTime: { $avg: '$executionTime' }
        }
      }
    ]);

    // Most common query patterns
    const commonPatterns = await Query.aggregate([
      { $match: { userId: req.user.userId, success: true } },
      {
        $group: {
          _id: '$category',
          count: { $sum: 1 },
          avgExecutionTime: { $avg: '$executionTime' },
          examples: { $push: '$originalQuery' }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 5 }
    ]);

    // User feedback analysis
    const feedbackStats = await Query.aggregate([
      { 
        $match: { 
          userId: req.user.userId,
          'feedback.rating': { $exists: true }
        }
      },
      {
        $group: {
          _id: null,
          avgRating: { $avg: '$feedback.rating' },
          totalFeedback: { $sum: 1 }
        }
      }
    ]);

    res.json({
      success: true,
      analytics: {
        overview: {
          totalQueries,
          successfulQueries,
          recentQueries,
          successRate: totalQueries > 0 ? (successfulQueries / totalQueries * 100).toFixed(1) : 0,
          avgExecutionTime: avgExecutionTime[0]?.avgTime || 0
        },
        categoryBreakdown: categoryStats,
        successRateOverTime,
        commonPatterns,
        feedback: feedbackStats[0] || { avgRating: 0, totalFeedback: 0 }
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to get analytics',
      error: error.message
    });
  }
});

// Get system-wide analytics (admin only)
router.get('/system', auth, async (req, res) => {
  try {
    // Check if user is admin
    const user = await User.findById(req.user.userId);
    if (!user || user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        message: 'Access denied. Admin role required.'
      });
    }

    const days = parseInt(req.query.days) || 30;
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    // Total system stats
    const totalUsers = await User.countDocuments({ isActive: true });
    const totalQueries = await Query.countDocuments();
    const totalSuccessfulQueries = await Query.countDocuments({ success: true });

    // Active users (users who made queries in the last 7 days)
    const activeUsers = await Query.distinct('userId', {
      createdAt: { $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) }
    });

    // Query volume over time
    const queryVolumeOverTime = await Query.aggregate([
      { 
        $match: { 
          createdAt: { $gte: startDate }
        }
      },
      {
        $group: {
          _id: { 
            $dateToString: { 
              format: '%Y-%m-%d', 
              date: '$createdAt' 
            }
          },
          total: { $sum: 1 },
          successful: { 
            $sum: { $cond: ['$success', 1, 0] }
          },
          uniqueUsers: { $addToSet: '$userId' }
        }
      },
      { 
        $addFields: {
          uniqueUsersCount: { $size: '$uniqueUsers' }
        }
      },
      { $sort: { _id: 1 } }
    ]);

    // Most popular query categories
    const popularCategories = await Query.aggregate([
      { $group: { _id: '$category', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);

    // Error analysis
    const errorAnalysis = await Query.aggregate([
      { $match: { success: false } },
      { 
        $group: { 
          _id: '$errorMessage', 
          count: { $sum: 1 },
          examples: { $push: '$originalQuery' }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 10 }
    ]);

    // Performance metrics
    const performanceMetrics = await Query.aggregate([
      { 
        $match: { 
          success: true,
          executionTime: { $gt: 0 }
        }
      },
      {
        $group: {
          _id: null,
          avgExecutionTime: { $avg: '$executionTime' },
          maxExecutionTime: { $max: '$executionTime' },
          minExecutionTime: { $min: '$executionTime' }
        }
      }
    ]);

    res.json({
      success: true,
      systemAnalytics: {
        overview: {
          totalUsers,
          activeUsers: activeUsers.length,
          totalQueries,
          successRate: totalQueries > 0 ? (totalSuccessfulQueries / totalQueries * 100).toFixed(1) : 0
        },
        queryVolumeOverTime,
        popularCategories,
        errorAnalysis,
        performance: performanceMetrics[0] || {}
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to get system analytics',
      error: error.message
    });
  }
});

module.exports = router;

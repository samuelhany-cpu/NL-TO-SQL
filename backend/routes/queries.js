const express = require('express');
const axios = require('axios');
const Joi = require('joi');
const Query = require('../models/Query');
const auth = require('../middleware/auth');

const router = express.Router();

// Validation schema
const querySchema = Joi.object({
  query: Joi.string().min(1).required(),
  includeVisualization: Joi.boolean().default(false)
});

const feedbackSchema = Joi.object({
  rating: Joi.number().min(1).max(5).required(),
  comment: Joi.string().allow('').optional()
});

// Parse natural language query
router.post('/parse', auth, async (req, res) => {
  const startTime = Date.now();
  
  try {
    const { error } = querySchema.validate(req.body);
    if (error) {
      return res.status(400).json({
        success: false,
        message: error.details[0].message
      });
    }

    const { query, includeVisualization } = req.body;

    // Call FastAPI service
    const fastApiUrl = process.env.FASTAPI_URL || 'http://localhost:8000';
    const response = await axios.post(`${fastApiUrl}/parse`, {
      query,
      include_visualization: includeVisualization
    }, {
      timeout: 30000 // 30 seconds timeout
    });

    const executionTime = Date.now() - startTime;
    const result = response.data;

    // Save query to database
    const queryRecord = new Query({
      userId: req.user.userId,
      originalQuery: query,
      correctedQuery: result.corrected_query,
      sqlQueries: result.sql_queries.map(sql => ({ sql })),
      results: result.results,
      success: result.success,
      executionTime,
      category: categorizeQuery(query),
      complexity: determineComplexity(query)
    });

    await queryRecord.save();

    res.json({
      success: true,
      queryId: queryRecord._id,
      data: result,
      executionTime
    });

  } catch (error) {
    const executionTime = Date.now() - startTime;
    
    // Save failed query to database
    try {
      const queryRecord = new Query({
        userId: req.user.userId,
        originalQuery: req.body.query || '',
        success: false,
        errorMessage: error.response?.data?.detail || error.message,
        executionTime
      });
      await queryRecord.save();
    } catch (dbError) {
      console.error('Failed to save error query:', dbError);
    }

    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        success: false,
        message: 'NL-to-SQL service is unavailable',
        error: 'Service connection failed'
      });
    }

    res.status(500).json({
      success: false,
      message: 'Query parsing failed',
      error: error.response?.data?.detail || error.message
    });
  }
});

// Get user's query history
router.get('/history', auth, async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const skip = (page - 1) * limit;

    const queries = await Query.find({ userId: req.user.userId })
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .select('-results'); // Exclude large results field

    const total = await Query.countDocuments({ userId: req.user.userId });

    res.json({
      success: true,
      queries,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to get query history',
      error: error.message
    });
  }
});

// Get specific query details
router.get('/:queryId', auth, async (req, res) => {
  try {
    const query = await Query.findOne({
      _id: req.params.queryId,
      userId: req.user.userId
    });

    if (!query) {
      return res.status(404).json({
        success: false,
        message: 'Query not found'
      });
    }

    res.json({
      success: true,
      query
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to get query',
      error: error.message
    });
  }
});

// Add feedback to a query
router.post('/:queryId/feedback', auth, async (req, res) => {
  try {
    const { error } = feedbackSchema.validate(req.body);
    if (error) {
      return res.status(400).json({
        success: false,
        message: error.details[0].message
      });
    }

    const query = await Query.findOne({
      _id: req.params.queryId,
      userId: req.user.userId
    });

    if (!query) {
      return res.status(404).json({
        success: false,
        message: 'Query not found'
      });
    }

    query.feedback = {
      rating: req.body.rating,
      comment: req.body.comment || '',
      timestamp: new Date()
    };

    await query.save();

    res.json({
      success: true,
      message: 'Feedback added successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to add feedback',
      error: error.message
    });
  }
});

// Delete a query
router.delete('/:queryId', auth, async (req, res) => {
  try {
    const query = await Query.findOneAndDelete({
      _id: req.params.queryId,
      userId: req.user.userId
    });

    if (!query) {
      return res.status(404).json({
        success: false,
        message: 'Query not found'
      });
    }

    res.json({
      success: true,
      message: 'Query deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to delete query',
      error: error.message
    });
  }
});

// Helper functions
function categorizeQuery(query) {
  const lowerQuery = query.toLowerCase();
  
  if (lowerQuery.includes('inventory') || lowerQuery.includes('stock') || lowerQuery.includes('units')) {
    return 'inventory';
  }
  if (lowerQuery.includes('sale') || lowerQuery.includes('revenue') || lowerQuery.includes('price')) {
    return 'sales';
  }
  if (lowerQuery.includes('product') || lowerQuery.includes('item') || lowerQuery.includes('mobile') || lowerQuery.includes('tv')) {
    return 'products';
  }
  
  return 'general';
}

function determineComplexity(query) {
  const words = query.split(' ').length;
  const hasMultipleQuestions = query.includes('?');
  const hasJoins = query.toLowerCase().includes('and') || query.toLowerCase().includes('or');
  
  if (words > 15 || hasMultipleQuestions || hasJoins) {
    return 'complex';
  }
  if (words > 8) {
    return 'medium';
  }
  
  return 'simple';
}

module.exports = router;

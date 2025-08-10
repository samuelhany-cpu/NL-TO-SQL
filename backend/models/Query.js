const mongoose = require('mongoose');

const querySchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  originalQuery: {
    type: String,
    required: true,
    trim: true
  },
  correctedQuery: {
    type: String,
    trim: true
  },
  sqlQueries: [{
    sql: String,
    executionTime: Number,
    resultCount: Number
  }],
  results: {
    type: mongoose.Schema.Types.Mixed
  },
  success: {
    type: Boolean,
    required: true
  },
  errorMessage: {
    type: String
  },
  executionTime: {
    type: Number, // in milliseconds
    default: 0
  },
  category: {
    type: String,
    enum: ['inventory', 'sales', 'products', 'general'],
    default: 'general'
  },
  complexity: {
    type: String,
    enum: ['simple', 'medium', 'complex'],
    default: 'simple'
  },
  feedback: {
    rating: {
      type: Number,
      min: 1,
      max: 5
    },
    comment: String,
    timestamp: {
      type: Date,
      default: Date.now
    }
  }
}, {
  timestamps: true
});

// Index for better query performance
querySchema.index({ userId: 1, createdAt: -1 });
querySchema.index({ success: 1 });
querySchema.index({ category: 1 });

module.exports = mongoose.model('Query', querySchema);

import React from 'react'

const History = () => {
  // Placeholder data
  const queries = [
    {
      id: 1,
      query: "How many mobiles do we have?",
      sql: "SELECT COUNT(*) FROM products WHERE category = 'mobile'",
      success: true,
      timestamp: "2025-08-10 14:30:22",
      executionTime: 45
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Query History</h1>
            <p className="mt-1 text-sm text-gray-600">
              View and manage your previous natural language queries
            </p>
          </div>
          <div className="flex space-x-3">
            <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
              📊 Export
            </button>
            <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700">
              🔍 Filter
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Search queries</label>
            <input
              type="text"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="Search by query text..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Status</label>
            <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
              <option>All</option>
              <option>Successful</option>
              <option>Failed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Date Range</label>
            <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
              <option>Last 7 days</option>
              <option>Last 30 days</option>
              <option>Last 90 days</option>
              <option>All time</option>
            </select>
          </div>
        </div>
      </div>

      {/* Query List */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Queries</h3>
        </div>
        
        {queries.length === 0 ? (
          <div className="text-center py-12">
            <span className="text-6xl">📝</span>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No queries yet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Start by parsing your first natural language query!
            </p>
            <div className="mt-6">
              <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
                🚀 Create Query
              </button>
            </div>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {queries.map((query) => (
              <div key={query.id} className="p-6 hover:bg-gray-50">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        query.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {query.success ? '✅ Success' : '❌ Failed'}
                      </span>
                      <span className="text-sm text-gray-500">{query.timestamp}</span>
                      <span className="text-sm text-gray-500">({query.executionTime}ms)</span>
                    </div>
                    
                    <h4 className="mt-2 text-lg font-medium text-gray-900">
                      {query.query}
                    </h4>
                    
                    <div className="mt-2">
                      <p className="text-sm text-gray-600">Generated SQL:</p>
                      <pre className="mt-1 text-sm text-gray-900 bg-gray-100 p-2 rounded overflow-x-auto">
                        {query.sql}
                      </pre>
                    </div>
                  </div>
                  
                  <div className="ml-4 flex space-x-2">
                    <button className="text-sm text-primary-600 hover:text-primary-800">
                      View Details
                    </button>
                    <button className="text-sm text-gray-400 hover:text-gray-600">
                      Rerun
                    </button>
                    <button className="text-sm text-red-400 hover:text-red-600">
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Pagination placeholder */}
      {queries.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div className="flex-1 flex justify-between sm:hidden">
              <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Previous
              </button>
              <button className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Next
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Showing <span className="font-medium">1</span> to <span className="font-medium">1</span> of{' '}
                  <span className="font-medium">1</span> results
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Previous
                  </button>
                  <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
                    1
                  </button>
                  <button className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Next
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default History

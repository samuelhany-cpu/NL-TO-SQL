import React, { useState } from 'react'
import { toast } from 'react-hot-toast'
import LoadingSpinner from '../components/LoadingSpinner'

const QueryParser = () => {
  const [query, setQuery] = useState('')
  const [includeVisualization, setIncludeVisualization] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!query.trim()) {
      toast.error('Please enter a query')
      return
    }

    setLoading(true)
    try {
      // This would call the actual API
      // For now, just simulate the response
      setTimeout(() => {
        setResult({
          success: true,
          original_query: query,
          sql_queries: ['SELECT * FROM products WHERE category = "mobile"'],
          results: [
            {
              sql: 'SELECT * FROM products WHERE category = "mobile"',
              data: [
                { id: 'MOB-001', name: 'iPhone 13', units: 50 },
                { id: 'MOB-002', name: 'Samsung Galaxy', units: 30 }
              ],
              count: 2
            }
          ]
        })
        setLoading(false)
        toast.success('Query parsed successfully!')
      }, 2000)
    } catch (error) {
      setLoading(false)
      toast.error('Failed to parse query')
    }
  }

  const exampleQueries = [
    "How many mobiles do we have?",
    "Show me all TVs in stock",
    "What computers are available?",
    "How many units of item TV-1234?"
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-900">Natural Language Query Parser</h1>
        <p className="mt-1 text-sm text-gray-600">
          Convert your natural language questions into SQL queries
        </p>
      </div>

      {/* Query Input Form */}
      <div className="bg-white shadow rounded-lg p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="query" className="block text-sm font-medium text-gray-700">
              Enter your question
            </label>
            <textarea
              id="query"
              name="query"
              rows={4}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="e.g., How many mobile phones do we have in stock?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="flex items-center">
            <input
              id="visualization"
              name="visualization"
              type="checkbox"
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              checked={includeVisualization}
              onChange={(e) => setIncludeVisualization(e.target.checked)}
            />
            <label htmlFor="visualization" className="ml-2 block text-sm text-gray-900">
              Include AST visualization
            </label>
          </div>

          <div className="flex justify-between items-center">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Parsing...
                </>
              ) : (
                '🧠 Parse Query'
              )}
            </button>

            <button
              type="button"
              onClick={() => {
                setQuery('')
                setResult(null)
              }}
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Clear
            </button>
          </div>
        </form>
      </div>

      {/* Example Queries */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Example Queries</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              onClick={() => setQuery(example)}
              className="text-left p-3 border border-gray-200 rounded-md hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <span className="text-sm text-gray-700">{example}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Query Results</h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-medium text-gray-700">Original Query:</h4>
              <p className="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">{result.original_query}</p>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-700">Generated SQL:</h4>
              {result.sql_queries.map((sql, index) => (
                <pre key={index} className="mt-1 text-sm text-gray-900 bg-gray-900 text-green-400 p-3 rounded overflow-x-auto">
                  {sql}
                </pre>
              ))}
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-700">Results:</h4>
              {result.results.map((sqlResult, index) => (
                <div key={index} className="mt-2">
                  {sqlResult.data && sqlResult.data.length > 0 ? (
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            {Object.keys(sqlResult.data[0]).map((key) => (
                              <th key={key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                {key}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {sqlResult.data.map((row, rowIndex) => (
                            <tr key={rowIndex}>
                              {Object.values(row).map((value, colIndex) => (
                                <td key={colIndex} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                  {value}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">No results found</p>
                  )}
                  <p className="mt-2 text-xs text-gray-500">
                    Found {sqlResult.count} result(s)
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default QueryParser

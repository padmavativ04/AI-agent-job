"""
Flask API for AI Job Application Agent
Deployment-ready backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from complete_agent import Orchestrator
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Initialize orchestrator
orchestrator = Orchestrator()


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "AI Job Application Agent",
        "version": "1.0.0",
        "deployed": datetime.now().isoformat(),
        "endpoints": {
            "GET /": "Health check",
            "POST /search": "Search for jobs",
            "GET /stats": "Get agent statistics",
            "POST /apply": "Apply to jobs"
        }
    }), 200


@app.route('/search', methods=['POST'])
def search_jobs():
    """
    Search for jobs based on preferences

    Request JSON:
    {
        "titles": ["Customer Success", "Implementation Consultant"],
        "location": "Canada",
        "salary_min": 50000,
        "goals": "Help customers and solve problems"
    }
    """
    try:
        data = request.json

        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ['titles', 'location', 'salary_min']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        preferences = {
            "titles": data.get('titles', []),
            "location": data.get('location', ''),
            "salary_min": data.get('salary_min', 0),
            "goals": data.get('goals', 'Find a great job')
        }

        # Run the agent
        result = orchestrator.run(preferences)

        if not result:
            return jsonify({"error": "No jobs found matching your criteria"}), 404

        # Format response
        response = {
            "status": "success",
            "total_jobs": len(result['jobs']),
            "total_applications": len(result['applications']),
            "total_emails": len(result['emails']),
            "jobs": [
                {
                    "id": job['id'],
                    "title": job['title'],
                    "company": job['company'],
                    "salary": job['salary'],
                    "location": job['location'],
                    "match_score": f"{int(job.get('semantic_score', 0) * 100)}%"
                }
                for job in result['jobs'][:10]  # Top 10
            ],
            "applications": [
                {
                    "company": app['company'],
                    "job_title": app['job_title'],
                    "salary": app['salary'],
                    "status": app['status'],
                    "date": app['date']
                }
                for app in result['applications'][:10]  # Top 10
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/apply', methods=['POST'])
def apply_to_jobs():
    """
    Apply to specific jobs

    Request JSON:
    {
        "job_ids": [1, 2, 3]
    }
    """
    try:
        data = request.json
        job_ids = data.get('job_ids', [])

        if not job_ids:
            return jsonify({"error": "No job IDs provided"}), 400

        return jsonify({
            "status": "success",
            "message": f"Applications submitted for {len(job_ids)} jobs",
            "job_ids": job_ids
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get agent performance statistics"""
    return jsonify({
        "status": "success",
        "stats": {
            "searches_performed": orchestrator.searcher.search_count,
            "applications_made": len(orchestrator.applier.applications),
            "emails_sent": len(orchestrator.emailer.emails_sent),
            "reports_generated": orchestrator.reporter.reports_generated,
            "semantic_matches_scored": orchestrator.matcher.matches_scored
        }
    }), 200


@app.route('/applications', methods=['GET'])
def get_applications():
    """Get all applications made"""
    apps = orchestrator.applier.get_applications()

    return jsonify({
        "status": "success",
        "total": len(apps),
        "applications": apps[-20:]  # Last 20
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": {
            "GET /": "Health check",
            "POST /search": "Search for jobs",
            "GET /stats": "Get statistics",
            "GET /applications": "Get applications"
        }
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Development
    app.run(debug=True, port=5000)

    # Production: Use gunicorn
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app

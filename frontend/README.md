# BodmasParser Frontend and API

This directory contains the frontend visualizer and API layer for the BodmasParser project.

## Features

- Input mathematical expressions via a text field
- Visualize parse trees using D3.js interactive visualization
- View postfix notation for expressions
- View evaluation results
- Error handling with detailed explanations
- Example expressions for quick testing
- Comprehensive API documentation

## Files

- `api.py`: FastAPI implementation that exposes the Parser functionality as REST endpoints
- `index.html`: Web interface for visualizing parse trees and evaluating expressions
- `styles.css`: Styling for the frontend interface
- `api-docs.html`: Detailed API documentation with examples
- `api_test.html`: Simple API connection test page

## Running the Application

### 1. Start Both Servers with One Command

From the project root directory, run:

```bash
./start_servers.sh
```

This will start both the API and frontend servers.

### 2. Or Start Each Server Individually

#### API Server:

```bash
source venv/bin/activate  # Activate virtual environment
python run_api.py
```

This will start the FastAPI server at http://localhost:8000

#### Frontend Server:

```bash
python serve_frontend.py
```

This will start a simple HTTP server at http://localhost:8080

### 3. Access the Visualizer

Open your web browser and navigate to:
http://localhost:8080

## API Endpoints

- `POST /parse`: Parse and evaluate a mathematical expression
  - Request body: `{"expression": "3+4*5"}`
  - Response: Contains postfix notation, parse tree, and evaluation result

- `GET /validate/{expression}`: Validate if an expression is well-formed
  - Response: `{"valid": true/false}`
  
- `GET /ping`: Simple health check endpoint
  - Response: `{"status": "ok", "message": "API is operational"}`

- `GET /`: Root endpoint with API information

## Documentation

API documentation is available at:
- http://localhost:8080/api-docs.html (Custom documentation with examples)
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Tree Visualization

The tree visualization uses D3.js to create an interactive representation of the parse tree:

- Operator nodes are shown in orange
- Operand nodes are shown in blue
- Hover over nodes to see details and highlight connections
- The tree layout adjusts automatically based on the expression complexity

## Error Handling

The visualization provides detailed error feedback for invalid expressions:

- Unbalanced parentheses
- Consecutive operators
- Invalid characters
- Invalid decimal numbers
- Division by zero
- And more

## Future Enhancements

- Support for more operators (%, sin, cos, etc.)
- Save/load expressions
- Mobile-friendly responsive design
- Animation of expression evaluation steps
- Customizable visualization options

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import json
import re
import dotenv
from typing import Dict, List, Union, Optional

# Add the parent directory to the Python path to import from the root directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Load environment variables from config.env
dotenv.load_dotenv(os.path.join(parent_dir, "config.env"))

from index import Parser
from operators import is_valid_expression, valid_parentheses

app = FastAPI(
    title="BodmasParser API",
    description="API for parsing and evaluating mathematical expressions",
    version="1.0.0"
)

# Get frontend URL from environment or use a safe default for development
frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:8080")
allowed_origins = [frontend_url]

# In debug mode, allow requests from any origin
if os.getenv("DEBUG", "").lower() in ("true", "1", "yes"):
    allowed_origins = ["*"]
    print(f"Running in debug mode - allowing all CORS origins")
else:
    print(f"CORS configured for: {allowed_origins}")

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow GET and POST
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]  # Expose all headers
)

class Expression(BaseModel):
    expression: str

class ParseResponse(BaseModel):
    postfix: List[str]
    parse_tree: Dict
    result: float
    input_expression: str
    valid: bool
    error: Optional[str] = None

@app.post("/parse", response_model=ParseResponse)
def parse_expression(req: Expression):
    """
    Parse and evaluate a mathematical expression
    """
    try:
        # Validate the expression first and provide specific error messages
        expression = req.expression.strip()
        
        # Check for empty expression
        if not expression:
            return ParseResponse(
                postfix=[],
                parse_tree={},
                result=0.0,
                input_expression=expression,
                valid=False,
                error="Expression cannot be empty"
            )
            
        # Check for valid characters
        if not re.match(r'^[0-9+\-*/^(). ]+$', expression):
            return ParseResponse(
                postfix=[],
                parse_tree={},
                result=0.0,
                input_expression=expression,
                valid=False,
                error="Invalid characters in expression. Only +, -, *, /, ^, decimal numbers and () are allowed."
            )
            
        # Check for consecutive operators
        if re.search(r'[+\-*/^]{2,}', expression):
            return ParseResponse(
                postfix=[],
                parse_tree={},
                result=0.0,
                input_expression=expression,
                valid=False,
                error="Invalid expression. Consecutive operators are not allowed."
            )
            
        # Check for balanced parentheses
        if not valid_parentheses(expression):
            return ParseResponse(
                postfix=[],
                parse_tree={},
                result=0.0,
                input_expression=expression,
                valid=False,
                error="Invalid expression. Parentheses are not balanced."
            )
            
        # Check for leading/trailing operators
        if re.match(r'^[+\-*/^]', expression) or re.search(r'[+\-*/^]$', expression):
            return ParseResponse(
                postfix=[],
                parse_tree={},
                result=0.0,
                input_expression=expression,
                valid=False,
                error="Invalid expression. Expression cannot start or end with an operator."
            )
            
        # Check for invalid decimal numbers
        tokens = re.sub(r'[+\-*/^()]', ' ', expression).split()
        for token in tokens:
            try:
                float(token)
            except ValueError:
                return ParseResponse(
                    postfix=[],
                    parse_tree={},
                    result=0.0,
                    input_expression=expression,
                    valid=False,
                    error=f"Invalid number in expression: {token}. Please use valid decimal numbers."
                )
        
        # If we got here, the expression is valid, so parse it
        parser = Parser(expression)
        
        # Get the parse tree as a dictionary
        parse_tree = json.loads(str(parser.parsetree))
        
        # Return the response
        return ParseResponse(
            postfix=parser.postfix,
            parse_tree=parse_tree,
            result=parser.evaluate(),
            input_expression=expression,
            valid=True,
            error=None
        )
    except ValueError as e:
        return ParseResponse(
            postfix=[],
            parse_tree={},
            result=0.0,
            input_expression=expression,
            valid=False,
            error=str(e)
        )
    except ZeroDivisionError:
        return ParseResponse(
            postfix=[],
            parse_tree={},
            result=0.0,
            input_expression=expression,
            valid=False,
            error="Division by zero"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/validate/{expression}")
def validate_expression(expression: str):
    """
    Validate a mathematical expression
    """
    try:
        is_valid = is_valid_expression(expression)
        return {"valid": is_valid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint - provides basic info about the API
    """
    return {
        "message": "Welcome to the BodmasParser API",
        "status": "operational",
        "documentation": "/docs",
        "endpoints": [
            {
                "path": "/parse",
                "method": "POST",
                "description": "Parse and evaluate a mathematical expression"
            },
            {
                "path": "/validate/{expression}",
                "method": "GET",
                "description": "Validate a mathematical expression"
            },
            {
                "path": "/ping",
                "method": "GET",
                "description": "Simple health check endpoint"
            }
        ]
    }

@app.get("/ping", tags=["Health"])
def ping():
    """
    Simple health check endpoint
    """
    return {"status": "ok", "message": "API is operational"}

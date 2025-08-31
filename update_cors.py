# This file will update the API's CORS settings during container startup
#!/usr/bin/env python3

import os
import sys

def update_cors_settings():
    """
    Updates the CORS settings in the frontend/api.py file to accept 
    requests from the same domain as well as the configured frontend URL
    """
    api_file = "/app/frontend/api.py"
    
    # Check if file exists
    if not os.path.exists(api_file):
        print(f"Error: {api_file} not found")
        return False
        
    with open(api_file, 'r') as file:
        content = file.read()
    
    # Find the CORS middleware section
    if "app.add_middleware(" in content and "CORSMiddleware" in content:
        # Replace the allow_origins line
        updated_content = content.replace(
            "allow_origins=[frontend_url]",
            "allow_origins=['*']"  # For testing, allow all origins
        )
        
        if updated_content == content:
            # Try another pattern that might be in the file
            updated_content = content.replace(
                "allow_origins=allowed_origins",
                "allow_origins=['*']"  # For testing, allow all origins
            )
        
        if updated_content == content:
            print("Warning: Could not update CORS settings in api.py")
            return False
            
        with open(api_file, 'w') as file:
            file.write(updated_content)
            
        print("Updated CORS settings in api.py to allow all origins")
        return True
    else:
        print("Warning: Could not find CORS middleware section in api.py")
        return False

if __name__ == "__main__":
    update_cors_settings()

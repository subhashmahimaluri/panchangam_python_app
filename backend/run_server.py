#!/usr/bin/env python3
"""
Run the Panchangam API server
"""
if __name__ == "__main__":
    import uvicorn
    
    print("Starting Panchangam API server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
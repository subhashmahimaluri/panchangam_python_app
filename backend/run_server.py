#!/usr/bin/env /opt/miniconda3/bin/python
"""
Run the Panchangam API server
"""
if __name__ == "__main__":
    import uvicorn
    
    print("Starting Panchangam API server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
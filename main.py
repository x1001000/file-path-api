import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

app = FastAPI(title="File Path Retriever")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/list-files", response_model=List[str])
async def list_files(
    directory: str = Query(..., description="Directory path to list files from"),
    recursive: bool = Query(False, description="Whether to list files recursively"),
    include_dirs: bool = Query(False, description="Include directories in the result"),
    file_types: Optional[List[str]] = Query(None, description="List of file extensions to filter (e.g., ['.txt', '.py'])")
):
    """
    Retrieve file paths under a specified directory.
    
    Parameters:
    - directory: Base directory to start listing files from
    - recursive: If True, lists files in subdirectories as well
    - include_dirs: If True, includes directory paths in the result
    - file_types: Optional list of file extensions to filter (e.g., ['.txt', '.py'])
    
    Returns:
    List of file paths
    """
    # Validate and normalize the directory path
    directory = os.path.abspath(os.path.expanduser(directory))
    
    # Check if directory exists
    if not os.path.isdir(directory):
        return []
    
    file_paths = []
    
    # Walk through directory
    if recursive:
        for root, dirs, files in os.walk(directory):
            # Handle directories if include_dirs is True
            if include_dirs:
                for dir_name in dirs:
                    full_dir_path = os.path.join(root, dir_name)
                    file_paths.append(full_dir_path)
            
            # Handle files
            for file in files:
                full_file_path = os.path.join(root, file)
                
                # Apply file type filtering if specified
                if file_types:
                    file_ext = os.path.splitext(file)[1]
                    if file_ext in file_types:
                        file_paths.append(full_file_path)
                else:
                    file_paths.append(full_file_path)
    else:
        # Non-recursive listing
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            
            # Handle directories if include_dirs is True
            if include_dirs and os.path.isdir(full_path):
                file_paths.append(full_path)
            
            # Handle files
            if os.path.isfile(full_path):
                # Apply file type filtering if specified
                if file_types:
                    file_ext = os.path.splitext(item)[1]
                    if file_ext in file_types:
                        file_paths.append(full_path)
                else:
                    file_paths.append(full_path)
    
    return file_paths

# Optional: Add a simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# To run the server:
# uvicorn main:app --reload

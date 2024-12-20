# File Path API

## Setup

1. Install required dependencies:
```bash
pip install fastapi uvicorn
```

2. Run the server:
```bash
uvicorn main:app --reload
```

## API Endpoints

### List Files

`GET /list-files`

Parameters:
- `directory` (required): The base directory to list files from
- `recursive` (optional, default=False): List files in subdirectories
- `include_dirs` (optional, default=False): Include directory paths in results
- `file_types` (optional): Filter files by extensions

#### Example Requests:

1. List all files in a directory:
```
/list-files?directory=/path/to/your/directory
```

2. Recursively list files:
```
/list-files?directory=/path/to/your/directory&recursive=true
```

3. List only Python files:
```
/list-files?directory=/path/to/your/directory&file_types=['.py']
```

4. Include directories in the result:
```
/list-files?directory=/path/to/your/directory&include_dirs=true
```

## Frontend Usage Example (JavaScript)

```javascript
async function listFiles(directory, options = {}) {
  const params = new URLSearchParams({
    directory,
    ...options
  });

  try {
    const response = await fetch(`http://localhost:8000/list-files?${params}`);
    const files = await response.json();
    console.log(files);
  } catch (error) {
    console.error('Error fetching files:', error);
  }
}

// Example usage
listFiles('/home/user/documents', { 
  recursive: true, 
  file_types: ['.txt', '.pdf'] 
});
```

## Notes
- Ensure proper security measures when exposing file system access
- The API uses CORS middleware to allow frontend requests
- Paths are absolute and normalized

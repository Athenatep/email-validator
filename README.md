# Email Validator Pro

A comprehensive email validation system with GUI interface and REST API support.

## Features

- **Email Validation**
  - Syntax validation
  - Domain verification
  - MX record checking
  - SMTP verification
  - Disposable email detection
  - Spam pattern detection
  - Typo detection
  - Duplicate detection

- **Batch Processing**
  - Support for CSV, Excel, and text files
  - Parallel processing
  - Progress tracking
  - Detailed reporting

- **Analytics & Reporting**
  - Validation statistics
  - Visual charts and graphs
  - PDF/HTML reports
  - Domain analysis

- **GUI Interface**
  - Modern Qt-based interface
  - Drag & drop support
  - Real-time validation
  - Progress monitoring

- **REST API**
  - FastAPI-based REST endpoints
  - Swagger documentation
  - Rate limiting
  - Caching support

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher (for development tools)
- Git (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd email-validator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```

4. Run the application:

- GUI Interface:
```bash
npm start
```

- REST API:
```bash
npm run api
```

### Development

- Run tests:
```bash
npm test
```

- Format code:
```bash
npm run format
```

- Lint code:
```bash
npm run lint
```

- Generate documentation:
```bash
npm run docs
```

## API Documentation

### Endpoints

- `POST /validate`: Single email validation
- `POST /validate/batch`: Batch validation
- `POST /report`: Generate reports
- `GET /cache/stats`: Cache statistics
- `POST /cache/clear`: Clear cache

### Example Request

```json
{
  "email": "test@example.com",
  "options": {
    "check_syntax": true,
    "check_domain": true,
    "check_spam": true
  }
}
```

### Example Response

```json
{
  "email": "test@example.com",
  "is_valid": true,
  "score": 95,
  "issues": [],
  "suggestions": []
}
```

## Configuration

All settings are configurable through `config/config.json`:
- Batch processing parameters
- Cache settings
- Validation options
- SMTP configurations
- Logging preferences

## Troubleshooting

1. **Installation Issues**
   - Ensure Python and Node.js are installed and in PATH
   - Check virtual environment activation
   - Verify all dependencies are installed

2. **GUI Issues**
   - Check Qt dependencies installation
   - Verify display server connection
   - Check system resources

3. **API Issues**
   - Verify port availability
   - Check network connectivity
   - Review API logs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
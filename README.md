# Meuze AI Content Creator

An AI-powered content creation tool built with Flask and OpenAI, supporting multiple languages.

## Features

- AI-powered content generation
- Multi-language support (English and Nederlands)
- Simple and intuitive web interface
- Customizable content templates
- Easy deployment
- Session-based language preference

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- OpenAI API key

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/dmeuze/Meuze-AI-Content-Creator.git
cd Meuze-AI-Content-Creator
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. Install the package and its dependencies:
```bash
# Install in development mode
pip install -e .

# Or install specific dependencies
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your OpenAI API key
# You can get an API key from: https://platform.openai.com/api-keys
```

5. Initialize the application:
```bash
# Set Flask environment variables
export FLASK_APP=tmz_content_creator
export FLASK_ENV=development
export FLASK_DEBUG=1

# On Windows, use:
# set FLASK_APP=tmz_content_creator
# set FLASK_ENV=development
# set FLASK_DEBUG=1
```

### Docker Installation (Alternative)

If you prefer using Docker:

1. Build the Docker image:
```bash
docker build -t meuze-ai-content-creator .
```

2. Run the container:
```bash
docker run -p 5000:5000 -e OPENAI_API_KEY=your_api_key meuze-ai-content-creator
```

## Usage

1. Start the development server:
```bash
flask run
```

2. Open your browser and navigate to `http://localhost:5000`

3. Using the application:
   - Select your preferred language (English or Dutch)
   - Enter your content prompt
   - Click "Generate Content"
   - View and use the generated content

## Features in Detail

### Language Support
- Switch between English and Dutch content generation
- Language preference is saved in your session
- System prompts optimized for each language
- Natural language processing in both languages

### Content Generation
- Professional tone and style
- Context-aware responses
- Format-preserving output
- Error handling and fallbacks
- Side-by-side content comparison
- Iterative improvement process with history tracking
- Loading states and progress indicators

### User Interface
- Clean and modern design
- Responsive layout for all devices
- Vertical content version comparison
- Interactive improvement history
- Real-time content updates
- Loading spinners and progress indicators
- Error handling with user feedback

## 🧠 Implementation Guide

Here's a simplified version of how the content generation system is implemented in Flask using OpenAI:

### 🧱 Step-by-step Flow

```python
# 1. Get original input from user
user_prompt = request.form["prompt"]

# 2. Run Prompt A — content generator
content_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an expert content creator on Topic A and Prompt Engineering."},
        {"role": "user", "content": f"Create a content piece based on: {user_prompt}"}
    ]
)

generated_content = content_response["choices"][0]["message"]["content"]

# 3. Run Prompt B — content reviewer
review_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an AI content reviewer. Check the content for clarity, tone, and completeness."},
        {"role": "user", "content": f"Review this content: {generated_content}. Give specific suggestions for improvement."}
    ]
)

suggestions = review_response["choices"][0]["message"]["content"]

# 4. Send review back to Prompt A — improve the original
improved_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful AI content editor."},
        {"role": "user", "content": f"Improve this content using the following feedback:\n\nOriginal:\n{generated_content}\n\nFeedback:\n{suggestions}"}
    ]
)

final_content = improved_response["choices"][0]["message"]["content"]
```

### 🧪 Key Features

- AI feedback loop that mimics human editing
- Multi-agent workflows inside a Flask API
- User choice between original and improved versions
- Improvement process tracking for analytics

### 🧰 Implementation Options

The system can be enhanced with:

- Modular prompt functions for better code organization
- Frontend toggle for version comparison
- Analytics dashboard for improvement tracking
- Custom prompt templates for different content types

## Development

To run tests:
```bash
pytest
```

To format code:
```bash
black .
```

To check code style:
```bash
flake8
```

## Project Structure

```
tmz_content_creator/
├── __init__.py
├── config/
│   └── config.py
├── routes/
│   └── main.py
├── services/
│   ├── __init__.py
│   ├── content_service.py
│   └── openai_service.py
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   └── index.html
└── tests/
    └── check_openai_connection.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
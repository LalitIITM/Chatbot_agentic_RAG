# 🌐 Frontend Guide - Agentic RAG Chatbot

This guide provides detailed information about the modern ChatGPT-like web frontend for the Agentic RAG Chatbot.

## 📸 Screenshots

### Initial View
![Initial View](https://github.com/user-attachments/assets/59139a56-aef4-4af1-8627-bcf82e6b5b3e)

The landing page features:
- Clean, dark-themed interface inspired by ChatGPT
- Gradient background with modern aesthetics
- Sidebar for navigation and controls
- Example prompts to get started quickly
- Centered welcome message

### Chat Conversation
![Chat Conversation](https://github.com/user-attachments/assets/5ff9fc34-4af9-42e8-80c6-1cbb65e88962)

The conversation view shows:
- Distinct message bubbles for user and assistant
- User messages with purple avatar badge
- Assistant messages with robot emoji and green badge
- Smooth scrolling to latest messages
- Clean, readable typography

## 🎨 Features

### Design
- **Modern Dark Theme**: Elegant dark color scheme with gradient accents
- **ChatGPT-Inspired UI**: Familiar interface for users of modern AI chatbots
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Smooth Animations**: Loading indicators and transitions for better UX

### Functionality
- **Real-time Chat**: Instant message sending and receiving
- **Conversation Management**: Reset chat to start fresh conversations
- **Example Prompts**: Quick-start buttons with common questions
- **Auto-scroll**: Automatically scrolls to show latest messages
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback while waiting for responses

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- All dependencies from `requirements.txt`

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   
   Create a `.env` file in the root directory:
   ```env
   # Required
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your-random-secret-key-here
   
   # Optional
   OPENAI_MODEL=gpt-3.5-turbo
   EMBEDDING_MODEL=text-embedding-ada-002
   PORT=5000
   FLASK_HOST=127.0.0.1
   FLASK_DEBUG=False
   ```
   
   **Security Note**: Generate a strong random SECRET_KEY. You can use Python:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Add documents** (optional):
   
   Place your `.txt` documents in the `data/documents/` directory. The system comes with sample documents about RAG, Python, and AI basics.

### Running the Application

Start the web server:
```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

Open your web browser and navigate to:
```
http://localhost:5000
```

### Configuration

You can customize the server using environment variables in your `.env` file:

```env
# Required
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your-random-secret-key-here

# Optional
PORT=5000                                    # Server port (default: 5000)
FLASK_HOST=127.0.0.1                        # Server host (default: 127.0.0.1 for security)
FLASK_DEBUG=False                           # Debug mode (default: False)
OPENAI_MODEL=gpt-3.5-turbo                 # Or gpt-4 for better results
EMBEDDING_MODEL=text-embedding-ada-002      # Embedding model
```

**Important Configuration Notes:**
- `FLASK_HOST=127.0.0.1` - Binds to localhost only for security. Use `0.0.0.0` to accept connections from any network interface (only in trusted networks)
- `SECRET_KEY` - Required for Flask session security. Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

## 🎯 Using the Frontend

### Starting a Conversation

1. **Use Example Prompts**: Click any of the example prompt cards to quickly ask a question
2. **Type Your Message**: Click the input field at the bottom and type your question
3. **Send**: Press Enter or click the ↑ button to send your message

### Managing Conversations

- **New Chat**: Click the "+ New Chat" button in the sidebar to clear conversation history and start fresh
- **Scroll**: The chat automatically scrolls to show new messages

### Understanding the Interface

#### Sidebar (Left Panel)
- **New Chat Button**: Clears conversation and starts fresh
- **Footer**: Shows chatbot branding

#### Main Chat Area
- **Header**: Shows the chatbot name
- **Messages Container**: Displays the conversation history
  - User messages: Purple avatar with "U"
  - Assistant messages: Green avatar with robot emoji 🤖
- **Input Area**: Fixed at bottom with text input and send button

#### Message States
- **Typing**: Shows animated dots while assistant is thinking
- **Error**: Displays red error banner at top if something goes wrong
- **Empty**: Shows welcome message and example prompts when no messages

## 🏗️ Technical Architecture

### Backend (Flask)
- **app.py**: Main Flask application
  - Serves the web interface
  - Handles API endpoints
  - Manages chatbot initialization

### Frontend (HTML/CSS/JS)
- **templates/index.html**: Single-page application
  - Embedded CSS for styling
  - Embedded JavaScript for interactivity
  - No external dependencies (vanilla JS)

### API Endpoints

#### GET /
- Returns the main HTML interface

#### POST /api/chat
- Handles chat messages
- **Request Body**:
  ```json
  {
    "message": "Your question here"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "response": "Assistant's response"
  }
  ```

#### POST /api/reset
- Clears conversation history
- **Response**:
  ```json
  {
    "success": true,
    "message": "Conversation history cleared"
  }
  ```

#### GET /api/health
- Health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy",
    "chatbot_initialized": true
  }
  ```

## 🎨 Customization

### Changing Colors

Edit the CSS in `templates/index.html`:

```css
/* Primary background */
background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);

/* Accent color (send button, etc.) */
background: #10a37f;

/* Message backgrounds */
.message.user { background: #343541; }
.message.assistant { background: #444654; }
```

### Modifying Example Prompts

Edit the example prompts in `templates/index.html`:

```html
<div class="example-prompt" onclick="sendExamplePrompt('Your question')">
    <div class="example-prompt-title">📚 Your Title</div>
    <div class="example-prompt-text">Your question text</div>
</div>
```

### Changing Port

Set the PORT environment variable:
```bash
PORT=8080 python app.py
```

Or in your `.env` file:
```env
PORT=8080
```

## 🔧 Troubleshooting

### Server Won't Start

**Issue**: Port already in use
```
Address already in use. Port 5000 is in use by another program.
```

**Solution**: Change the port or stop the other service
```bash
PORT=8080 python app.py
```

### No API Key Error

**Issue**: Missing OpenAI API key
```
OPENAI_API_KEY not found in environment variables
```

**Solution**: Create a `.env` file with your API key
```env
OPENAI_API_KEY=sk-...your-key-here
```

### Documents Not Loading

**Issue**: No documents in knowledge base

**Solution**: Add `.txt` files to `data/documents/` directory

### Chat Not Responding

**Issue**: Network errors or server issues

**Solution**: 
1. Check server logs for errors
2. Verify your OpenAI API key is valid
3. Check your internet connection
4. Ensure you have sufficient OpenAI API credits

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

1. **Set production environment variables**:
   ```env
   FLASK_DEBUG=False
   SECRET_KEY=your-secure-secret-key-here
   ```

2. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Deploy to cloud platforms**:
   - **Heroku**: Use `Procfile` with `web: gunicorn app:app`
   - **AWS/GCP/Azure**: Use container services or VM instances
   - **Vercel/Netlify**: These are for static sites; use a Python-friendly platform instead

### Security Considerations

- Always use HTTPS in production
- Set a strong SECRET_KEY in production
- Rate limit API endpoints to prevent abuse
- Keep your OpenAI API key secure and never commit it to version control
- Consider implementing user authentication for production use

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 🤝 Contributing

Feel free to contribute improvements to the frontend:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

# AI-Powered Technical Interview Simulator

A comprehensive platform for data engineering candidates to practice technical interviews with an AI interviewer. The simulator provides realistic interview experiences with SQL and Python coding challenges, similar to those used by top tech companies like Meta, Amazon, and Uber.

## Features

- **AI-Powered Interviewer**: Realistic conversational AI that conducts technical interviews
- **SQL & Python Challenges**: Practice with real-world data engineering problems
- **Adaptive Difficulty**: Questions adjust based on your experience level
- **Code Execution**: Run and test your code in a sandboxed environment
- **Detailed Feedback**: Get comprehensive feedback on your solutions
- **Company-Specific Prep**: Focus on interview styles of top tech companies

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/potureddigowtham/mock_interviewer.git
   cd mock_interviewer
   ```

2. Install dependencies:
   ```bash
   # Install backend dependencies
   cd server
   pip install -r requirements.txt
   
   # Install frontend dependencies
   cd ../client
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update the .env file with your configuration
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd server
   python app.py
   ```

2. Start the frontend development server:
   ```bash
   cd client
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
mock_interviewer/
├── client/                 # Frontend React application
├── server/                 # Backend Python/Flask server
├── ai/                     # AI interviewer logic and models
├── scripts/                # Utility scripts
├── tests/                  # Test files
├── .gitignore
├── README.md
└── package.json
```

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by real technical interview processes at top tech companies
- Built with modern web technologies and AI/ML capabilities

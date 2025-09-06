# Job Application Email Sender 📧

A professional AI-powered Streamlit application that automatically generates personalized job application emails and sends them to multiple recruiters simultaneously. The application uses OpenAI's GPT models to create tailored email content and SendGrid for reliable email delivery.
#### Special thanks to Ed Donner for The Complete Agentic AI Course(2025)👏🏻.

- ## Click Here to visit the Streamlit app(https://agenticai-recruiter-cold-email-sender.streamlit.app/)

## 🌟 Features

- **Multi-Style Email Generation**: Three distinct writing styles (Professional, Engaging, Concise)
- **Automated Email Sending**: Send personalized emails to multiple recruiters at once
- **Professional UI**: Beautiful gradient-based interface with animated backgrounds
- **Resume Attachment**: Automatic PDF resume attachment to all emails
- **Real-time Preview**: View generated email content before sending
- **Send Logs**: Track email delivery status and details
- **HTML Email Format**: Professional HTML formatting with clickable LinkedIn links


## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **AI Models**: OpenAI GPT-4o-mini for content generation
- **Email Service**: SendGrid API for email delivery
- **File Handling**: Base64 encoding for resume attachments
- **Async Processing**: Concurrent email generation and sending


## 📋 Prerequisites

Before running the application, ensure you have these:

1. **Python 3.8+** installed
2. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
3. **SendGrid API Key** - Get from [SendGrid Console](https://app.sendgrid.com/settings/api_keys)
4. **Required Python packages** (see Installation section)

## 🚀 Installation

1. **Clone or download the project files**

```bash
# Ensure you have the main script file in your working directory
```

2. **Install required dependencies**

```bash
pip install streamlit sendgrid python-dotenv openai
```

3. **Install the agents library** (if not already available)

```bash
pip install agents  # Or install from your specific source
```

4. **Create environment file** (optional)

```bash
# Create a .env file in your project directory
touch .env
```


## ⚙️ Configuration

### API Keys Setup

The application requires two API keys that you'll enter in the sidebar:

1. **OpenAI API Key**:
    - Sign up at [OpenAI Platform](https://platform.openai.com/)
    - Navigate to API Keys section
    - Create a new secret key
    - Copy and paste into the sidebar
2. **SendGrid API Key**:
    - Sign up at [SendGrid](https://sendgrid.com/)
    - Go to Settings > API Keys
    - Create a new API key with Mail Send permissions
    - Copy and paste into the sidebar

### Environment Variables (Optional)

You can also set these in a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
```


## 🏃‍♂️ Running the Application

1. **Start the Streamlit server**:

```bash
streamlit run your_script_name.py
```

2. **Access the application**:
    - Open your browser and go to `http://localhost:8501`
    - The application will automatically open if configured

## 📖 How to Use

### Step 1: Configure API Keys

- Enter your OpenAI API Key in the sidebar
- Enter your SendGrid API Key in the sidebar
- Wait for the "✅ Configuration Complete!" message


### Step 2: Fill Applicant Information

- **Full Name**: Your complete name
- **Email Address**: Your sending email address
- **Phone Number**: Your contact number
- **LinkedIn Profile**: Full LinkedIn URL
- **Target Role**: Position you're applying for
- **Company Name**: Target company
- **Additional Notes**: Any extra information


### Step 3: Add Recruiter Details

- **Recruiter Names**: Comma-separated list (e.g., "John Smith, Sarah Johnson")
- **Recruiter Emails**: Comma-separated list (e.g., "john@company.com, sarah@company.com")
- **Important**: Names and emails must be in the same order


### Step 4: Upload Resume

- Click "Upload Resume (PDF)"
- Select your PDF resume file
- Wait for confirmation message


### Step 5: Generate and Send

- Click "🚀 Generate \& Send Emails"
- Wait for draft generation (progress bar will show status)
- Emails are automatically sent after generation
- Review the preview and send logs


## 🔧 Application Architecture

### AI Agents System

The application uses a multi-agent architecture:

1. **Applicant Agents (3 styles)**:
    - Professional Applicant: Formal, serious tone
    - Engaging Applicant: Friendly, witty tone
    - Concise Applicant: Short, to-the-point
2. **Content Processing Agents**:
    - Subject Writer: Creates compelling email subjects
    - HTML Converter: Formats content into professional HTML
3. **Management Agents**:
    - Application Manager: Generates drafts using applicant agents
    - Email Manager: Handles subject creation, HTML formatting, and sending

### Processing Flow

```
User Input → Application Manager → Applicant Agents → Draft Generation
    ↓
Draft Content → Subject Writer → Email Subject
    ↓
Draft Content → HTML Converter → HTML Format
    ↓
HTML Email + Subject + Resume → SendGrid → Email Delivery
```


### Concurrent Processing

- **Draft Generation**: All recruiter emails generated simultaneously
- **Email Sending**: Parallel processing for faster delivery
- **Progress Tracking**: Real-time updates during processing


## 🎨 UI Features

### Professional Design

- **Gradient Backgrounds**: Animated color transitions
- **Responsive Layout**: Works on desktop and mobile
- **Custom Styling**: Professional color scheme and typography
- **Interactive Elements**: Hover effects and smooth transitions


### User Experience

- **Real-time Feedback**: Progress bars and status messages
- **Error Handling**: Clear error messages and validation
- **Preview System**: See content before sending
- **Download Options**: Save drafts as text files


## 📊 Email Templates

The system generates emails with the following structure:

```
Subject: [AI-generated compelling subject line]

Dear [Recruiter Name],

[Personalized introduction paragraph]

[Professional background and qualifications]

[Role-specific interest and company research]

[Contact information and next steps]

Best regards,
[Your Name]
[Your Phone]
[Your LinkedIn Profile - clickable link]
```


## 🔍 Troubleshooting

### Common Issues

1. **"Configuration Required" Message**:
    - Ensure both API keys are entered in the sidebar
    - Check that keys are valid and have proper permissions
2. **"Number of names and emails must match"**:
    - Verify that recruiter names and emails lists have the same count
    - Check for extra commas or spaces
3. **Email Sending Failures**:
    - Verify SendGrid API key has Mail Send permissions
    - Check that sender email is verified in SendGrid
    - Ensure recipient emails are valid
4. **Draft Generation Errors**:
    - Check OpenAI API key validity
    - Ensure sufficient API credits
    - Verify all required fields are filled

### Performance Tips

- **Batch Size**: For large recruiter lists (>20), consider running in smaller batches
- **API Limits**: Monitor OpenAI API usage to avoid rate limits
- **Email Limits**: Check SendGrid daily sending limits


## 📁 File Structure

```
project/
│
├── your_script_name.py    # Main application file
├── .env                   # Environment variables (optional)
├── requirements.txt       # Dependencies (create if needed)
└── README.md             # This file
```


### Dependencies List

Create a `requirements.txt` file:

```txt
streamlit>=1.28.0
sendgrid>=6.10.0
python-dotenv>=1.0.0
openai>=1.0.0
agents>=0.1.0
asyncio
base64
io
os
typing
```


## 🚨 Security Considerations

- **API Keys**: Never commit API keys to version control
- **Email Validation**: Application validates email formats
- **Rate Limiting**: Built-in async handling prevents API overload
- **Data Handling**: No user data is stored permanently


## 📈 Future Enhancements

Potential improvements for future versions:

- **Database Integration**: Store sent emails and responses
- **Template Customization**: User-defined email templates
- **Analytics Dashboard**: Track email open rates and responses
- **Scheduled Sending**: Queue emails for specific times
- **Integration Options**: Connect with job boards and CRM systems


## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:

- Check the Troubleshooting section
- Review API documentation (OpenAI, SendGrid)
- Ensure all dependencies are properly installed
- Verify API keys and permissions


## 📄 License

This project is provided as-is for educational and personal use. Please review the terms of service for OpenAI and SendGrid APIs when using this application.

***

**Built with ❤️ using Streamlit and OpenAI -  Powered by SendGrid**


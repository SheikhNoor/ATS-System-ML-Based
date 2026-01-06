# Frontend - ATS Resume Optimization System

## Overview
This is the Next.js frontend for the ATS Resume Optimization System. It provides a modern, responsive interface for resume analysis.

## Features
- **Drag-and-Drop Upload**: Easy file upload with visual feedback
- **Real-time Validation**: Instant validation for files and inputs
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Modern UI**: Built with Tailwind CSS for a clean, professional look
- **Interactive Results**: Visual score breakdown with color-coded keywords

## Tech Stack
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **Language**: JavaScript (React)

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm (or yarn)
- Backend API running on port 8000

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```
   or
   ```bash
   yarn install
   ```

2. **Set up environment variables**:
   ```bash
   copy .env.example .env.local
   ```
   Edit `.env.local` and update the API URL if needed:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Running the Application

Start the development server:
```bash
npm run dev
```
or
```bash
yarn dev
```

The application will be available at: http://localhost:3000

## Project Structure

```
frontend/
├── components/
│   └── Dashboard.js        # Main dashboard component
├── pages/
│   ├── _app.js            # App wrapper
│   ├── _document.js       # HTML document
│   └── index.js           # Home page
├── styles/
│   └── globals.css        # Global styles
├── public/                # Static assets
├── package.json           # Dependencies
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind configuration
├── postcss.config.js      # PostCSS configuration
└── README.md             # This file
```

## Building for Production

### Build the application:
```bash
npm run build
```

### Start the production server:
```bash
npm start
```

## Usage Guide

1. **Upload Resume**: Drag and drop your resume (PDF/DOCX) or click to browse
2. **Enter Job Description**: Paste the job description in the text area
3. **Select Category**: Choose IT or Non-IT category
4. **Analyze**: Click the "Analyze Resume" button
5. **Review Results**: Check your ATS score, matched/missing keywords, and recommendations

## Customization

### Changing Colors
Edit [tailwind.config.js](tailwind.config.js) to customize the color scheme:
```javascript
theme: {
  extend: {
    colors: {
      primary: { ... }
    }
  }
}
```

### Modifying API Endpoint
Update the `.env.local` file:
```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

## Troubleshooting

### Common Issues

1. **API Connection Error**:
   - Ensure backend is running on port 8000
   - Check CORS settings in backend
   - Verify `NEXT_PUBLIC_API_URL` in `.env.local`

2. **Styling Issues**:
   - Clear `.next` folder: `rm -rf .next`
   - Reinstall dependencies: `npm install`
   - Restart dev server

3. **File Upload Fails**:
   - Check file size (max 10MB)
   - Ensure file format is PDF or DOCX
   - Verify backend is accepting requests

## Deployment

### Vercel (Recommended)
1. Push code to GitHub
2. Import project in Vercel
3. Add environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy

### Other Platforms
Build the static version:
```bash
npm run build
npm start
```

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing
Feel free to submit issues and enhancement requests!

## License
MIT License

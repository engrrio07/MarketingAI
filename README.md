# MarketingAI

MarketingAI is an advanced AI-powered marketing assistant that helps businesses generate content, schedule social media posts, and analyze content performance. It leverages artificial intelligence to streamline marketing tasks and provide valuable insights.

## Features

- **AI-Powered Content Generation**: Create high-quality, engaging content using advanced AI models.
- **Social Media Post Scheduling**: Plan and schedule posts across various social media platforms.
- **Content Analytics**: Track and visualize the performance of your content with detailed metrics and insights.
- **User Authentication**: Secure user accounts with login and registration functionality.
- **Automated Analytics Updates**: Periodic updates of content performance metrics.

## Technologies Used

- Backend: FastAPI
- Frontend: Streamlit
- Database: PostgreSQL
- AI/ML: CrewAI, OpenAI
- Data Visualization: Plotly, Matplotlib

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables:
Create a `.env` file in the root directory and add the following:
```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```
4. Start the database: `docker-compose up -d`

## Running the Application

1. Start the FastAPI backend: `uvicorn app.main:app --reload`

2. In a new terminal, start the Streamlit frontend: `streamlit run frontend/app.py`

3. Open a web browser and navigate to `http://localhost:8501` to access the MarketingAI application.

## Usage

1. Register for a new account or log in if you already have one.
2. Use the "Generate Content" tab to create new marketing content.
3. Schedule social media posts using the "Schedule Social Media Posts" tab.
4. View and analyze content performance in the "Content Analytics" dashboard.

## Contributing

Contributions to MarketingAI are welcome! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or support, please contact [your-email@example.com](mailto:your-email@example.com).
# LinkedIn Job Scraper Flask App

This is a Flask web application that scrapes job listings from LinkedIn using Beautiful Soup and provides the scraped data in a CSV format. It allows you to extract job information such as job title, company, description, location, criteria, and more.

## Features

- Scrapes job listings from LinkedIn job search pages for multiple countries.
- Extracts job details like title, company, description, criteria, location, and more.
- Provides data in CSV format for easy analysis and storage.
- Handles pagination to scrape multiple pages of job listings.
- Built using Python, Flask, Beautiful Soup, and requests libraries.

## Getting Started
1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/linkedin-job-scraper.git

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt

3. Run the Flask app:
   ```sh
   python app.py

4. Open your web browser and navigate to http://127.0.0.1:5000 to access the app.

## Usage
At this time, visiting the main page i.e (navigating to http://127.0.0.1:5000) will trigger the scrapping and you can see the progress in terminal.

## Configuration
You can modify the 'links' dictionary in 'app.py' to add or customize LinkedIn job search URLs for different countries, work types, and search preferences.

## Future work
The main page of the app will provide options to scrape job listings for different countries and work types (onsite, remote, hybrid).
Allow users to select a country and work type, then click the "Scrape Jobs" button.
The app will start scraping job listings from LinkedIn and display progress.
Once the scraping is complete, a CSV file will be generated containing the scraped data. The CSV file will be saved in the 'datasets' directory.

**contibutions are welcome**

## Contributing
Thank you for considering contributing to the LinkedIn Job Scraper Flask App! Whether you're reporting a bug, proposing new features, or making improvements, your contributions are valuable to the community.

### How to Contribute
1. Fork the repository to your GitHub account.

2. Clone the forked repository to your local machine:

   ```sh
   git clone https://github.com/your-username/linkedin-job-scraper.git

3. Create a new branch for your changes:

   ```sh
   git checkout -b feature/new-feature

4. Make your changes and test the app to ensure everything is working as expected. Commit your changes:

   ```sh
   git commit -m "Add new feature"

5. Push your changes to your forked repository:

   ```sh
   git push origin feature/new-feature

6. Create a pull request from your forked repository to the original repository.

7. Describe your changes and why they should be merged. Provide any relevant context.

8. Once your pull request is submitted, maintainers will review your changes and provide feedback.

## Code of Conduct
Please note that this project follows the Code of Conduct. By participating, you are expected to uphold this code of conduct.

## Issues and Bugs
If you encounter any issues, have questions, or want to discuss improvements, feel free to create an issue. Be sure to provide as much detail as possible.

## Contact
If you have any questions or need further assistance, you can contact the project maintainers via email [mailto:victorjohnukam@gmail.com] or social media.

## Notes
* This app is for exploratory and research purposes only. Always follow LinkedIn's terms of use and be respectful of the website's policies when scraping.
* Web scraping can be fragile and may break if the website's structure changes.

## License
This project is licensed under the MIT License.
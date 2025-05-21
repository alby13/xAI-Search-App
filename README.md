# xAI Live Search App
xAI Search App built in Python with GUI to interact with the xAI Live Search API. This tool allows you to easily test and utilize the Live Search feature, which is currently in a free beta period until June 5, 2025.


<img src="https://github.com/alby13/xAI-Search-App/blob/main/screenshot.jpg">


## Features

*   **Interactive Interface:** Easy-to-use GUI for constructing and sending API requests.
*   **API Key Management:** Input your xAI API key (recommend using a new key for the beta).
*   **Prompt Input:** Multi-line text area for your search queries.
*   **Model Selection:** Specify the xAI model to use (e.g., `grok-3-latest`).
*   **Search Mode Control:** Select between `"auto"`, `"on"`, or `"off"` for search preference.
*   **Citation Retrieval:** Option to request and display source citations.
*   **Date Range Filtering:** Specify `from_date` and `to_date` for time-bound searches.
*   **Result Count Limit:** Set `max_search_results` to control the number of sources considered.
*   **Detailed Source Configuration:**
    *   Enable/disable **Web**, **X (Twitter)**, **News**, and **RSS** sources.
    *   **Web & News:**
        *   Specify `country` for region-specific results.
        *   List `excluded_websites`.
        *   Toggle `safe_search`.
    *   **X (Twitter):**
        *   Specify target `x_handles`.
    *   **RSS:**
        *   Provide `links` to RSS feeds (currently supports one link as per xAI docs).
*   **Response Display:** View the full JSON API response.
*   **Clear Citation Display:** Extracted citations are shown separately for easy review.
*   **Non-Blocking API Calls:** GUI remains responsive during API requests.

## Prerequisites

*   Python 3.6+
*   `tkinter` (usually included with Python standard library)
*   `requests` library

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Install dependencies:**
    ```bash
    pip install requests
    ```
    (If you are using a virtual environment, activate it first.)

## How to Use

1.  **Set your API Key:**
    *   **Recommended:** Create a new API key from your xAI account specifically for Live Search beta testing.
    *   You can set it as an environment variable:
        ```bash
        export XAI_API_KEY="your_new_xai_api_key_here"
        ```
        The application will attempt to read this variable on startup.
    *   Alternatively, you can paste your API key directly into the "xAI API Key" field in the GUI.

2.  **Run the application:**
    ```bash
    python xai_search_gui.py
    ```

3.  **Fill in the GUI fields:**
    *   **Prompt:** Enter your search query or instruction.
    *   **Model:** Ensure the correct model (e.g., `grok-3-latest`) is specified.
    *   **Search Parameters:**
        *   Choose the `Mode` (`auto`, `on`, `off`).
        *   Check `Return Citations` if desired.
        *   Optionally, fill in `From Date`, `To Date` (YYYY-MM-DD format), and `Max Search Results`.
    *   **Data Sources:**
        *   Check the boxes for the data sources you wish to use (`Web`, `X`, `News`, `RSS`).
        *   Fill in the specific parameters for each selected source (e.g., country codes, excluded websites, X handles, RSS links).
        *   If no sources are explicitly checked and search mode is `auto` or `on`, the API will default to "web" and "x".

4.  **Send Request:** Click the "Send Request" button.

5.  **View Response:**
    *   The status label will indicate "Sending request..." and then "Response received." or an error message.
    *   The full JSON response from the API will be displayed in the right-hand text area.
    *   If citations were requested and returned, they will be listed below the JSON response.

## Important Notes

*   **Beta Program:** The xAI Live Search feature is in beta and free to use until **June 5, 2025**.
*   **Data Sharing:** By using Live Search during this beta, you consent to sharing your request data with xAI for service improvement.
*   **API Key Security:** Always keep your API keys confidential. Using a dedicated key for this beta is highly recommended.
*   **Content Liability:** xAI is not liable for any damages or liabilities resulting from the content accessed via Live Search.
*   **RSS Feed:** The xAI documentation currently states support for one RSS link in the `links` parameter for the RSS source, even though the parameter name is plural.


## License

Distributed under the MIT License.

---

This GUI was created to help users explore and take advantage of the xAI Live Search beta program.

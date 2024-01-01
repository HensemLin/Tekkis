# Tekkis

## Overview

This project is designed to scrape car details from [Mudah](https://www.mudah.my/malaysia/cars-for-sale), store the information in a MySQL database, and expose the data through a FastAPI-based API. Additionally, it provides visualization capabilities using Streamlit for understanding the distribution of car prices and the relationship between car age and mileage.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#Prerequisites)
  - [Installation](#Installation)
- [Usage](#Usage)
  - [FastAPI API](#FastAPI-API)
  - [Streamlit Visualization](#Streamlit-Visualization)
- [API Endpoints](#API-Endpoints)
- [Configuration](#Configuration)
- [Contributing](#Contributing)
- [License](#License)

## Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:

- Python (3.7 or later)
- MySQL Server
- pip (Python package installer)

### Installation

1. Clone the repository:
   <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">git clone https://github.com/HensemLin/Tekkis.git
   </code></div></div></pre>
2. Navigate to the project directory:
   <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">cd your-repository
   </code></div></div></pre>
3. Install dependencies:
   <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">pip install -r requirements.txt
   </code></div></div></pre>

## Usage

### FastAPI API

1. Set up your MySQL database and configure connection details in `.env` as shown in the `.env.example`.
2. Run the FastAPI application:

   <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">uvicorn app.main:app --reload
   </code></div></div></pre>

   FastAPI will start serving the API at `http://127.0.0.1:8000`.

3. When the application is started, it will run the web scrap function to scrap up to 50 cars from [Mudah](https://www.mudah.my/malaysia/cars-for-sale) and save them in the database.

### Streamlit Visualization

1. Ensure FastAPI is running.
2. Run the [API Endpoints](#API-Endpoints) below to create an API and configure in `.env` as shown in the `.env.example`.
3. Run the Streamlit app in a different terminal:

   <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">streamlit run streamlit.py
   </code></div></div></pre>

   Open your browser and navigate to `http://localhost:8501`.

## API Endpoints

### Car Details

- **GET /car/**
  - Retrieve a list of car details (limited to 50 by default).
  - Requires API key.
- **GET /car/{id}**
  - Retrieve details for a specific car by ID.
  - Requires API key.

### API Key Management

- **GET /API/**
  - Retrieve a list of existing API keys.
- **GET /API/{id}**
  - Retrieve details for a specific API key by ID.
- **GET /API/createAPI/**
  - Create a new API key.
  - Returns the new API key.
  - Requires API key.
- **DELETE /API/{id}**
  - Delete an existing API key by ID.
  - Requires API key.

## Configuration

- MySQL database connection details can be configured in `.env` example shown in `.env.example`.
- API key can be configure in `.env` example shown in `.env.example`.
- Maximum number of cars to scrape can be modified in `main.py` in the `initialize_table_data()` function.

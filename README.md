# surfSramFlask

A minimal Flask web application demonstrating authentication with SURF's SRAM (SURF Research Access Management) system.

## 📦 Project Structure
```
surfSramFlask/ 
├── application/ # Main Flask app (views, templates, etc.) 
├── config/ # Configuration files for different environments 
├── auth_tools.py # Authentication utilities 
├── config.py # Main configuration logic 
├── conda_env.yaml # Conda environment definition 
├── run_application.py # Entry point to run the Flask app 
├── .gitignore 
├── LICENSE # MIT License
```

## 🚀 Getting Started

### Prerequisites

- [Anaconda or Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Python 3.8+

### Installation

1. Clone the repository:

```bash
git clone https://github.com/kuytje/surfSramFlask.git
cd surfSramFlask

python run_application.py
```

2. Create and activate the Conda environment:

```bash
conda env create -f conda_env.yaml
conda activate surf_sram_env
```

3. Set environment variables (if needed), then run the application:

```bash
python run_application.py
```

# 🔐 SRAM Authentication
This app includes support for authentication using SURF's SRAM, allowing users to log in via federated identity providers. Edit auth_tools.py and relevant config/ files to adapt the authentication flow to your institution's needs.

# 🛠 Configuration
Use the config/ directory to manage different environment settings (e.g., development, production). The config.py file loads these settings based on environment variables.

# 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

# 📬 Contact

For questions or suggestions, feel free to open an issue or contact the author at e.kuijt@nioo.knaw.nl.
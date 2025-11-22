# Bandit-Based Advertisement Selection API

**Ad‑Personalization Service Template** implementing multi-armed bandit algorithms for personalized advertisement selection. Uses Thompson Sampling with Beta-Bernoulli bandits to optimize ad performance through exploration-exploitation balance.

## 🎯 Features

- **Thompson Sampling Algorithm**: Bayesian approach for optimal ad selection
- **Persona-Based Targeting**: Associate different ads with user personas
- **Real-time Learning**: Updates performance based on user interactions
- **RESTful API**: Clean, well-documented endpoints
- **Type Safety**: Full Pydantic validation
- **Docker Support**: Containerized deployment ready

## 🏗️ Architecture

```
┌─────────────────┐
│   FastAPI App   │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Factory  │ (Strategy Pattern)
    └────┬─────┘
         │
    ┌────▼──────────────────┐
    │ Thompson Sampling     │
    │ Strategy              │
    │ - Beta Distribution   │
    │ - Exploration/Exploit │
    └───────────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Bandit-persona-prompt
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python ad_select_main.py
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - OpenAPI Schema: http://localhost:8000/openapi.json

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t ad-selection-api .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 8000:8000 --name ad-selection ad-selection-api
   ```

3. **View logs**
   ```bash
   docker logs -f ad-selection
   ```

## 📡 API Endpoints

### 1. Register Persona Ads
Associate advertisements with a user persona.

```bash
curl -X 'POST' \
  'http://localhost:8000/register_persona_ads' \
  -H 'Content-Type: application/json' \
  -d '{
  "persona_id": "persona_01",
  "ad_ids": ["Ad_1", "Ad_2", "Ad_3"]
}'
```

**Response:**
```json
{
  "message": "Persona ads registered successfully",
  "persona_id": "persona_01",
  "ad_count": 3
}
```

### 2. Select Ad
Get the optimal advertisement for a persona using Thompson Sampling.

```bash
curl -X 'POST' \
  'http://localhost:8000/select_ad' \
  -H 'Content-Type: application/json' \
  -d '{
  "persona_id": "persona_01"
}'
```

**Response:**
```json
{
  "ad_id": "Ad_2",
  "persona_id": "persona_01"
}
```

### 3. Update Reward
Provide feedback on ad performance after user interaction.

```bash
curl -X 'POST' \
  'http://localhost:8000/update' \
  -H 'Content-Type: application/json' \
  -d '{
  "ad_id": "Ad_2",
  "reward": {
    "success": 1,
    "failure": 0
  }
}'
```

**Response:**
```json
{
  "message": "Reward updated successfully",
  "ad_id": "Ad_2"
}
```

## 🧪 Example Workflow

```bash
# 1. Register ads for a persona
curl -X POST http://localhost:8000/register_persona_ads \
  -H 'Content-Type: application/json' \
  -d '{"persona_id": "tech_enthusiast", "ad_ids": ["laptop_ad", "phone_ad", "tablet_ad"]}'

# 2. Select an ad (initially random, as no data exists)
curl -X POST http://localhost:8000/select_ad \
  -H 'Content-Type: application/json' \
  -d '{"persona_id": "tech_enthusiast"}'

# 3. User clicked the ad - record success
curl -X POST http://localhost:8000/update \
  -H 'Content-Type: application/json' \
  -d '{"ad_id": "laptop_ad", "reward": {"success": 1, "failure": 0}}'

# 4. Select again - now informed by previous success
curl -X POST http://localhost:8000/select_ad \
  -H 'Content-Type: application/json' \
  -d '{"persona_id": "tech_enthusiast"}'
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for configuration:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000

# Strategy Configuration
BANDIT_STRATEGY=thompson_sampling

# Logging
LOG_LEVEL=INFO
```

## 📊 Thompson Sampling Algorithm

The algorithm uses **Beta-Bernoulli bandits**:

1. **Initialization**: Each ad starts with Beta(1, 1) prior (uniform distribution)
2. **Selection**: Sample θ from Beta(α, β) for each ad, select ad with highest θ
3. **Update**: After interaction:
   - Success (click): α = α + 1
   - Failure (no click): β = β + 1

This approach naturally balances:
- **Exploration**: Trying ads with high uncertainty
- **Exploitation**: Favoring ads with proven performance

## 🗂️ Project Structure

```
Bandit-persona-prompt/
├── ad_select_main.py                    # FastAPI application
├── ad_select_factory.py                 # Strategy factory
├── ad_select_strategy.py                # Abstract strategy interface
├── ad_select_thompson_sampling_strategy.py  # Thompson Sampling implementation
├── ad_select_data_model.py              # Pydantic models
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Container configuration
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## 🔮 Future Enhancements

- [ ] Epsilon-Greedy strategy implementation
- [ ] Upper Confidence Bound (UCB) strategy
- [ ] Contextual bandits with user features
- [ ] Persistence layer (Redis/PostgreSQL)
- [ ] A/B testing framework integration
- [ ] Metrics and monitoring (Prometheus)
- [ ] Multi-objective optimization
- [ ] Batch update support via Kafka

## 🤝 Integration with Event Streaming

This service is designed to integrate with event-driven architectures:

```
User Interaction → Kafka → Flink Processing → Update API → Thompson Sampling
                                                    ↓
                                            Redis Cache (optional)
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

**Note**: This project was developed with the assistance of an AI-Powered coding assistant.

## 👨‍💻 Author

Ravi G - Agentic AI Enthusiast

## 🙏 Acknowledgments

- Thompson Sampling algorithm based on Bayesian optimization principles
- Inspired by conceptual ad-tech systems using multi-armed bandits

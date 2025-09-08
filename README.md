# open-context7-api

The API server component of open-context7 ecosystem.

## Usage

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env.dev
# Edit .env.dev with your API keys

# Start development server
make dev
```

## Development

```bash
make install     # Full setup
make dev         # Development server
make beta        # Staging server
make prod        # Production server
make lint        # Code quality checks
```

## License

[MIT](LICENSE)

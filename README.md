# The Monospace Web (Python Edition)

A Python-powered replication of [The Monospace Web](https://github.com/owickstrom/the-monospace-web) by Oskar Wickström. 
Where the original uses Nix, Pandoc, and Make, this version uses Python, Jinja2, and duct tape.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install Python 3.13+ and other dependencies with uv:
   ```bash
   uv sync
   ```

3. Edit your markdown in `demo/index.md`

4. Build the site:
   ```bash
   uv run scripts/build.py
   ```

The generated site will be in the `docs` directory.

## Development

To run the tests:
```bash
uv run tests/test_replication.py
```

## License

MIT License - see [LICENSE](LICENSE) for details.

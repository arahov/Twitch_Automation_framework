# Quick Start Guide

## ⚡ Get Started in 3 Minutes

### 1. Install Dependencies (1 minute)

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run Tests (2 minutes)

```bash
# Run all tests
pytest

# OR use the convenient runner script
./run_tests.sh all
```

That's it! The framework will:
- ✅ Automatically download ChromeDriver
- ✅ Configure mobile emulation (Pixel 5)
- ✅ Navigate to Twitch
- ✅ Perform the search
- ✅ Take screenshots
- ✅ Generate reports

## 📊 View Results

After running tests:

- **Screenshots**: Check `screenshots/` folder
- **Logs**: Check `logs/framework.log`
- **Reports**: Check `reports/report.html`

## 🎯 Run Specific Tests

```bash
# Run only smoke tests
pytest -m smoke

# Run only critical tests
pytest -m critical

# Run a specific test ( USE THIS TO TEST THE OROGINAL ASSIGNMENT)
pytest tests/test_twitch_search.py::TestTwitchSearch::test_search_and_navigate_to_streamer

# Run in headless mode (no browser window)
HEADLESS=true pytest
```

## 🔧 Quick Configuration

Edit `.env` file to customize:

```bash
# Run in headless mode
HEADLESS=true

# Change device
DEVICE_NAME="iPhone 12"

# Increase timeout for slower connections
EXPLICIT_WAIT=30
```

## 📱 Supported Devices

- Pixel 5 (default)
- iPhone 12
- iPhone 14 Pro Max
- Samsung Galaxy S21

Change device:
```bash
DEVICE_NAME="iPhone 12" pytest
```

## 🚀 Multi-Device Parallel Testing

Run tests across multiple devices simultaneously for comprehensive cross-device validation!

```bash
# Run single test on all 4 devices in parallel
pytest -n 4 tests/test_twitch_search.py::TestTwitchSearch::test_search_and_navigate_to_streamer

# Run all tests distributed across 4 devices
pytest -n 4

# Run smoke tests on 2 devices (Pixel 5 and iPhone 12)
pytest -n 2 -m smoke

# Auto-detect worker count based on CPU cores
pytest -n auto
```

**Device Assignment**:
- Worker `gw0` → Pixel 5
- Worker `gw1` → iPhone 12
- Worker `gw2` → iPhone 14 Pro Max
- Worker `gw3` → Samsung Galaxy S21

**Benefits**:
- ✅ Test UI/UX consistency across devices
- ✅ Faster test execution (parallel)
- ✅ Device-specific screenshots and logs

## 🐛 Troubleshooting

**Tests taking too long?**
- Increase timeout: Set `EXPLICIT_WAIT=30` in `.env`

**Can't find elements?**
- Check if mobile emulation is enabled: `MOBILE_EMULATION=true` in `.env`

**Need more details?**
- Enable debug logging: Set `LOG_LEVEL=DEBUG` in `.env`
- Check logs: `cat logs/framework.log`

**Parallel tests not working?**
- Ensure `pytest-xdist` is installed: `pip install pytest-xdist`
- Check worker logs for device-specific issues
- Reduce worker count if system resources are limited

## 📚 Next Steps

See [README.md](README.md) for:
- Complete architecture details
- Advanced configuration
- CI/CD integration
- Adding new tests
- Best practices

## 🎓 Test Scenario

The framework automates this flow:
1. Go to https://m.twitch.tv/
2. Click search icon (browse tab)
3. Search for "StarCraft II"
4. Scroll down 2 times
5. Select a streamer
6. Wait for page load (handles popups automatically)
7. Take screenshot

All with proper error handling, retries, and logging!

#!/bin/bash

# Twitch Automation Framework - Test Runner Script
# This script provides easy commands to run tests with different configurations

set -e

echo "======================================"
echo "Twitch Automation Framework"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: ./run_tests.sh [OPTION]"
    echo ""
    echo "Options:"
    echo "  all               Run all tests"
    echo "  smoke             Run smoke tests only"
    echo "  critical          Run critical tests only"
    echo "  mobile            Run mobile tests only"
    echo "  regression        Run regression tests"
    echo "  parallel          Run tests in parallel"
    echo "  headless          Run tests in headless mode"
    echo "  report            Run tests and generate HTML report"
    echo "  single TEST_NAME  Run a specific test"
    echo "  help              Display this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_tests.sh all"
    echo "  ./run_tests.sh smoke"
    echo "  ./run_tests.sh headless"
    echo "  ./run_tests.sh single test_search_and_navigate_to_streamer"
    echo ""
}

# Check if pytest is installed
check_dependencies() {
    if ! command -v pytest &> /dev/null; then
        echo -e "${RED}Error: pytest is not installed${NC}"
        echo "Please run: pip install -r requirements.txt"
        exit 1
    fi
}

# Run tests based on argument
case "${1:-all}" in
    all)
        echo -e "${GREEN}Running all tests...${NC}"
        pytest -v
        ;;
    
    smoke)
        echo -e "${GREEN}Running smoke tests...${NC}"
        pytest -v -m smoke
        ;;
    
    critical)
        echo -e "${GREEN}Running critical tests...${NC}"
        pytest -v -m critical
        ;;
    
    mobile)
        echo -e "${GREEN}Running mobile tests...${NC}"
        pytest -v -m mobile
        ;;
    
    regression)
        echo -e "${GREEN}Running regression tests...${NC}"
        pytest -v -m regression
        ;;
    
    parallel)
        echo -e "${GREEN}Running tests in parallel...${NC}"
        pytest -v -n auto
        ;;
    
    headless)
        echo -e "${GREEN}Running tests in headless mode...${NC}"
        HEADLESS=true pytest -v
        ;;
    
    report)
        echo -e "${GREEN}Running tests and generating HTML report...${NC}"
        pytest -v --html=reports/report.html --self-contained-html
        echo -e "${GREEN}Report generated: reports/report.html${NC}"
        ;;
    
    single)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please specify test name${NC}"
            echo "Example: ./run_tests.sh single test_search_and_navigate_to_streamer"
            exit 1
        fi
        echo -e "${GREEN}Running test: $2${NC}"
        pytest -v -k "$2"
        ;;
    
    help|--help|-h)
        usage
        exit 0
        ;;
    
    *)
        echo -e "${RED}Error: Unknown option '$1'${NC}"
        echo ""
        usage
        exit 1
        ;;
esac

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}======================================"
    echo "Tests completed successfully!"
    echo "======================================${NC}"
else
    echo ""
    echo -e "${RED}======================================"
    echo "Tests failed! Check logs for details."
    echo "======================================${NC}"
    exit 1
fi

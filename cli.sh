#!/bin/bash

while true; do
    echo "Please choose a command to execute:"
    echo "1) Run unittest"
    echo "2) Run unittest with coverage"
    echo "3) Generate coverage report"
    echo "4) Generate coverage HTML report"
    echo "5) Exit"
    echo ""

    read -p "Enter your choice (1/2/3/4/5): " choice

    case $choice in
        1) 
            python -m unittest components/ast_binary_graph/test_codebase_graph.py
            ;;
        2)
            python -m coverage run -m unittest components/ast_binary_graph/test_codebase_graph.py
            ;;
        3)
            python -m coverage report
            ;;
        4)
            python -m coverage html
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac

    # Pause and wait for user input to continue
    read -p "Press any key to continue..."
    clear
done

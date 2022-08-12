# ACME Widget Co

## Prerequisites

Either `python 3.10` or `docker`

## Usage

Source code only cotains the `main.py` module, when executed it launches an interactive session that provides a simple interface to the basket and its functionalities.

Example session:

    Welcome to the interactive session
    ✨ Your basket awaits your orders ✨
    Waiting for user prompt to be:
        - add code - Add new widget to the basket, code should be one of [R01, B01, G01]
        - total - Returns total price of the basket
        - widgets - Returns current widgets added to the basket
        - catalog - Returns details about the widget catalog 
        - offers - Returns current offers available
        - clear - Resets the basket
        - exit - exit this interactive session
        
    > catalog
    - Red Widget, price $32.95, order with code R01
    - Green Widget, price $24.95, order with code G01
    - Blue Widget, price $7.95, order with code B01
    > add R01
    > add G01
    > widgets
    📦️ Current widgets 📦️
    Red Widget: 1
    Green Widget: 1
    > total
    60.85
    > exit

Clone

    git clone https://github.com/Hasan-J/acme-widgets.git
    cd acme-widgets

### python

Run

    python3.10 main.py

Test

    pytest

### docker

Uses `python:3.10.5-slim-bullseye` as base image

Build

    docker build -t acme-widgets:hasanjawad .

Run

    docker run -it --rm acme-widgets:hasanjawad

Test

    docker run -it --rm --entrypoint pytest acme-widgets:hasanjawad

Clean image

    docker image remove acme-widgets:hasanjawad
